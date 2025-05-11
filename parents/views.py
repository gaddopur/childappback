from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Parent, Child
from .serializers import ParentSerializer, ChildSerializer


# react
#

# Create your views here.

class ParentView(APIView):

    def get(self, request):
        email = request.GET.get('email')
        if email is not None:
            parent = Parent.objects.get(email=email)
            serializer = ParentSerializer(parent, many=False)

            return Response(serializer.data)
        else:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = ParentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChildView(APIView):

    def _verify_parent_token(self, token):
        try:
            parent = Parent.objects.get(auth_token=token)
            return parent is not None
        except Parent.DoesNotExist:
            return False

    def get(self, request):
        parent_token = request.headers.get('Authorization')
        if not parent_token or not self._verify_parent_token(parent_token):
            return Response({'error': 'Invalid parent authentication'},
                            status=status.HTTP_401_UNAUTHORIZED)

        email = request.GET.get('email')
        if email is not None:
            child = Child.objects.get(email=email)
            serializer = ChildSerializer(child, many=False)

            return Response(serializer.data)
        else:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = ChildSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)