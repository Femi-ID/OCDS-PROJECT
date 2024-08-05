from django.shortcuts import render
from .serializers import QuestionSerializer, ReplySerializer
from rest_framework.views import APIView
from rest_framework import status
from .models import Question, Reply
from community.models import Community 
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
import uuid
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Count
from django.http import JsonResponse
from django.template.defaultfilters import slugify


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


class ListQuestionByCommunity(APIView):
    """List all questions for a community."""
    # parser_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated]
        
    def get(self, request, community_id):
        # confirm if I should create a query to check if the user is a member of the community
        # try:
        community = get_object_or_404(Community, id=community_id)
        questions = Question.objects.filter(community=community).order_by('-updated_at')
        # questions = Question.objects.select_related('replies__body').filter(community=community).order_by('-updated_at')

        if not questions:
            return Response({"status": 204, 
                                "success": True,
                            "message": "The community exists but currently has no questions."})
        serializer = QuestionSerializer(questions, many=True)
        # replies = Reply.objects.filter(question=questions)
        # serialized_replies = ReplySerializer(replies, many=True)

        # question_replies = []
        # for question in questions:
        #     question_replies.append({'replies': question.replies})
        #     JsonResponse(question_replies)

        

        return Response({'status': 200,
                         'success': True,
                         'message': f'Community {community.name} and its questions',
                         'community_name': community.name,
                         'data': serializer.data,
                        #  'question_replies': question_replies
                        #  'serialized_replies':serialized_replies
                         },
                         status=status.HTTP_200_OK)
        # except Exception as e:
        #     return Response({
        #         "status": 500,
        #         "success": False,
        #         "message": f'Server Malfunctionzz: {e}'
        #         }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request, communityId):
        """Create new questions in a community."""
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
            
            if request.user not in community.users:
                return Response({
                    'error': "You are authenticated but cannot make this request; not a member of the community"},
                    status=status.HTTP_403_FORBIDDEN)
            serializer = QuestionSerializer(data=request.data)
            if serializer.is_valid():
                # serializer.owner = request.user
                serializer.save(owner=self.request.user, community=community, slug=slugify(serializer.data['title']))
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


class QuestionDetails(APIView):
    """View the details of the questions(replies, upvote, downvote)"""
    
    def get(self, request, question_id):
        try:
            question = get_object_or_404(Question, id=question_id)
            replies = Reply.objects.select_related('question').filter(question=question).order_by('-created_at')
            
            reply_serializer = ReplySerializer(replies, many=True)
            question_serializer = ReplySerializer(question)

            return Response({'status': 200,
                             'success': True,
                             'message': f'Question: "{question.title}" and its replies',
                             'Question_title': question.title,
                             'question_data': question_serializer.data,
                             'reply_data': reply_serializer.data,
                             },
                             status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": 500,
                "success": False,
                "message": f'Server Error: {e}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            