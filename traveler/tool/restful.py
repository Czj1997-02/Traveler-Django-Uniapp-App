from rest_framework import status
from rest_framework.response import Response


def result(code=status.HTTP_200_OK, msg='', data=None, kwargs=None):
    context = {
        'code': code,
        'msg': msg,
        'data': data
    }
    if kwargs and isinstance(kwargs, dict) and kwargs.keys():
        context.update(kwargs)
    return Response(context)


def success(msg='', data=None):
    """
    请求成功
    """
    return result(code=status.HTTP_200_OK, msg=msg, data=data)

def success_create(msg='', data=None):
    """
    成功创建
    """
    return result(code=status.HTTP_201_CREATED, msg=msg, data=data)

def params_error(msg='', data=None):
    """
    参数错误
    """
    return result(code=status.HTTP_400_BAD_REQUEST, msg=msg, data=data)


def unauthorized(msg='', data=None):
    """
    未授权
    """
    return result(code=status.HTTP_401_UNAUTHORIZED, msg=msg, data=data)


def method_error(msg='', data=None):
    """
    方法错误
    """
    return result(code=status.HTTP_405_METHOD_NOT_ALLOWED, msg=msg, data=data)


def server_error(msg='', data=None):
    """
    服务器错误
    """
    return result(code=status.HTTP_500_INTERNAL_SERVER_ERROR, msg=msg, data=data)
