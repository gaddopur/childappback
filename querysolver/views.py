import logging
import os

from django.conf import settings
from django.core.files.storage import default_storage
from rest_framework.response import Response
from rest_framework import status, viewsets, parsers
from rest_framework.views import APIView

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
        try:
            result = self._evaluateExpression(expression)
            return Response({'result': result}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def _evaluateExpression(expression: str) -> str:
        return eval(expression)
