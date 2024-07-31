from rest_framework import serializers
from .models import Question, Reply
from taggit.serializers import (TagListSerializerField, TaggitSerializer)
from django.db.models import Count

class VoteCountField(serializers.Field):
    def to_representation(self, value):
        return value
    
# class QuestionSerializer(serializers.ModelSerializer, TaggitSerializer):
#     tags = TagListSerializerField
#     owner = serializers.ReadOnlyField(source='owner.username')
#     # up_votes = serializers.StringRelatedField(many=True, read_only=True)
#     # up_votes = serializers.SerializerMethodField(source='total_votes.up_votes')
#     # down_votes = serializers.SerializerMethodField(source='total_votes.down_votes')
#     up_votes = VoteCountField(source='total_votes.up_votes')
#     down_votes = VoteCountField(source='total_votes.down_votes')
#     class Meta: 
#         model = Question
#         fields = ['id', 'owner', 'title', 'body', 'created_at', 'community', 'owner', 'votes', 'up_votes', 'down_votes']

#     def get_up_votes(self, object):
#         up_votes = self.object.filter('votes__vote_type'=='UPVOTE').annotate(
#             up_votes_sum=Count('vote_type'))
#         return up_votes

#     def get_down_votes(self, object):
#         return object.total_votes('down_votes')


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

    # def get_up_votes(self, obj):
    #     up_votes, down_votes = obj.total_votes()
    #     return up_votes

    # def get_down_votes(self, obj):
    #     up_votes, down_votes = obj.total_votes()
    #     return down_votes 

    # def get_up_votes(self, obj):
    #     return obj.vote_type.filter(vote_type='UPVOTE').annotate(
    #         up_votes_sum=Count('vote_type'))

    # def get_down_votes(self, obj):
    #     return obj.vote_type.filter(vote_type='DOWNVOTE').count()
    
    
    


class ReplySerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    class Meta:
        model = Reply
        fields = ['question', 'body', 'date_created', 'length', 'questions_replies']


        def get_replies(self, obj):
            length = self.reply.count()
            return length


# class VoteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model: Vote
#         fields = ['question', 'reply', 'voted_by', 'vote_type']