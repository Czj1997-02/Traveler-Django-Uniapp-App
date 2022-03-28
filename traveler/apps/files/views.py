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

# Create your views here.

#first
class ImagesViews(MyModelViewSet):

    queryset = Images.objects.filter(deleted__exact='0')
    serializer_class = ImagesSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CommonPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    #search_fields = ['realname', 'user__username']
    def create(self, request, *args, **kwargs):
        """
        创建一个模型的实例.
        """
        # print(request.data)
        # 直接修改request.data,使用API提交时会报 AttributeError: This QueryDict instance is immutable错误
        # request.data['created_by'] = request.user.id
        # request.data['createdDate'] = now()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['created_by'] = request.user.extension
        serializer.validated_data['last_edited_by'] = request.user.extension
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        context = {
            'code': status.HTTP_201_CREATED,
            'msg': '创建成功！',
            'data': serializer.data
        }
        return Response(context, status=status.HTTP_201_CREATED, headers=headers)
    
#first
class ImagesOptionViews(MyModelViewSet):

    queryset = Images.objects.filter(deleted__exact='0')
    serializer_class = ImagesOptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    # search_fields = ['name',]
    
#first
class FilesViews(MyModelViewSet):

    queryset = Files.objects.filter(deleted__exact='0')
    serializer_class = FilesSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CommonPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    #search_fields = ['realname', 'user__username']
    
#first
class FilesOptionViews(MyModelViewSet):

    queryset = Files.objects.filter(deleted__exact='0')
    serializer_class = FilesOptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    # search_fields = ['name',]
    