from django.shortcuts import render
from .models import Information, Community
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CommunitySerializer, InformationSerializer, QuestionSerializer
from accounts.models import User
from questions.models import Question
from django.db.models import Min, Max, Count
class ListCreateInformation(APIView):
    """Display information in the home page."""

    def get(self, request):
        information = Information.objects.all()
        trending_questions = Question.objects.annotate(quest=Count("replies")).order_by("-quest")[:5]
        communities = Community.objects.annotate(most_users=Count("users")).order_by('-most_users')[:5]

        # community_questions = []
        # for community in communities:
        #      questions = Question.objects.filter(community=community).annotate(trend=Count('replies')).order_by('-trend')[:5]
        #      community_questions.append(questions)
            #  return community_questions
        
        # if not information:
        #         return Response({"status": 200, 
        #                          "success": True,
        #                          "message": "No information available"})
        
        info_serializer = InformationSerializer(information, many=True)
        trending_question_serializer = QuestionSerializer(trending_questions, many=True)
        # community_quest_serializer = QuestionSerializer(community_questions, many=True)

        # trending_questions = Question.objects.filter('total_votes__gte'==1)[:5].order_by('total_votes')
        # trending_questions = Question.objects.annotate(quest=Count("votes__voted_by")).filter(quest__gte=1)[:10]
        return Response({'status': 200,
                         'success': True,
                         'message': 'Top 5 most trending questions.',
                         'data': info_serializer.data, 
                         'trending_questions': trending_question_serializer.data
                         },
                         status=status.HTTP_200_OK)

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
        return Response({'status': 200,
                         'success': True,
                         'message': 'List of all communities.',
                         'data': serializer.data}, status=status.HTTP_200_OK)