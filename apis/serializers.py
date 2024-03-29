from info.models import *
from rest_framework import serializers
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django.utils import timezone



class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']

#---------------------------------------------------------------------------------------------
#------------------------------------------News Serializers ----------------------------------
#---------------------------------------------------------------------------------------------


class NewsSerializer(serializers.ModelSerializer):
    news_title = serializers.CharField(source='title')
    news_description = serializers.CharField(source='description')
    news_image = serializers.SerializerMethodField()
    #news_tags = serializers.ListField(source='tags.values_list("name", flat=True)')
    

    class Meta:
        model = News
        fields = ['id','news_title', 'news_description', 'news_image',]
    
    def get_news_image(self, obj):
        request = self.context.get('request', None)
        
        # Check if the image field is not None and not empty
        if obj.image:
            # If an image is present, return the absolute URL with media prefix
            return f"https://pigeon-i7rj.onrender.com{obj.image.url}"
        else:
            # If no image is present, return None
            return None
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['news_tags'] = [tag['name'] for tag in TagSerializer(instance.tags.all(), many=True).data]
        return representation

    

#---------------------------------------------------------------------------------------------
#------------------------------------------Notice Serializers ----------------------------------
#---------------------------------------------------------------------------------------------


class NoticeSerializer(serializers.ModelSerializer):
    notice_title = serializers.CharField(source='title')
    notice_description = serializers.CharField(source='description')
    notice_author = serializers.CharField(source='posted_by.name', allow_null=True)
    created_date = serializers.SerializerMethodField()
    #news_tags = serializers.ListField(source='tags.values_list("name", flat=True)')
    

    class Meta:
        model = Notice
        fields = ['id','notice_title', 'notice_description', 'notice_author','created_date']

    def get_created_date(self, instance):
        return instance.created_date.strftime('%Y-%m-%d')
    
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['notice_tags'] = [tag['name'] for tag in TagSerializer(instance.tags.all(), many=True).data]
        return representation
