import asyncio
import logging
import random
import os

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
    def post(self, request):
        data = request.data
        expression = data['expression']
        print(expression)
        print(type(expression))
        try:
            result = self._evaluateExpression(expression)
            return Response({'result': result}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def _evaluateExpression(self, expression: str) -> str:
        bot = MathChatbot()
        response = asyncio.run(bot.chat("new_session_id_1", expression))
        print(response)
        return response
    

class SchoolBookSummaryView(APIView):
    def get(self, request):
        # Extract query parameters
        board = request.query_params.get('board')
        class_level = request.query_params.get('class')
        subject = request.query_params.get('subject')
        book_name = request.query_params.get('book_name')
        chapter = request.query_params.get('chapter')
        lang = request.query_params.get('lang')

        # Validate required parameters
        required_params = [board, class_level, subject, book_name, chapter, lang]
        if not all(required_params):
            return Response(
                {'error': 'Missing required parameters: board, class, subject, book_name, chapter, lang'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Construct directory path
        chapter_dir = f"Chapter_{int(chapter):02d}"  # Format as Chapter_01, Chapter_02, etc.
        summary_dir = os.path.join(
            settings.SCHOOL_BOOKS_SUMMARIES_ROOT,
            board,
            f"Class_{class_level}",
            subject,
            book_name,
            chapter_dir,
            lang
        )

        # Verify directory exists
        if not os.path.isdir(summary_dir):
            return Response(
                {'error': 'Summary directory not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Get random summary file
        try:
            summary_files = [f for f in os.listdir(summary_dir) if f.endswith('.md')]
            if not summary_files:
                return Response(
                    {'error': 'No summary files found in directory'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            selected_file = random.choice(summary_files)
            file_path = os.path.join(summary_dir, selected_file)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return Response({'summary': content})
        
        except Exception as e:
            return Response(
                {'error': f'Error retrieving summary: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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