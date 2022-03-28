from django.http import request
from django.shortcuts import render
from django.utils.timezone import now

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import permissions
from rest_framework import generics, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import filters
from rest_framework.response import Response

from .serializers import *
from .filters import *
from rewrite.my_modelviewset import MyModelViewSet
from tool.paginations import CommonPagination
from tool import restful

#轮播图
class SwiperViews(MyModelViewSet):

    queryset = Swiper.objects.filter(deleted__exact='0')
    serializer_class = SwiperSerializer
    permission_classes = [permissions.IsAuthenticated]
    # pagination_class = CommonPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id','name']
    #search_fields = ['realname', 'user__username']
    
#轮播图
class SwiperOptionViews(MyModelViewSet):

    queryset = Swiper.objects.filter(deleted__exact='0')
    serializer_class = SwiperOptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id','name']
    search_fields = ['name',]
    
#增加公告
class NoticeViews(MyModelViewSet):

    queryset = Notice.objects.filter(deleted__exact='0')
    serializer_class = NoticeSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CommonPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id','name']
    #search_fields = ['realname', 'user__username']
    # def get_queryset(self, *args, **kwargs):
    #     top = self.request.query_params.get("top")
    #     if top:
    #         return Notice.objects.filter(deleted__exact='0')
    #     else:
    #         return Notice.objects.filter(deleted__exact='0')

    
#增加公告
class NoticeOptionViews(MyModelViewSet):

    queryset = Notice.objects.filter(deleted__exact='0')
    serializer_class = NoticeOptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id','name']
    search_fields = ['name',]
    