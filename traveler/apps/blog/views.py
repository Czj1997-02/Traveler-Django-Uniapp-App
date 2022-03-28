from django.http import request
from django.shortcuts import render
from django.utils.timezone import now

from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
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
class BlogViews(MyModelViewSet):

    # queryset = Blog.objects.filter(deleted__exact='0')
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CommonPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    filter_class = BlogFilter
    search_fields = ['name', 'desc','content']
    #search_fields = ['realname', 'user__username']
    def get_queryset(self, *args, **kwargs):
        follower = self.request.query_params.get('follower')
        if follower:
            if int(follower) == self.request.user.extension.id:
                return Blog.objects.filter(deleted__exact='0').filter(created_by = self.request.user.extension)
            else:
                return Blog.objects.filter(deleted__exact='0').filter(created_by = int(follower),show = True)
        else:
            return Blog.objects.filter(deleted__exact='0').filter(Q(created_by = self.request.user.extension) | Q(show = True))
    # def get_queryset(self, *args, **kwargs):
    #     tags = self.request.query_params.get("tags")
    #     type = self.request.query_params.get("type")
    #     belong = self.request.query_params.get("belong")
    #     if tags:
    #         return Blog.objects.filter(deleted__exact='0',tags=BlogTags.objects.filter(id=int(tags)).first(),show=True)
    #     if type:
    #         BlogItem = []
    #         Typ2Blogs = Typ2Blog.objects.filter(deleted__exact='0',typ=BlogType.objects.filter(id=int(type)).first())
    #         for t2b in Typ2Blogs:
    #             BlogItem.append(t2b.blog.id)

    #         return Blog.objects.filter(deleted__exact='0',id__in=BlogItem,show=True)
    #     if belong:
    #         if belong == 'my':
    #             return Blog.objects.filter(deleted__exact='0',created_by = self.request.user.extension)
    #     else:
    #         return Blog.objects.filter(deleted__exact='0',show=True)
    
#first
class BlogOptionViews(MyModelViewSet):

    # queryset = Blog.objects.filter(deleted__exact='0')
    serializer_class = BlogOptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    # search_fields = ['name',]
    def get_queryset(self, *args, **kwargs):
        tags = self.request.query_params.get("tags")
        type = self.request.query_params.get("type")
        belong = self.request.query_params.get("belong")
        if tags:
            return Blog.objects.filter(deleted__exact='0',tags=BlogTags.objects.filter(id=int(tags)).first(),show=True)
        if type:
            BlogItem = []
            Typ2Blogs = Typ2Blog.objects.filter(deleted__exact='0',typ=BlogType.objects.filter(id=int(type)).first())
            for t2b in Typ2Blogs:
                BlogItem.append(t2b.blog.id)

            return Blog.objects.filter(deleted__exact='0',id__in=BlogItem,show=True)
        if belong:
            if belong == 'my':
                return Blog.objects.filter(deleted__exact='0',created_by = self.request.user.extension)
        else:
            return Blog.objects.filter(deleted__exact='0',show=True)
    
#first
class BlogTypeViews(MyModelViewSet):

    queryset = BlogType.objects.filter(deleted__exact='0')
    serializer_class = BlogTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CommonPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    #search_fields = ['realname', 'user__username']
    
#first
class BlogTypeOptionViews(MyModelViewSet):

    queryset = BlogType.objects.filter(deleted__exact='0')
    serializer_class = BlogTypeOptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    # search_fields = ['name',]
    
#first
class Typ2BlogViews(MyModelViewSet):

    queryset = Typ2Blog.objects.filter(deleted__exact='0')
    serializer_class = Typ2BlogSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CommonPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    #search_fields = ['realname', 'user__username']
    
#first
class Typ2BlogOptionViews(MyModelViewSet):

    queryset = Typ2Blog.objects.filter(deleted__exact='0')
    serializer_class = Typ2BlogOptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    # search_fields = ['name',]
    
#first
class BlogTalkViews(MyModelViewSet):

    # queryset = BlogTalk.objects.filter(deleted__exact='0')
    serializer_class = BlogTalkSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CommonPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    #search_fields = ['realname', 'user__username']
    def get_queryset(self, *args, **kwargs):
        blog = self.request.query_params.get("blog")

        if blog:
            return BlogTalk.objects.filter(deleted__exact='0',blog=Blog.objects.filter(deleted__exact='0',id=blog).first())
        else:
            return BlogTalk.objects.filter(deleted__exact='0').filter(Q(created_by = self.request.user.extension) | Q(blog__created_by = self.request.user.extension))


    
#first
class BlogTalkOptionViews(MyModelViewSet):

    queryset = BlogTalk.objects.filter(deleted__exact='0')
    serializer_class = BlogTalkOptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    # search_fields = ['name',]
    
#tags
class BlogTagsViews(MyModelViewSet):

    queryset = BlogTags.objects.filter(deleted__exact='0')
    serializer_class = BlogTagsSerializer
    permission_classes = [permissions.IsAuthenticated]
    # pagination_class = CommonPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # filterset_fields = ['id','name']
    #search_fields = ['realname', 'user__username']
    
#tags
class BlogTagsOptionViews(MyModelViewSet):

    queryset = BlogTags.objects.filter(deleted__exact='0')
    serializer_class = BlogTagsOptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # filterset_fields = ['id','name']
    # search_fields = ['name',]
    
#帖子行程地点点赞收藏
class BlogPraiseViews(MyModelViewSet):

    queryset = BlogPraise.objects.filter(deleted__exact='0')
    serializer_class = BlogPraiseSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CommonPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # filterset_fields = ['id','name']
    #search_fields = ['realname', 'user__username']
    def destroy(self, request, *args, **kwargs):
        """
        销毁模型实例.
        """
        instance = self.get_object()
        # 永久删除
        self.perform_destroy(instance)
        context = {
            'code': status.HTTP_204_NO_CONTENT,
            'msg': '删除成功！',
            'data': ''
        }
        # 如果反馈“HTTP_204_NO_CONTENT”，会导致context中内容没有返回给浏览器
        return Response(context, status=status.HTTP_200_OK)
    
#帖子行程地点点赞收藏
class BlogPraiseOptionViews(MyModelViewSet):

    queryset = BlogPraise.objects.filter(deleted__exact='0')
    serializer_class = BlogPraiseOptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # filterset_fields = ['id','name']
    # search_fields = ['name',]
    
#帖子行程地点点赞收藏
class BlogCollectViews(MyModelViewSet):

    queryset = BlogCollect.objects.filter(deleted__exact='0')
    serializer_class = BlogCollectSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CommonPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # filterset_fields = ['id','name']
    #search_fields = ['realname', 'user__username']
    def destroy(self, request, *args, **kwargs):
        """
        销毁模型实例.
        """
        instance = self.get_object()
        # 永久删除
        self.perform_destroy(instance)
        context = {
            'code': status.HTTP_204_NO_CONTENT,
            'msg': '删除成功！',
            'data': ''
        }
        # 如果反馈“HTTP_204_NO_CONTENT”，会导致context中内容没有返回给浏览器
        return Response(context, status=status.HTTP_200_OK)
    
#帖子行程地点点赞收藏
class BlogCollectOptionViews(MyModelViewSet):

    queryset = BlogCollect.objects.filter(deleted__exact='0')
    serializer_class = BlogCollectOptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # filterset_fields = ['id','name']
    # search_fields = ['name',]
    