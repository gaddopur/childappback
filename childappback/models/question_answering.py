"""
Question Answering Tool

This script provides functionality for answering questions using the Gemini API. 
It supports both command-line usage and programmatic integration with web services.

Features:
- Secure question validation
- API key management with failover
- Asynchronous support
- Robust error handling with retries

Usage Patterns:

Command Line:
--------------
python question_answering.py "What is photosynthesis?" --retries 3

Programmatic API:
-----------------
from question_answering import QuestionAnswerer

qa = QuestionAnswerer()

# Synchronous usage
answer = qa.answer("How do airplanes fly?")

# Asynchronous usage
async def get_answer():
    answer = await qa.async_answer("Why is the sky blue?")
    # Handle answer...

Web Service Integration:
------------------------
from fastapi import FastAPI
from question_answering import QuestionAnswerer

app = FastAPI()
qa = QuestionAnswerer()

@app.post("/answer")
async def answer_question(question: str):
    return await qa.async_answer(question)
"""

import os
import asyncio
import logging
import time
from threading import RLock
from typing import Optional, Tuple
import google.generativeai as genai
from google.api_core import exceptions
from api_key_manager import APIKeyManager

# Configure logging
logger = logging.getLogger(__name__)

def configure_logging():
    """Separate logging configuration for better control"""
    logger = logging.getLogger(__name__)
    logger.propagate = False  # Prevent propagation to root logger
    
    # Clear existing handlers
    if logger.handlers:
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # File handler
    file_handler = logging.FileHandler("qa_service.log")
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

class QuestionValidationError(Exception):
    """Custom exception for invalid questions."""
    pass

class QuestionAnswerer:
    """
    QuestionAnswerer Class
    
    Provides robust question answering using Gemini AI with:
    - Question validation and sanitization
    - API key rotation and failover
    - Retry logic with exponential backoff
    - Asynchronous support
    """
    
    def __init__(self, api_key_manager: APIKeyManager = None):
        self.api_key_manager = api_key_manager or APIKeyManager()
        self._lock = RLock()
        self.model_cache = {}
        self.model_config = {
            "temperature": 0,
            "top_p": 0.05,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }
        logger.info("QuestionAnswerer initialized")

    def _get_model(self, api_key: str) -> Optional[genai.GenerativeModel]:
        """Retrieve or create a configured Gemini model."""
        try:
            if api_key in self.model_cache:
                logging.debug(f"Model cache hit for ...{api_key[-4:]}")
                return self.model_cache[api_key]

            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(
                model_name="models/gemini-1.5-pro-001",
                generation_config=self.model_config
            )

            with self._lock:
                self.model_cache[api_key] = model

            logging.info(f"Model created for ...{api_key[-4:]}")
            return model

        except Exception as e:
            logging.error(f"Model creation failed: {str(e)}")
            return None

    async def async_answer(self, question: str, max_retries: int = 3) -> Optional[str]:
        """Asynchronous interface for question answering."""
        loop = asyncio.get_event_loop()
        try:
            return await loop.run_in_executor(None, self.answer, question, max_retries)
        except Exception as e:
            logging.error(f"Async processing failed: {str(e)}")
            return None

    def answer(self, question: str, max_retries: int = 3) -> Optional[str]:
        """Main entry point for question answering."""
        start_time = time.time()
        try:
            logger.info(f"Processing question: {question}...")
            valid, reason = self._validate_question(question)
            if not valid:
                logging.error(f"Validation failed: {reason}")
                return None

            result = self._process_question(question, max_retries)
            logger.info(f"Question processed in {time.time()-start_time:.2f}s")
            return result

        except Exception as e:
            logging.error(f"Processing failed after {time.time()-start_time:.2f}s: {str(e)}")
            return None

    def _process_question(self, question: str, max_retries: int) -> Optional[str]:
        """Core processing with retry logic."""
        for attempt in range(1, max_retries + 1):
            attempt_start = time.time()
            api_key = self.api_key_manager.get_available_key()
            if not api_key:
                logging.warning(f"Attempt {attempt} failed: No keys available")
                time.sleep(2 ** attempt)
                continue

            try:
                model = self._get_model(api_key)
                if not model:
                    continue

                prompt = (
                    f"Answer in very simple words for a school kid:\n"
                    f"Question: {question}\nAnswer:"
                )

                response = model.generate_content(prompt, request_options={'timeout': 30})
                self.api_key_manager.update_key_status(api_key, success=True)
                
                logging.info(f"Attempt {attempt} succeeded in {time.time()-attempt_start:.2f}s")
                return response.text.strip()

            except exceptions.ResourceExhausted as e:
                self._handle_error(api_key, f"Rate limit: {str(e)}", attempt, max_retries)
            except exceptions.GoogleAPIError as e:
                self._handle_error(api_key, f"API Error: {str(e)}", attempt, max_retries)
            except Exception as e:
                self._handle_error(api_key, f"Unexpected error: {str(e)}", attempt, max_retries)

        logging.error(f"Failed after {max_retries} attempts")
        return None

    def _validate_question(self, question: str) -> Tuple[bool, str]:
        """Validate input question."""
        if not isinstance(question, str):
            return False, "Question must be a string"
        if len(question.strip()) == 0:
            return False, "Empty question"
        if len(question) > 1000:
            return False, "Question too long (max 1000 characters)"
        return True, "Validation passed"

    def _handle_error(self, api_key: str, message: str, attempt: int, max_attempts: int):
        """Handle API errors and retries."""
        logging.warning(f"Attempt {attempt}/{max_attempts} failed: {message}")
        self.api_key_manager.update_key_status(api_key, success=False)
        time.sleep(1)

if __name__ == "__main__":
    import argparse

    def main():
        parser = argparse.ArgumentParser(description='Question Answering Tool')
        parser.add_argument('question', type=str, help='Question to answer')
        parser.add_argument('--retries', type=int, default=3, help='Retry attempts')
        args = parser.parse_args()

        qa = QuestionAnswerer()
        answer = qa.answer(args.question, args.retries)
        
        if answer:
            print("# Answer\n")
            print(answer)
            exit(0)
        else:
            logging.error("Failed to generate answer")
            exit(1)

    main()