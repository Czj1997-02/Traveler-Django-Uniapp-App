"""
重写ModelViewSet的部分方法，为响应数据添加'code'、'msg'两个字段，方便前端程序做相应处理。
"""
from django.utils.timezone import now

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response


class MyModelViewSet(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        """
        创建一个模型的实例.
        """
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

    def retrieve(self, request, *args, **kwargs):
        """
        检索一个模型的实例.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        context = {
            'code': status.HTTP_200_OK,
            'msg': '检索成功！',
            'data': serializer.data
        }
        return Response(context)

    def update(self, request, *args, **kwargs):
        """
        更新一个模型的实例.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # 直接修改request.data,使用API提交时会报 AttributeError: This QueryDict instance is immutable错误
        # 为请求数据添加操作者和操作时间
        # request.data['last_edited_by'] = request.user.id
        # request.data['lastEditedDate'] = now()

        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['last_edited_by'] = request.user.extension
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        context = {
            'code': status.HTTP_200_OK,
            'msg': '更新成功！',
            'data': serializer.data
        }

        return Response(context)

    def destroy(self, request, *args, **kwargs):
        """
        销毁模型实例.
        """
        typ = self.request.query_params.get('type')
        instance = self.get_object()

        if typ == 'real':
            return self._real_single_delete(instance)
        elif typ == 'batch':
            ids = self.request.data.get('ids')
            return self._batch_delete(instance, ids)
        elif typ == 'real_batch':
            ids = self.request.data.get('ids')
            return self._real_batch_delete(instance, ids)
        return self._single_delete(instance)
        
    def list(self, request, *args, **kwargs):
        """
        列出查询集.
        """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            context = {
                'code': status.HTTP_200_OK,
                'msg': '查询成功！',
                'data': serializer.data
            }
            return self.get_paginated_response(context)

        serializer = self.get_serializer(queryset, many=True)
        context = {
            'code': status.HTTP_200_OK,
            'msg': '查询成功！',
            'data': serializer.data
        }
        return Response(context)

    def _single_delete(self, instance):
        """假删除单个"""
        instance.deleted = 1
        instance.save()
        context = {
            'code': status.HTTP_204_NO_CONTENT,
            'msg': '删除成功！',
            'data': ''
        }
        # 如果反馈“HTTP_204_NO_CONTENT”，会导致context中内容没有返回给浏览器
        return Response(context, status=status.HTTP_200_OK)

    def _real_single_delete(self, instance):
        """真删除单个"""
        self.perform_destroy(instance)
        context = {
            'code': status.HTTP_204_NO_CONTENT,
            'msg': '删除成功！',
            'data': ''
        }
        return Response(context, status=status.HTTP_200_OK)

    def _batch_delete(self, instance, ids):
        """批量假删除"""
        model_name = instance.__class__.__name__
        eval(model_name).objects.filter(id__in=ids).update(deleted='1')
        context = {
            'code': status.HTTP_204_NO_CONTENT,
            'msg': '删除成功！',
            'data': ''
        }
        return Response(context, status=status.HTTP_200_OK)

    def _real_batch_delete(self, instance, ids):
        """批量真删除"""
        model_name = instance.__class__.__name__
        eval(model_name).objects.filter(id__in=ids).delete()
        context = {
            'code': status.HTTP_204_NO_CONTENT,
            'msg': '删除成功！',
            'data': ''
        }
        return Response(context, status=status.HTTP_200_OK)

