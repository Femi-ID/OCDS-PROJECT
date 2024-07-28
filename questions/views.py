from django.shortcuts import render
from .serializers import QuestionSerializer, ReplySerializer, VoteSerializer
from rest_framework.views import APIView
from rest_framework import status
from .models import Question, Reply, Vote
from community.models import Community 
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
import uuid
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Count


# check for validity of uuid
def is_uuid_valid(uuid_to_test, version=4):
    try:
        uuid_obj = uuid.UUID(uuid_to_test, version=version)
        # community = Community.objects.get(id=uuid_obj)
    except ValueError:
        return Response({'error': "Invalid community id",
                         'status': 400}, 
                        status=status.HTTP_400_BAD_REQUEST)
    print({'message': 'Valid community id', 
                     'uuid_obj': uuid_obj})


class QuestionListByCommunity(APIView):
    """List all questions for the General page."""
    # parser_classes = [IsAuthenticated]
    # permission_classes = [IsAuthenticated]
        
    def get(self, request, communityId):
        # is_uuid_valid(communityId)
        # confirm if I should create a query to check if the user is a member of the community
        try:
            community = get_object_or_404(Community, id=communityId)
            questions = Question.objects.filter(community=community)
            if not questions:
                return Response({"status": 400, 
                                 "success": True,
                                "message": "The community exists but currently has no questions."})
            serializer = QuestionSerializer(questions, many=True)
            # for question in serializer.data['votes']:
            #     up_vote = question.total_votes.up_votes
            #     down_vote = question.total_votes.down_votes
            #     return {"up_vote":up_vote,"down_vote":down_vote}
            # quest_up_vote = 

            up_votes = questions.filter('votes__vote_type'=='UPVOTE').annotate(
                up_votes_sum=Count('vote_type'))
            down_votes = questions.filter('votes__vote_type'=='DOWNVOTE').annotate(
                down_votes_sum=Count('vote_type'))

        
            return Response({'status': 200,
                             'success': True,
                             'message': f'Community {community.name} and its questions',
                             'data': serializer.data},
                             status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": 500,
                "success": False,
                "message": f'Server Malfunction: {e}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request, communityId):
        # is_uuid_valid(communityId)
        try:
            community = get_object_or_404(Community, id=communityId)
            if not community:
                return Response({'status': 404,
                                    'error': 'Community does not exist.'}, 
                                status=status.HTTP_404_NOT_FOUND)
            
            if request.user.user_type not in ['mentor', 'admin']:
                return Response({'error': 'You are not authorized to create questions', 'status': 401}, 
                                status=status.HTTP_401_UNAUTHORIZED)
            
            serializer = QuestionSerializer(data=request.data)
            if serializer.is_valid():
                # serializer.save(commit=False)
                # serializer.owner = request.user
                serializer.save(owner=self.request.user, community=community, slug=serializer.data['title'])
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
                "message": f'Server Malfunction: {e}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class QuestionModelViewSet(ModelViewSet):
#     queryset = Question.objects.all()
#     serializer_class = QuestionSerializer