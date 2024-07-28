from rest_framework import serializers
from .models import Question, Reply, Vote
from taggit.serializers import (TagListSerializerField, TaggitSerializer)
from django.db.models import Count

class VoteCountField(serializers.Field):
    def to_representation(self, value):
        return value
    
class QuestionSerializer(serializers.ModelSerializer, TaggitSerializer):
    tags = TagListSerializerField
    owner = serializers.ReadOnlyField(source='owner.username')
    # up_votes = serializers.StringRelatedField(many=True, read_only=True)
    # up_votes = serializers.SerializerMethodField(source='total_votes.up_votes')
    # down_votes = serializers.SerializerMethodField(source='total_votes.down_votes')
    up_votes = VoteCountField(source='total_votes.up_votes')
    down_votes = VoteCountField(source='total_votes.down_votes')
    class Meta: 
        model = Question
        fields = ['id', 'owner', 'title', 'body', 'created_at', 'community', 'owner', 'votes', 'up_votes', 'down_votes']

    def get_up_votes(self, object):
        up_votes = self.object.filter('votes__vote_type'=='UPVOTE').annotate(
            up_votes_sum=Count('vote_type'))
        return up_votes

    def get_down_votes(self, object):
        return object.total_votes('down_votes')


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ['question', 'body', 'date_created']


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model: Vote
        fields = ['question', 'reply', 'voted_by', 'vote_type']

