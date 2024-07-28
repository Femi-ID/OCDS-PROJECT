from rest_framework import serializers
from .models import Information, Community


class InformationSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Information
        fields = ['title', 'content', 'owner']


class CommunitySerializer(serializers.ModelSerializer):
    class Meta: 
        model = Community
        fields = ['name', 'slug', 'description']
        