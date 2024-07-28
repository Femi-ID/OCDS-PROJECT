from django.shortcuts import render
from .models import Information, Community
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CommunitySerializer, InformationSerializer
from accounts.models import User
from questions.models import Question

class ListCreateInformation(APIView):
    """Display information in the home page."""

    def get(self, request):
        information = Information.objects.all()
        if not information:
                return Response({"status": 200, 
                                 "success": True,
                                "message": "No information available"})
        serializer = InformationSerializer(information, many=True)

        trending_questions = Question.objects.filter()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if request.user.user_type != 'admin':
                return Response({'error': 'You are not authorized to create questions', 
                                 'status': 401}, 
                                status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = InformationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListCommunity(APIView):
    """To display the list of communities."""
    def get(self, request):
        communities = Community.objects.all()
        serializer = CommunitySerializer(communities, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)