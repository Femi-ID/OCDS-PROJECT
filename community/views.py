from django.shortcuts import render
from .models import Information, Community, CommunityMessage
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CommunitySerializer, InformationSerializer, QuestionSerializer, CommunityMessageSerializer
from accounts.models import User
from questions.models import Question
from django.db.models import Min, Max, Count
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


def join_ocds_community():
        """Add users who are not members of ocds community."""
        ocds_community = Community.objects.filter(slug='ocds-general-community').prefetch_related('users')
        users = User.objects.exclude(community=ocds_community)
        if users:
            ocds_community.users.add(*users)

class ListCommunitiesInformation(APIView):
    """Display information in the home page.""" 

    def get(self, request):
        information = Information.objects.all()
        trending_questions = Question.objects.annotate(quest=Count("replies")).order_by("-quest")[:5]
        communities = Community.objects.annotate(most_users=Count("users")).order_by('-most_users')[:5]

        community_questions = []
        for community in communities:
             questions = Question.objects.filter(community=community).annotate(trend=Count('replies')).order_by('-trend')[:5]
             community_questions.append(questions)
            #  print(community_questions)
        community_quest_serializer = QuestionSerializer(community_questions, many=True)

        # join_ocds_community()

        info_serializer = InformationSerializer(information, many=True)
        trending_question_serializer = QuestionSerializer(trending_questions, many=True)
        # community_quest_serializer = QuestionSerializer(community_questions, many=True)

        # trending_questions = Question.objects.filter('total_votes__gte'==1)[:5].order_by('total_votes')
        # trending_questions = Question.objects.annotate(quest=Count("votes__voted_by")).filter(quest__gte=1)[:10]
        return Response({'status': 200,
                         'success': True,
                         'message': 'Top 5 most trending questions.',
                         'data': info_serializer.data, 
                         'trending_questions': trending_question_serializer.data,
                        #  'community_quest_serializer': community_quest_serializer.data
                         },
                         status=status.HTTP_200_OK)


class ListCommunity(APIView):
    """To display the list of communities."""
    def get(self, request):
        communities = Community.objects.all()
        serializer = CommunitySerializer(communities, many=True)
        return Response({'status': 200,
                         'success': True,
                         'message': 'List of all communities.',
                         'data': serializer.data}, status=status.HTTP_200_OK)
    

class JoinCommunity(APIView):
    def post(self, request, community_id):
        # permission_classes = [IsAuthenticatedOrReadOnly, IsAuthenticated]
        if self.request.user.is_authenticated:
            community = get_object_or_404(Community, id=community_id)
            if request.user not in community.users:
                community.users.add(request.user)
                return Response({
                    'success': f'You have successfully joined "{community.name}" community'
                }, status=status.HTTP_204_NO_CONTENT)
            
            return Response({
                'message': "You are already a member of this community."
            }, status=status.HTTP_204_NO_CONTENT)
        return Response({
            'message': "Login or sign-up to join a community."
        })
            
    

class CreateInformation(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.user_type not in ['admin', 'mentor']: # change this back to only 'admin'
                return Response({'error': "You are not authorized to access this route. You can't create information.",
                                'status': 401},
                                status=status.HTTP_401_UNAUTHORIZED)
            
            admin_info = Information.objects.filter(owner=request.user)
            if admin_info:
                serializer = InformationSerializer(admin_info, many=True)
                return Response({
                    'message': f'The information created by this user: {request.user.username}',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            
        return Response({'message': "Login or sign-up. Only admins are allowed to create information.",
                         "status": 401},
                         status=status.HTTP_401_UNAUTHORIZED)
        

    def post(self, request):
        """Only admin users create information."""
        if request.user.is_authenticated:
            if self.request.user.user_type not in ['admin', 'mentor']: # change this back to only 'admin'
                return Response({'error': 'You are not authorized to create information.',
                                'status': 401},
                                status=status.HTTP_401_UNAUTHORIZED)
            
            serializer = InformationSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save(owner=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message': "Login or sign-up. Only admins are allowed to create information.",
                         "status": 401},
                         status=status.HTTP_401_UNAUTHORIZED)


class RetrieveCreateMessages(APIView):
    def get(self, request, communityId):
        try:
            if request.user not in community.users and request.user.user_type != 'admin':
                return Response({
                            'error': "You are authenticated but cannot make this request or not a member of the community"},
                            status=status.HTTP_403_FORBIDDEN)
            community = get_object_or_404(CommunityMessage, id=communityId)
            community_messages = CommunityMessage.objects.filter(community=community).order_by('-created_at')
            serializer = CommunityMessageSerializer(community_messages, many=True)            
            return Response({'status': 200,
                            'success': True,
                            'info': f'Community {community.name} and its messages.',
                            'community_name': community.name,
                            'messages': serializer.data,
                            #  'question_replies': question_replies
                            #  'serialized_replies':serialized_replies
                            },
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": 500,
                "success": False,
                "message": f'Internal server error: {e}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            # wake up and finish this!!!


    """Only admin users can send messages."""
    def post(self, request, communityId):
        if request.user.user_type == "admin":
            try:
                community = get_object_or_404(Community, id=communityId)
                
                if request.user not in community.users:
                    return Response({
                        'error': "You are authenticated but cannot make this request; not a member of the community"},
                        status=status.HTTP_403_FORBIDDEN)
                #  create a message model and replace it with the question serializer
                serializer = CommunityMessageSerializer(data=request.data)
                if serializer.is_valid():
                    # serializer.owner = request.user
                    serializer.save(owner=self.request.user, community=community)
                    return Response({'status': 200,
                                    'success': True,
                                    'message': f'Question has been created.',
                                    'data': serializer.data},
                                    status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
            except Exception as e:
                return Response({
                    "status": 500,
                    "success": False,
                    "message": f'Server Malfunction: {e}',
                    'error': 'You are not authorized to create questions'
                    }, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)