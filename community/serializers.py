from rest_framework import serializers
from .models import Information, Community
from questions.models import Question
from taggit.serializers import (TagListSerializerField, TaggitSerializer)
from django.db.models import Count, Sum

class InformationSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Information
        fields = ['title', 'content', 'owner']


class CommunitySerializer(serializers.ModelSerializer):
    class Meta: 
        model = Community
        fields = ['id', 'name', 'slug', 'description']
        

class QuestionSerializer(serializers.ModelSerializer, TaggitSerializer):
    tags = TagListSerializerField()
    # owner = serializers.ReadOnlyField(source='owner.username')
    # up_votes = serializers.SerializerMethodField()
    # down_votes = serializers.SerializerMethodField()
    questions_replies = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'owner', 'title', 'body', 'created_at', 'community','tags', 'questions_replies']

    # def get_up_votes(self, obj):
    #     up_votes, down_votes = obj.total_votes()
    #     return up_votes

    # def get_down_votes(self, obj):
    #     up_votes, down_votes = obj.total_votes()
    #     return down_votes 
    
    def get_questions_replies(self, object):
        # return object.annotate(questions_replies=Count("voted_by")).order_by('questions_replies')[:10]
        return object.replies.count()
    