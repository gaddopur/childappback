import asyncio
import logging
import random
import os
import uuid
import asyncio
import re

from django.conf import settings
from django.core.files.storage import default_storage
from rest_framework.response import Response
from rest_framework import status, viewsets, parsers
from rest_framework.views import APIView

from models.Math_Tutor import MathChatbot
from models.pdf_summerizer import PDFSummarizer
from models.question_answering import QuestionAnswerer
from .serializers import QuerySerializer, UploadFileSerializer

logger = logging.getLogger(__name__)

class QuerySolver(viewsets.ViewSet):
    def solveQuery(self, request):
        querySerializer = QuerySerializer(data=request.data)
        if querySerializer.is_valid():
            query = querySerializer.validated_data['query']
            response_data = {
                'query': query,
                'response': self._querySolver(query)
            }
            responseSerializer = QuerySerializer(response_data)
            return Response(responseSerializer.data, status=status.HTTP_200_OK)
            
        return Response(data=querySerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    def _querySolver(self, query: str) -> str:
        qa = QuestionAnswerer()
        answer = qa.answer(query)
        return answer


class SummarizePdfView(APIView):

    parser_classes = [parsers.MultiPartParser, parsers.FormParser]  # Important for file uploads!

    """
    API endpoint to handle POST requests for summarizing a PDF document.
    """

    def post(self, request):
        serializer = UploadFileSerializer(data=request.data)
        if serializer.is_valid():
            upload_file = serializer.validated_data['file']
            if upload_file:
                file_name = os.path.basename(upload_file.name)
                uploads_dir = os.path.join(settings.MEDIA_ROOT, 'upload')
                os.makedirs(uploads_dir, exist_ok=True)  # Ensure directory exists

                # Full file path with filename
                file_path = "upload/" + file_name
                # Log the absolute file path for debugging

                default_storage.save(file_path, upload_file)
                summary = self._summarizePdf(file_path)
                return Response({'message': 'File uploaded successfully', 'content': summary})

            return Response({'error': 'No file found in the request'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'error': 'Failed to upload file'}, status=status.HTTP_400_BAD_REQUEST)

    def _summarizePdf(self, file_path: str) -> str:
        summarizer = PDFSummarizer()
        summary = summarizer.summarize(file_path)
        return summary


class MathSolver(APIView):
    parser_classes = [parsers.JSONParser]

    # single shared bot instance (holds all session histories in memory)
    bot = MathChatbot()

    def post(self, request):
        """
        POST /querysolver/math_solver/
        Body: { "expression": "2+3",           # required
                "session_id": "abc123" }       # optional

        Response: { "result": "...",           # bot’s answer
                    "session_id": "abc123" }    # use to continue        
        """
        data = request.data
        expr = data.get('expression')
        if not expr:
            return Response(
                {"error": "Missing 'expression'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # grab or create a session_id
        raw_sid = data.get("session_id")
        if raw_sid:
            session_id = re.sub(r"[^\w-]", "", raw_sid)[:32]
        else:
            session_id = uuid.uuid4().hex

        try:
            # call the bot via the class attribute
            answer = asyncio.run(self.bot.chat(session_id, expr))

            return Response(
                {
                    "result": answer,
                    "session_id": session_id
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            # log it if you like: logger.exception(e)
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SchoolBookSummaryView(APIView):
    def get(self, request):
        # Extract query parameters
        board = request.query_params.get('board')
        class_level = request.query_params.get('class')
        subject = request.query_params.get('subject')
        book_name = request.query_params.get('book_name')
        chapter = request.query_params.get('chapter')
        lang = request.query_params.get('lang')
        file_name = request.query_params.get('file')

        # Validate required parameters
        required_params = [board, class_level, subject, book_name, chapter, lang]
        if not all(required_params):
            return Response(
                {'error': 'Missing required parameters: board, class, subject, book_name, chapter, lang'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        logger.info(f"Received parameters: board={board}, class={class_level}, subject={subject}, book_name={book_name}, chapter={chapter}, lang={lang}")

        # Construct directory path - FIXED CLASS LEVEL HANDLING
        summary_dir = os.path.join(
            settings.SCHOOL_BOOKS_SUMMARIES_ROOT,
            board,
            class_level,  # Use class_level directly without additional prefix
            subject,
            book_name,
            chapter,      # Use chapter name directly
            lang
        )

        logger.info(f"Constructed summary directory: {summary_dir}")
        
        # Verify directory exists
        if not os.path.isdir(summary_dir):
            logger.warning(f"Summary directory not found: {summary_dir}")
            return Response(
                {'error': 'Summary directory not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Handle file selection
        try:
            summary_files = [f for f in os.listdir(summary_dir) 
                            if f.endswith('.md') and os.path.isfile(os.path.join(summary_dir, f))]
            
            if not summary_files:
                logger.warning(f"No markdown files found in: {summary_dir}")
                return Response(
                    {'error': 'No summary files found in directory'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            selected_file = random.choice(summary_files)
            file_path = os.path.join(summary_dir, selected_file)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return Response({
                'summary': content,
                'file_name': selected_file,
                'file_path': file_path
            })
        
        except Exception as e:
            logger.exception(f"Error retrieving summary from {summary_dir}")
            return Response(
                {'error': f'Error retrieving summary: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class AvailableSummaryOptionsView(APIView):
    def get(self, request):
        try:
            base_path = settings.SCHOOL_BOOKS_SUMMARIES_ROOT
            logger.info(f"Fetching available options from: {base_path}")
            
            # Validate base path
            if not os.path.exists(base_path):
                error_msg = f"Base directory not found: {base_path}"
                logger.error(error_msg)
                return Response({"error": error_msg}, status=status.HTTP_404_NOT_FOUND)
            
            if not os.path.isdir(base_path):
                error_msg = f"Path is not a directory: {base_path}"
                logger.error(error_msg)
                return Response({"error": error_msg}, status=status.HTTP_400_BAD_REQUEST)
            
            # Get all boards
            boards = [d for d in os.listdir(base_path) 
                     if os.path.isdir(os.path.join(base_path, d))]
            logger.info(f"Found boards: {boards}")
            
            return Response({"boards": boards})
            
        except Exception as e:
            logger.exception("Unhandled error in AvailableSummaryOptionsView")
            return Response(
                {"error": f"Internal server error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class NestedOptionsView(APIView):
    def get(self, request):
        path = request.query_params.get('path', '')
        full_path = os.path.join(settings.SCHOOL_BOOKS_SUMMARIES_ROOT, path)
        
        logger.info(f"Fetching nested options for path: {full_path}")
        
        if not os.path.exists(full_path):
            logger.error(f"Path not found: {full_path}")
            return Response({"error": "Path not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if not os.path.isdir(full_path):
            logger.error(f"Path is not a directory: {full_path}")
            return Response({"error": "Not a directory"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            options = [d for d in os.listdir(full_path) 
                      if os.path.isdir(os.path.join(full_path, d))]
            logger.info(f"Found options: {options}")
            
            return Response({"options": options})
        
        except Exception as e:
            logger.exception(f"Error listing {full_path}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FileExplorerView(APIView):
    def get(self, request):
        try:
            path = request.query_params.get('path', '')
            base_path = settings.SCHOOL_BOOKS_SUMMARIES_ROOT
            
            # Normalize paths
            base_path = os.path.normpath(base_path)
            full_path = os.path.normpath(os.path.join(base_path, path))
            
            # Security check: ensure the requested path is within base_path
            if not full_path.startswith(base_path):
                logger.error(f"Security violation: {full_path} is outside of {base_path}")
                return Response({"error": "Invalid path"}, status=400)
            
            logger.info(f"File explorer request - Path: '{path}', Full path: '{full_path}'")
            
            if not os.path.exists(full_path):
                logger.error(f"Path not found: {full_path}")
                return Response({"error": "Path not found"}, status=404)
            
            if not os.path.isdir(full_path):
                logger.error(f"Path is not a directory: {full_path}")
                return Response({"error": "Not a directory"}, status=400)
            
            # Get directory contents
            contents = []
            for item in os.listdir(full_path):
                item_path = os.path.join(full_path, item)
                rel_path = os.path.relpath(item_path, base_path)
                
                # Normalize path separators for frontend
                rel_path = rel_path.replace('\\', '/')
                
                if os.path.isdir(item_path):
                    contents.append({
                        "name": item,
                        "path": rel_path,
                        "isDir": True
                    })
                elif item.endswith('.md'):
                    contents.append({
                        "name": item,
                        "path": rel_path,
                        "isDir": False,
                        "size": os.path.getsize(item_path)
                    })
            
            logger.info(f"Returning {len(contents)} items for path: {path}")
            
            return Response({
                "basePath": base_path.replace('\\', '/'),
                "currentPath": path,
                "contents": contents
            })
        
        except Exception as e:
            logger.exception(f"Critical error in FileExplorerView")
            return Response({"error": str(e)}, status=500)
""""

{
"expression": "find all the root of x**2-4x-77"
}
"""

"""
Home page


//[
//  "AIzaSyDrWsM293WR0dAndDmeZY55-bCdS1yYNQs",
//  "AIzaSyCZMSbCBw0gYLpoJqQzx7_TJ-PJ9pJAzTI",
//  "AIzaSyDN_5m5C7Tu2-_jJVARWUiBJCHG4jsE5Ns",
//  "AIzaSyAzSUEVeGNFtBOtLQUTEUoD9ZrJU0fzNzQ",
//  "AIzaSyBkZNpcVBe0KyeNi5Xgo5LLY1vNJDeQvDo",
//  "AIzaSyAniT0B7C4ZdVqc7DJLvErHXhpGkCNZPZA",
//  "AIzaSyCfFOnGjgd-ZXS0VgPQ-wejgWGQTXcMpVw",
//  "AIzaSyDmG6cUWjZBIdYI5H1NDqdaYwZjMYmjFYY"
//]
[
"""