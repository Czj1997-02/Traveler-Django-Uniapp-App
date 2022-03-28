from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings


class MyCreateModelMixin:
    """
    Create a model instance.
    """
    def create(self, request, *args, **kwargs):
        """
        创建一个模型的实例.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        context = {
            'code': status.HTTP_201_CREATED,
            'msg': '创建成功！',
            'data': serializer.data
        }
        return Response(context, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class MyListModelMixin:
    """
    列出查询集
    """
    def list(self, request, *args, **kwargs):
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


class MyRetrieveModelMixin:
    """
    检索模型实例（详情页）。
    """
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        context = {
            'code': status.HTTP_200_OK,
            'msg': '查询成功！',
            'data': serializer.data
        }
        return Response(context)


class MyUpdateModelMixin:
    """
    Update a model instance.
    """
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
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

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class MyDestroyModelMixin:
    """
    Destroy a model instance.
    """
    def destroy(self, request, *args, **kwargs):
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

    def perform_destroy(self, instance):
        instance.delete()

    def _single_delete(self, instance):
        """假删除单个"""
        instance.deleted = 1
        instance.save()
        context = {
            'code': status.HTTP_204_NO_CONTENT,
            'msg': '删除成功！',
            'data': ''
        }
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
