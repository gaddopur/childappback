"""
PDF Summarization Tool

This script provides functionality for summarizing PDF documents using a Generative AI model. 
It is designed to be used both as a command-line tool and a programmatic API, with support 
for integration into web services.

Features:
- Secure validation of PDF files (path safety, type, size).
- Robust text extraction from PDF documents.
- API key management with retry and failover logic.
- Asynchronous support for scalable web applications.

Usage Patterns:

Command Line:
--------------
python pdf_summarizer.py "/path/to/file.pdf" --retries 5

Programmatic API:
-----------------
from pdf_summarizer import PDFSummarizer

summarizer = PDFSummarizer()

# Synchronous usage
summary = summarizer.summarize("document.pdf")

# Asynchronous usage
async def process_file():
    summary = await summarizer.async_summarize("document.pdf")
    # Handle the summary...

Web Service Integration:
------------------------
from fastapi import FastAPI, UploadFile
from pdf_summarizer import PDFSummarizer
import tempfile

app = FastAPI()
summarizer = PDFSummarizer()

@app.post("/summarize")
async def summarize_pdf(file: UploadFile):
    with tempfile.NamedTemporaryFile(delete=True) as tmp:
        tmp.write(await file.read())
        return await summarizer.async_summarize(tmp.name)
"""

import os
import asyncio
import logging
import time
from pathlib import Path
import fitz # PyMuPDF
from threading import RLock
from typing import Optional, Tuple
import google.generativeai as genai
from google.api_core import exceptions
from api_key_manager import APIKeyManager

# Configure logging to output to both a file and the console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("summary_service.log"),  # Log file
        logging.StreamHandler()  # Console output
    ]
)

class PDFValidationError(Exception):
    """Custom exception for PDF validation failures."""
    pass

