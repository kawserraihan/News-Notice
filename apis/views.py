from django.shortcuts import render
from info.models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
#from rest_framework.authtoken.models import Token
#from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
#from itertools import chain
from rest_framework import serializers, status
from rest_framework.generics import ListAPIView
from django.db.models.signals import post_save
from rest_framework.generics import get_object_or_404
from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from django.db.models import Sum, Count
from django.conf import settings
import apis.serializers as api_ser
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from apis.serializers import *
from collections import defaultdict

#---------------------------------------------------------------------------------------------
#------------------------------------------News API VIEW -------------------------------------
#---------------------------------------------------------------------------------------------

class NewsAll(APIView):
    def get(self,request):
        news = News.objects.all()
        serializer = NewsSerializer(news, many=True)
        
        return JsonResponse(serializer.data, safe=False)
    

class NoticesAll(APIView):
    def get(self,request):
        notices = Notice.objects.all()
        serializer = NoticeSerializer(notices, many=True)
        
        return JsonResponse(serializer.data, safe=False)