#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import django_filters
from django.db.models import Q
from django.db.models.query import QuerySet
from django.utils.timezone import now, localtime
from .models import *

# 过滤器
# class XXXFilter(django_filters.rest_framework.FilterSet):
#     XXX = django_filters.CharFilter(help_text='XXX', method='filter_XXX')

#     def filter_XXX(self, queryset, name, value):
#         model = self.request.query_params['model']
#         return queryset.filter(deleted__exact='0').filter()

#     class Meta:
#         model = XXX
#         fields = ['XXX',]
