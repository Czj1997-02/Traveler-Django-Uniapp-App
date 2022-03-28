from django.http import request
from django.shortcuts import render
from django.utils.timezone import now

from django_filters.rest_framework import DjangoFilterBackend
# from files.models import Images
from rest_framework import permissions
from rest_framework import generics, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import filters
from rest_framework.response import Response
from django.db.models import Q
from .serializers import *
from .filters import *
from rewrite.my_modelviewset import MyModelViewSet
from tool.paginations import CommonPagination
from tool import restful
import requests
from urllib import parse
import json
# 解析高德短链接请求的经纬度坐标
def getdata(url):
    if url:
        url2 = requests.get(url).url
        data_1 = parse.urlparse(url2) 
        data_2 = data_1.query.split(',')
        data = {}
        data['list'] = []
        for i in data_2:
            try:
            # print(float(i))
                data['list'].append(float(i))
            except:
                pass
        print(data_2)
        if len(data_2) >=3:
            data['lat']=float(data_2[1])
            data['lng']=float(data_2[2])
        return data
    else:
        return []
#first
class PlaceViews(MyModelViewSet):

    # queryset = Place.objects.filter(deleted__exact='0')
    serializer_class = PlaceSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CommonPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    filter_class = PlaceFilter
    search_fields = ['name', 'desc']
    def get_queryset(self, *args, **kwargs):
        follower = self.request.query_params.get('follower')
        if follower:
            if int(follower) == self.request.user.extension.id:
                return Place.objects.filter(deleted__exact='0').filter(created_by = self.request.user.extension)
            else:
                return Place.objects.filter(deleted__exact='0').filter(created_by = int(follower),show = True)
        else:
            return Place.objects.filter(deleted__exact='0').filter(Q(created_by = self.request.user.extension) | Q(show = True))
    def create(self, request, *args, **kwargs):
        """
        创建一个模型的实例.
        """
        # 直接修改request.data,使用API提交时会报 AttributeError: This QueryDict instance is immutable错误
        # request.data['created_by'] = request.user.id
        # request.data['createdDate'] = now()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        img_list = ['img1','img2','img3','img4','img5','img6','img7','img8','img9']
        if 'imgs' in request.data :
            # 前端传过来的imgs是个字符串，把字符串切片处理成id数组
            imgs = request.data['imgs'].split(',')
            # 判断这个数组的长度
            if len(imgs) >= 1:
                for img_i in range(0,len(imgs)):
                    # 把对应ID的图片对象找出来填入
                    if imgs[img_i]:
                        serializer.validated_data[img_list[img_i]] = Images.objects.filter(id=int(imgs[img_i])).first()
        if 'gaode' in request.data:
            gaodeData = getdata(request.data['gaode'])
            if 'lat' in gaodeData and 'lng' in gaodeData:
                serializer.validated_data['lat'] = gaodeData['lat']
                serializer.validated_data['lng'] = gaodeData['lng']


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
class PlaceOptionViews(MyModelViewSet):

    # queryset = Place.objects.filter(deleted__exact='0')
    serializer_class = PlaceOptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    # search_fields = ['name',]
    def get_queryset(self, *args, **kwargs):
        typ = self.request.query_params.get("typ")
        type = self.request.query_params.get("type")
        belong = self.request.query_params.get("belong")

        if type:
            PlaceItem = []
            Typ2Places = Typ2Place.objects.filter(deleted__exact='0',typ=PlaceType.objects.filter(id=int(type)).first())
            for t2p in Typ2Places:
                PlaceItem.append(t2p.place.id)

            return Place.objects.filter(deleted__exact='0',id__in=PlaceItem,show=True)
        if typ:
            return Place.objects.filter(deleted__exact='0',typ=typ,show=True)
        if belong:
            if belong == 'my':
                return Place.objects.filter(deleted__exact='0',created_by = self.request.user.extension)
        else:
            return Place.objects.filter(deleted__exact='0',show=True)
    
#first
class PlaceTypeViews(MyModelViewSet):

    queryset = PlaceType.objects.filter(deleted__exact='0')
    serializer_class = PlaceTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CommonPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    #search_fields = ['realname', 'user__username']
    
#first
class PlaceTypeOptionViews(MyModelViewSet):

    queryset = PlaceType.objects.filter(deleted__exact='0')
    serializer_class = PlaceTypeOptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    # search_fields = ['name',]
    
#first
class Typ2PlaceViews(MyModelViewSet):

    queryset = Typ2Place.objects.filter(deleted__exact='0')
    serializer_class = Typ2PlaceSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CommonPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    #search_fields = ['realname', 'user__username']
    
#first
class Typ2PlaceOptionViews(MyModelViewSet):

    queryset = Typ2Place.objects.filter(deleted__exact='0')
    serializer_class = Typ2PlaceOptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    # search_fields = ['name',]
    
#first
class PlaceTalkViews(MyModelViewSet):

    # queryset = PlaceTalk.objects.filter(deleted__exact='0')
    serializer_class = PlaceTalkSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CommonPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    #search_fields = ['realname', 'user__username']
    def get_queryset(self, *args, **kwargs):
        place = self.request.query_params.get("place")

        if place:
            return PlaceTalk.objects.filter(deleted__exact='0',place=Place.objects.filter(deleted__exact='0',id=place).first())
        else:
            return PlaceTalk.objects.filter(deleted__exact='0').filter(Q(created_by = self.request.user.extension) | Q(place__created_by = self.request.user.extension))
    
#first
class PlaceTalkOptionViews(MyModelViewSet):

    queryset = PlaceTalk.objects.filter(deleted__exact='0')
    serializer_class = PlaceTalkOptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    # search_fields = ['name',]
    
#帖子行程地点点赞收藏
class PlacePraiseViews(MyModelViewSet):

    queryset = PlacePraise.objects.filter(deleted__exact='0')
    serializer_class = PlacePraiseSerializer
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
class PlacePraiseOptionViews(MyModelViewSet):

    queryset = PlacePraise.objects.filter(deleted__exact='0')
    serializer_class = PlacePraiseOptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # filterset_fields = ['id','name']
    # search_fields = ['name',]
    
#帖子行程地点点赞收藏
class PlaceCollectViews(MyModelViewSet):

    queryset = PlaceCollect.objects.filter(deleted__exact='0')
    serializer_class = PlaceCollectSerializer
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
class PlaceCollectOptionViews(MyModelViewSet):

    queryset = PlaceCollect.objects.filter(deleted__exact='0')
    serializer_class = PlaceCollectOptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # filterset_fields = ['id','name']
    # search_fields = ['name',]
    