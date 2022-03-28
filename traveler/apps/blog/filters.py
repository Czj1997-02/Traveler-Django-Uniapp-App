#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import django_filters
from django.db.models import Q
from django.db.models.query import QuerySet
from django.utils.timezone import now, localtime
from .models import *
from user.models import City,Follow
# 过滤器
# class XXXFilter(django_filters.rest_framework.FilterSet):
#     XXX = django_filters.CharFilter(help_text='XXX', method='filter_XXX')

#     def filter_XXX(self, queryset, name, value):
#         model = self.request.query_params['model']
#         return queryset.filter(deleted__exact='0').filter()

#     class Meta:
#         model = XXX
#         fields = ['XXX',]
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
    
class BlogFilter(django_filters.rest_framework.FilterSet):
    # 城市、类型、归属、状态
    # city = self.request.query_params.get("city")
    # typ = self.request.query_params.get("typ")
    # belong = self.request.query_params.get("belong")
    # show = follow、praise、collect
    
    # city = django_filters.CharFilter(help_text='城市', method='filter_city')
    tags = django_filters.CharFilter(help_text='类型', method='filter_tags')
    belong = django_filters.CharFilter(help_text='归属', method='filter_belong')
    show = django_filters.CharFilter(help_text='状态', method='filter_show')

    # def filter_city(self, queryset, name, value):
    #     # model = self.request.query_params['model']
    #     return queryset.filter(deleted__exact='0').filter(city=City.objects.filter(id=int(value)).first())
    def filter_tags(self, queryset, name, value):
        # model = self.request.query_params['model']
        if value == 'null':
            return queryset.filter(deleted__exact='0')
        else:
            return queryset.filter(deleted__exact='0').filter(tags=BlogTags.objects.filter(id=int(value)).first())
    def filter_belong(self, queryset, name, value):
        # model = self.request.query_params['model']
        # my私有 all所有 show公有
        if value == 'undefined':
            return queryset.filter(deleted__exact='0')
        else:
            if value == 'my':
                return queryset.filter(deleted__exact='0').filter(created_by = self.request.user.extension)
            elif value == 'show':
                return queryset.filter(deleted__exact='0').filter(show = True)
            elif  value == 'all':
                return queryset.filter(deleted__exact='0')
            else:
                return queryset.filter(deleted__exact='0')
        
    def filter_show(self, queryset, name, value):
        # model = self.request.query_params['model']
        # show = follow关注、praise赞过、collect收藏
        
        # 被关注人的具体id
        # follower = self.request.query_params['follower']
        # return queryset.filter(deleted__exact='0').filter(created_by = int(follower))
        if value == 'undefined':
            return queryset.filter(deleted__exact='0')
        else:
            if value == 'follow':
                # 获取关注列表
                follows = Follow.objects.filter(deleted__exact='0',created_by = self.request.user.extension)
                follow_ids = [self.request.user.extension.id,]
                for follow in follows:
                    follow_ids.append(follow.follow.id)
                return queryset.filter(deleted__exact='0').filter(created_by__id__in = follow_ids)
            
            elif value == 'praise':
                #获取点赞列表
                praises = BlogPraise.objects.filter(deleted__exact='0',created_by = self.request.user.extension)
                praises_ids = []
                for praise in praises:
                    praises_ids.append(praise.blog.id)
                return queryset.filter(deleted__exact='0').filter(id__in = praises_ids)
            
            elif value == 'collect':
                #获取点赞列表
                collects = BlogCollect.objects.filter(deleted__exact='0',created_by = self.request.user.extension)
                collects_ids = []
                for collect in collects:
                    collects_ids.append(collect.blog.id)
                return queryset.filter(deleted__exact='0').filter(id__in = collects_ids)
            else:    
                return queryset.filter(deleted__exact='0')
        # return queryset.filter(deleted__exact='0').filter()

    class Meta:
        model = Blog
        fields = ['tags','belong','show']
