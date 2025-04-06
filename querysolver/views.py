from django.conf import settings
from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import QuerySerializer
from .mlmodels.querysolver import answer_question_simple


class QuerySolver(viewsets.ViewSet):
    def solveQuery(self, request):
        querySerializer = QuerySerializer(data=request.data)
        if querySerializer.is_valid():
            query = querySerializer.validated_data['query']
            response_data = {
                'query': query,
                'response': self.querySolver(query)
            }
            responseSerializer = QuerySerializer(response_data)
            return Response(responseSerializer.data, status=status.HTTP_200_OK)
            
        return Response(data=querySerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    def querySolver(self, query: str) -> str:
        return answer_question_simple(query, settings.GENAI_API_KEY)
        # Write your code here
        # return " ".join(query.split()[::-1])


