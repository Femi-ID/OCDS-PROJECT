from rest_framework import serializers
from .models import Question, Reply, Vote


class QuestionSerializer(serializers.Serializer):
    class Meta: 
        model = Question
        fields = ['owner', 'body', 'date_created']


class ReplySerializer(serializers.Serializer):
    class Meta:
        model = Reply
        fields = ['question', 'body', 'date_created']

