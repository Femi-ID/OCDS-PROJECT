from rest_framework import serializers
from .models import Question, Reply
from taggit.serializers import (TagListSerializerField, TaggitSerializer)
from django.db.models import Count, Sum
from .enums import VoteChoices, VOTE_CHOICES

class VoteCountField(serializers.Field):
    def to_representation(self, value):
        return value

#     def get_up_votes(self, object):
#         up_votes = self.object.filter('votes__vote_type'=='UPVOTE').annotate(
#             up_votes_sum=Count('vote_type'))
#         return up_votes


class QuestionSerializer(serializers.ModelSerializer, TaggitSerializer):
    tags = TagListSerializerField()
    owner = serializers.ReadOnlyField(source='owner.username')
    questions_replies=serializers.SerializerMethodField()
    # up_votes = serializers.SerializerMethodField()
    # down_votes = serializers.SerializerMethodField()
    

    class Meta:
        model = Question
        fields = ['id', 'owner', 'title', 'body', 'created_at', 'community', 
                  'owner', 'voted_by', 'tags', 'replies', 'questions_replies']
        
    def get_questions_replies(self, object):
            return object.replies.count()
            # queryset = Question.objects.filter(replies__question__id=object.id)
            # return QuestionSerializer(queryset, many=True).data

    # def get_down_votes(self, obj):
    #     # up_votes, down_votes = obj.total_votes()
    #     down_vote = obj.vote_type='DOWNVOTE'.count()
    #     return down_vote 

    # def get_up_votes(self, obj):
    #     return obj.vote_type.filter(vote_type='UPVOTE').annotate(
    #         up_votes_sum=Count('vote_type'))
    # def get_up_votes(self, obj):
    #     return Question.objects.filter(vote_type='UPVOTE').annotate(down_vote_sum=Count('vote_type'))
    #     # return QuestionSerializer(query_set, many=True)

    # def get_down_votes(self, obj):
    #     return Question.objects.filter(vote_type='DOWNVOTE').annotate(down_vote_sum=Count('vote_type'))
        # return QuestionSerializer(query_set, many=True)
        # return obj.vote_type.filter(vote_type='DOWNVOTE').count()
    
    # def getType1Items(self, ownerObj):
    #     queryset = models.Item.objects.filter(owner__id=ownerObj.id).filter(itemType="type1")
    #     return ItemSerializer(queryset, many=True).data
    
    
class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ['question_id', 'body', 'created_at']

    # upvote_count = serializers.SerializerMethodField()

    # def get_upvote_count(self, obj):
    #     return Reply.objects.filter(vote_type="UPVOTE").count()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        total_upvote = Reply.objects.filter(vote_type="UPVOTE").count()
        upvote = []
        upvote.append(total_upvote)
        values = len(upvote)
        print(values)
        print(upvote)
        representation['total_upvote'] = values
        return representation


        # def get_replies(self, obj):
        #     # length = self.reply.count()
        #     # return length

        #     queryset = Reply.objects.filter(question__id=obj.question)
            
        #     return QuestionSerializer(queryset, many=True).data


# class CommunityMessageSerializer(serializers.ModelSerializer):
#      no_of_messages = serializers.SerializerMethodField()
     
#      class Meta:
#         model = CommunityMessage
#         fields = ['id', 'owner', 'title', 'content', 'no_of_messages']
        
#      def get_no_of_messages(self, object):
#          return object.content.count()
    

# class VoteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model: Vote
#         fields = ['question', 'reply', 'voted_by', 'vote_type']