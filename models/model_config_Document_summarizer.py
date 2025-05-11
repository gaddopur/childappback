"""
Configuration for Document Summarization Tool

Contains model configurations, supported document types, and processing parameters.
"""

MODEL_CONFIG = {
    "model_name": "gemini-2.0-flash-001",
    "generation_config": {
        "temperature": 0.1,
        "top_p": 0.3,
        "top_k": 40,
        "max_output_tokens": 8192
    },
    "max_file_size": 25 * 1024 * 1024,  # 25 MB
    "allowed_path_prefix": "../",  # Relative to MEDIA_ROOT
    "retry_config": {
        "max_retries": 5,
        "backoff_factor": 2
    }
}

PROMPT_TEMPLATES = {
    "default": "Summarize this document in 500 words or less, focusing on key points and main ideas:",
    "pdf": "Analyze this PDF document and create a comprehensive summary highlighting key sections and findings:",
    "docx": "Summarize this Word document, maintaining the structure of headings and important formatting elements:",
    "pptx": "Create a slide-by-slide summary of this presentation, highlighting main points from each slide:",
    "txt": "Summarize this text document, focusing on core concepts and important information:",
    "xlsx": "Analyze this spreadsheet and summarize key data points, trends, and important figures:",
    "md": "Summarize this Markdown document, preserving important code blocks and technical details:",
    "html": "Extract and summarize the main content from this HTML document, ignoring boilerplate:",
    "epub": "Create a chapter-wise summary of this eBook, focusing on plot development and key themes:"
}

SUPPORTED_TYPES = {
    "pdf": {"mime": "application/pdf", "extractor": "pymupdf"},
    "docx": {"mime": "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "extractor": "python-docx"},
    "pptx": {"mime": "application/vnd.openxmlformats-officedocument.presentationml.presentation", "extractor": "python-pptx"},
    "xlsx": {"mime": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "extractor": "openpyxl"},
    "txt": {"mime": "text/plain", "extractor": "native"},
    "md": {"mime": "text/markdown", "extractor": "native"},
    "html": {"mime": "text/html", "extractor": "bs4"},
    "epub": {"mime": "application/epub+zip", "extractor": "epub"}
}