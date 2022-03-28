from django.http import request
from django.shortcuts import render
from django.utils.timezone import now
from django.db.models import Q
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

#first
class TripViews(MyModelViewSet):

    # queryset = Trip.objects.filter(deleted__exact='0')
    serializer_class = TripSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CommonPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    filter_class = TripFilter
    search_fields = ['name', 'desc']
    #search_fields = ['realname', 'user__username']
    def get_queryset(self, *args, **kwargs):
        follower = self.request.query_params.get('follower')
        if follower:
            if int(follower) == self.request.user.extension.id:
                return Trip.objects.filter(deleted__exact='0').filter(created_by = self.request.user.extension)
            else:
                return Trip.objects.filter(deleted__exact='0').filter(created_by = int(follower),show = True)
        else:
            return Trip.objects.filter(deleted__exact='0').filter(Q(created_by = self.request.user.extension) | Q(show = True))
    # def get_queryset(self, *args, **kwargs):
    
    #     type = self.request.query_params.get("type")
    #     belong = self.request.query_params.get("belong")

    #     if type:
    #         TripItem = []
    #         Typ2Trips = Typ2Trip.objects.filter(deleted__exact='0',typ=TripType.objects.filter(id=int(type)).first())
    #         for t2t in Typ2Trips:
    #             TripItem.append(t2t.trip.id)

    #         return Trip.objects.filter(deleted__exact='0',id__in=TripItem,show=True)
    #     if belong:
    #         if belong == 'my':
    #             return Trip.objects.filter(deleted__exact='0',created_by = self.request.user.extension)
    #     else:
    #         return Trip.objects.filter(deleted__exact='0',show=True)
    
#first
class TripOptionViews(MyModelViewSet):

    # queryset = Trip.objects.filter(deleted__exact='0')
    serializer_class = TripOptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    # search_fields = ['name',]
    search_fields = ['name', 'desc']
    def get_queryset(self, *args, **kwargs):

        type = self.request.query_params.get("type")
        belong = self.request.query_params.get("belong")

        if type:
            TripItem = []
            Typ2Trips = Typ2Trip.objects.filter(deleted__exact='0',typ=TripType.objects.filter(id=int(type)).first())
            for t2t in Typ2Trips:
                TripItem.append(t2t.trip.id)

            return Trip.objects.filter(deleted__exact='0',id__in=TripItem,show=True)
        if belong:
            if belong == 'my':
                return Trip.objects.filter(deleted__exact='0',created_by = self.request.user.extension)
        else:
            return Trip.objects.filter(deleted__exact='0',show=True)
    
#first
class TripTypeViews(MyModelViewSet):

    queryset = TripType.objects.filter(deleted__exact='0')
    serializer_class = TripTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CommonPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    #search_fields = ['realname', 'user__username']
    
#first
class TripTypeOptionViews(MyModelViewSet):

    queryset = TripType.objects.filter(deleted__exact='0')
    serializer_class = TripTypeOptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    # search_fields = ['name',]
    
#first
class Typ2TripViews(MyModelViewSet):

    queryset = Typ2Trip.objects.filter(deleted__exact='0')
    serializer_class = Typ2TripSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CommonPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    #search_fields = ['realname', 'user__username']
    
#first
class Typ2TripOptionViews(MyModelViewSet):

    queryset = Typ2Trip.objects.filter(deleted__exact='0')
    serializer_class = Typ2TripOptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    # search_fields = ['name',]
    
#first
class TripTalkViews(MyModelViewSet):

    # queryset = TripTalk.objects.filter(deleted__exact='0')
    serializer_class = TripTalkSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CommonPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    #search_fields = ['realname', 'user__username']
    def get_queryset(self, *args, **kwargs):
        trip = self.request.query_params.get("trip")

        if trip:
            return TripTalk.objects.filter(deleted__exact='0',trip=Trip.objects.filter(deleted__exact='0',id=trip).first())
        else:
            return TripTalk.objects.filter(deleted__exact='0').filter(Q(created_by = self.request.user.extension) | Q(trip__created_by = self.request.user.extension))
    
#first
class TripTalkOptionViews(MyModelViewSet):

    queryset = TripTalk.objects.filter(deleted__exact='0')
    serializer_class = TripTalkOptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    # search_fields = ['name',]
    
#帖子行程地点点赞收藏
class TripPraiseViews(MyModelViewSet):

    queryset = TripPraise.objects.filter(deleted__exact='0')
    serializer_class = TripPraiseSerializer
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
class TripPraiseOptionViews(MyModelViewSet):

    queryset = TripPraise.objects.filter(deleted__exact='0')
    serializer_class = TripPraiseOptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # filterset_fields = ['id','name']
    # search_fields = ['name',]
    
#帖子行程地点点赞收藏
class TripCollectViews(MyModelViewSet):

    queryset = TripCollect.objects.filter(deleted__exact='0')
    serializer_class = TripCollectSerializer
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
class TripCollectOptionViews(MyModelViewSet):

    queryset = TripCollect.objects.filter(deleted__exact='0')
    serializer_class = TripCollectOptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # filterset_fields = ['id','name']
    # search_fields = ['name',]
    
#增加行程地点明细
class PlacesInTripViews(MyModelViewSet):

    # queryset = PlacesInTrip.objects.filter(deleted__exact='0')
    serializer_class = PlacesInTripSerializer
    permission_classes = [permissions.IsAuthenticated]
    # pagination_class = CommonPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id','name']
    #search_fields = ['realname', 'user__username']
    def get_queryset(self, *args, **kwargs):

        trip = self.request.query_params.get("trip")
        if trip:
            return PlacesInTrip.objects.filter(deleted__exact='0',trip=Trip.objects.filter(id=int(trip)).first())
        else:
            return PlacesInTrip.objects.filter(deleted__exact='0')
    
    def destroy(self, request, *args, **kwargs):
        """
        销毁模型实例.
        """
        # typ = self.request.query_params.get('type')
        instance = self.get_object()

        places = PlacesInTrip.objects.filter(deleted__exact='0',trip = instance.trip)

        for place in places:
            # 所有后面的顺序前进一位
            if place.index > instance.index:
                place.index = place.index -1
                place.save()
                # print(place.index -1 )

        self.perform_destroy(instance)
        context = {
            'code': status.HTTP_204_NO_CONTENT,
            'msg': '删除成功！',
            'data': ''
        }
        return Response(context, status=status.HTTP_200_OK)
        

    
#增加行程地点明细
class PlacesInTripOptionViews(MyModelViewSet):

    queryset = PlacesInTrip.objects.filter(deleted__exact='0')
    serializer_class = PlacesInTripOptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id','name']
    search_fields = ['name',]
    