class PDFSummarizer:
    """
    PDFSummarizer Class

    This class provides the core functionality to summarize PDF documents using a 
    Generative AI model. It includes features for:
    - Secure validation of input PDFs, including path sanitization, file type, and size checks.
    - Robust text extraction from PDF files.
    - Fail-safe integration with the Generative AI model, supporting API key management, retries, and logging.
    - Asynchronous support for use in web applications or scalable systems.

    Usage:
    Create an instance of PDFSummarizer and use the `summarize` method for synchronous 
    processing or `async_summarize` for asynchronous processing. The class is designed 
    for reuse in various contexts, including command-line tools, APIs, or backend services.
    """
    
    def __init__(self, api_key_manager: APIKeyManager = None):
        """
        Initialize the summarizer with API key management and configuration.
        :param api_key_manager: APIKeyManager instance for managing API keys.
        """
        self.api_key_manager = api_key_manager or APIKeyManager()
        self._lock = RLock()  # Thread-safe lock for shared resources
        self.model_cache = {}  # Cache for models keyed by API keys
        self.model_config = {  # Configuration for the generative AI model
            "temperature": 0.3,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
        }
        
        # Define security restrictions for PDF file paths and size
        self.allowed_path_prefix = Path(
            os.getenv("ALLOWED_PDF_PATH", os.path.abspath(os.path.join(os.getcwd(), "../")))
        ).resolve()
        logging.info(f"Allowed path prefix set to: {self.allowed_path_prefix}")
        self.max_file_size = 10 * 1024 * 1024  # 10 MB file size limit

    def _get_model(self, api_key: str) -> Optional[genai.GenerativeModel]:
        """
        Retrieve or create a generative model for a given API key.
        :param api_key: The API key to configure the model.
        :return: Configured generative model or None if failed.
        """
        start_time = time.time()
        try:
            if api_key in self.model_cache:
                logging.debug(f"Model cache hit for ...{api_key[-4:]}")
                return self.model_cache[api_key]

            # Configuration timing
            config_start = time.time()
            genai.configure(api_key=api_key)
            config_duration = time.time() - config_start

            # Model creation timing
            model_start = time.time()
            model = genai.GenerativeModel(
                model_name="models/gemini-1.5-pro-001",
                generation_config=self.model_config
            )
            model_duration = time.time() - model_start

            with self._lock:
                self.model_cache[api_key] = model

            logging.info(
                f"Model created for ...{api_key[-4:]} | "
                f"Config: {config_duration:.2f}s, "
                f"Init: {model_duration:.2f}s"
            )
            return model

        except Exception as e:
            logging.error(f"Model creation failed after {time.time()-start_time:.2f}s: {str(e)}")
            return None

    async def async_summarize(self, pdf_path: str) -> Optional[str]:
        """
        Asynchronous interface to summarize a PDF file.
        :param pdf_path: Path to the PDF file.
        :return: Generated summary or None if failed.
        """
        loop = asyncio.get_event_loop()
        try:
            # Run the synchronous summarize method in an executor
            return await loop.run_in_executor(None, self.summarize, pdf_path)
        except Exception as e:
            logging.error(f"Async processing failed: {str(e)}")
            return None

    def summarize(self, pdf_path: str, max_retries: int = 3) -> Optional[str]:
        """
        Generate a summary for a PDF file.
        :param pdf_path: Path to the PDF file.
        :param max_retries: Maximum number of retry attempts.
        :return: Generated summary or None if failed.
        """
        total_start = time.time()
        try:
            # Validation timing
            valid_start = time.time()
            valid, reason = self._validate_pdf(pdf_path)
            valid_duration = time.time() - valid_start
            if not valid:
                logging.error(f"Validation failed in {valid_duration:.2f}s: {reason}")
                return None

            # Processing
            process_start = time.time()
            result = self._process_pdf(pdf_path, max_retries)
            process_duration = time.time() - process_start

            logging.info(
                f"Total processing time: {time.time()-total_start:.2f}s | "
                f"Validation: {valid_duration:.2f}s | "
                f"Core processing: {process_duration:.2f}s"
            )
            return result
        
        except Exception as e:
            logging.error(f"Total failure after {time.time()-total_start:.2f}s: {str(e)}")
            return None

    def _process_pdf(self, pdf_path: str, max_retries: int) -> Optional[str]:
        """
        Process the PDF file to generate a summary with retries.
        :param pdf_path: Path to the PDF file.
        :param max_retries: Maximum number of retry attempts.
        :return: Generated summary or None if failed.
        """
        for attempt in range(1, max_retries + 1):
            attempt_start = time.time()
            api_key = self.api_key_manager.get_available_key()
            if not api_key:
                logging.warning(f"Attempt {attempt} failed: No keys available")
                time.sleep(2 ** attempt)  # Exponential backoff for retries
                continue

            try:
                # Extract text from the PDF
                extract_start = time.time()
                text = self._extract_text(pdf_path)
                extract_duration = time.time() - extract_start
                if not text:
                    return None

                # Get the model for the API key
                model_start = time.time()
                model = self._get_model(api_key)
                model_duration = time.time() - model_start
                if not model:
                    continue

                # Generate the summary
                gen_start = time.time()
                response = model.generate_content(
                    f"Summarize this document in 500 words or less:\n{text[:]}",
                    request_options={'timeout': 30}
                )
                gen_duration = time.time() - gen_start
                # Update key usage status
                self.api_key_manager.update_key_status(api_key, success=True)
                logging.info(
                    f"Attempt {attempt} success | "
                    f"Extract: {extract_duration:.2f}s | "
                    f"Model: {model_duration:.2f}s | "
                    f"Gen: {gen_duration:.2f}s"
                )
                return response.text

            except exceptions.ResourceExhausted:
                error_duration = time.time() - attempt_start
                logging.warning(f"Attempt {attempt} failed in {error_duration:.2f}s: {str(e)}")
                self._handle_error(api_key, "Rate limit exceeded", attempt, max_retries)
            except exceptions.GoogleAPIError as e:
                error_duration = time.time() - attempt_start
                logging.warning(f"Attempt {attempt} failed in {error_duration:.2f}s: {str(e)}")
                self._handle_error(api_key, f"API Error: {str(e)}", attempt, max_retries)
            except Exception as e:
                error_duration = time.time() - attempt_start
                logging.warning(f"Attempt {attempt} failed in {error_duration:.2f}s: {str(e)}")
                self._handle_error(api_key, f"Unexpected error: {str(e)}", attempt, max_retries)

        logging.error(f"Failed after {max_retries} attempts")
        return None

    def _validate_pdf(self, pdf_path: str) -> Tuple[bool, str]:
        """
        Validate the PDF file for path safety, existence, type, and size.
        :param pdf_path: Path to the PDF file.
        :return: Tuple with validation status and reason.
        """
        try:
            path = Path(pdf_path).resolve()

            # Debugging logs for resolved paths
            logging.debug(f"Resolved input path: {path}")
            logging.debug(f"Allowed path prefix: {self.allowed_path_prefix}")

            # Ensure the file path is within the allowed directory
            if not path.is_relative_to(self.allowed_path_prefix):
                return False, (
                    f"Security restriction: PDF must be in {self.allowed_path_prefix}\n"
                    f"Attempted path: {path}"
                )
            
            # Check file existence and type
            if not path.exists():
                return False, "File not found"
            if path.suffix.lower() != '.pdf':
                return False, "Invalid file type"
            
            # Check file size
            file_size = path.stat().st_size
            if file_size > self.max_file_size:
                return False, f"File too large ({file_size/1024/1024:.1f}MB > {self.max_file_size/1024/1024}MB limit)"
                
            return True, "Validation passed"
            
        except Exception as e:
            return False, f"Validation error: {str(e)}"

    def _extract_text(self, pdf_path: str) -> Optional[str]:
        """
        Extract text from the PDF file.
        :param pdf_path: Path to the PDF file.
        :return: Extracted text or None if extraction failed.
        """
        try:
            text = []
            with fitz.open(pdf_path) as doc:
                for page in doc.pages():
                    text.append(page.get_text())
            full_text = "\n".join(text)
            
            if not full_text.strip():
                logging.warning("No text extracted from PDF")
                return None
                
            logging.debug(f"Extracted {len(full_text)} characters")
            return full_text
            
        except Exception as e:
            logging.error(f"Text extraction failed: {str(e)}")
            return None

    def _handle_error(self, api_key: str, message: str, attempt: int, max_attempts: int):
        """
        Handle errors during API calls or retries.
        :param api_key: The API key used in the failed attempt.
        :param message: Error message.
        :param attempt: Current attempt number.
        :param max_attempts: Total number of allowed attempts.
        """
        logging.warning(f"Attempt {attempt}/{max_attempts} failed: {message}")
        self.api_key_manager.update_key_status(api_key, success=False)
        time.sleep(1)  # Brief pause between retries

if __name__ == "__main__":
    import argparse

    def main():
        """
        Main function to execute the PDF summarization tool.
        """
        parser = argparse.ArgumentParser(description='PDF Summarization Tool')
        parser.add_argument('pdf_path', type=str, help='Path to PDF file')
        parser.add_argument('--retries', type=int, default=3, help='Number of retry attempts')
        args = parser.parse_args()

        summarizer = PDFSummarizer()

        summary = summarizer.summarize(args.pdf_path, args.retries)
        
        if summary:
            print("# PDF Summary\n")
            print(summary)
            exit(0)
        else:
            logging.error("Failed to generate summary")
            exit(1)

    main()