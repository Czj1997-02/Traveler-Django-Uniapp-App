from PIL.Image import MIME
from django.shortcuts import render

# Create your views here.
import datetime

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User

from tool import restful
from rewrite.my_modelviewset import MyModelViewSet
from rewrite.my_mixins import MyListModelMixin, MyRetrieveModelMixin
from tool.paginations import CommonPagination
from tool.telcode import telcode

from .serializers import *
from django.http import request
from django.shortcuts import render
from django.utils.timezone import now


from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import permissions
from rest_framework import generics, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .filters import *
from rewrite.my_modelviewset import MyModelViewSet
from tool.paginations import CommonPagination
from tool import restful


# 登录
class Login(TokenObtainPairView):
    """
    获取Token
    """
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            # 如果验证错误，在这里中断了进程，如果要在验证错误时返回内容，需在Serializer重写is_valid
            serializer.is_valid(raise_exception=True)
            print(serializer)
            serializer.validated_data['code'] = status.HTTP_200_OK
            user = User.objects.filter(username=request.data['username']).first()
            data = {
                'token': serializer.validated_data['access'],
                'user_name': user.username,
                'user': user.id,
                'is_superuser': user.is_superuser,
                'email': user.email,
                'city':  user.extension.city.name,
                'perms': user.get_all_permissions()
            }
            return restful.success('登录成功！', data)
        except:
            return restful.unauthorized('账号或密码错误！')

# 发送注册验证码
class RegisterCodeViewSet(MyModelViewSet):
    serializer_class = TelCodeSerializer

    def get_queryset(self, *args, **kwargs):
        telephone = self.request.query_params.get("telephone")
        if telephone:
            return TelCode.objects.filter(telephone__exact=str(telephone))
        else:
            return TelCode.objects.filter(id=0)
    def create(self, request, *args, **kwargs):

        code = telcode(str(request.data['telephone']),'注册')
        if code == 'error':
            return restful.unauthorized('验证码获取异常')
        # print(code)
        # request.data['code'] = str(code)
        # data=request.POST
        # # 记住旧的方式
        # _mutable = data._mutable
        # # 设置_mutable为True
        # data._mutable = True
        # # 改变你想改变的数据
        # data['code'] = str(code)
        # # 恢复_mutable原来的属性
        # data._mutable = _mutable



        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer.instance.code = str(code)
        serializer.save()

        headers = self.get_success_headers(serializer.data)
        context = {
            'code': status.HTTP_201_CREATED,
            'msg': '创建成功！',
            'data': serializer.data
        }
        return Response(context, status=status.HTTP_201_CREATED, headers=headers)
# 注册
class Register(MyModelViewSet):
    """
    用户注册：最好添加邮箱认证或手机号认证
    """
    # queryset = User.objects.filter(id=0)
    serializer_class = RegisterSerializer

    def get_queryset(self, *args, **kwargs):
        # 注册时验证账号或电话是否存在，存在不允许注册
        username = self.request.query_params.get("username")
        telephone = self.request.query_params.get("telephone")
        if username:
            return User.objects.filter(username__exact=username)
        elif telephone:
            return User.objects.filter(extension__telephone__exact=str(telephone))
        else:
            return User.objects.filter(id=0)

    def create(self, request, *args, **kwargs):
        """
        创建一个模型的实例.
        """
        # print(request.data)
        Truecode = TelCode.objects.filter(telephone__exact=str(request.data['telephone']),code__exact=str(request.data['code']),created_date__gte=now() - datetime.timedelta(minutes=5)).first()
        if Truecode:
            hastel = User.objects.filter(extension__telephone__exact=str(request.data['telephone']))
            if hastel:
                return restful.unauthorized('手机号已存在，请直接登录')
            # print(Truecode)
            # return restful.unauthorized('验证码测试成功')
            else:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                password = request.data["password"]
                serializer.save()
                serializer.instance.set_password(password)

                if "username" in request.data:
                    serializer.instance.username = str(request.data["username"])
                if "first_name" in request.data:
                    serializer.instance.first_name = request.data["first_name"]
                if "last_name" in request.data:
                    serializer.instance.last_name = request.data["last_name"]
                if "is_staff" in request.data:
                    serializer.instance.is_staff = request.data["is_staff"]
                if "is_active" in request.data:
                    serializer.instance.is_active = request.data["is_active"]
                serializer.instance.save()

                if "realname" in request.data:
                    serializer.instance.extension.realname = request.data["realname"]
                    por = Portrait()
                    okpath = txt2pic(str(request.data["realname"]), r'media/img/portraits')
                    okpath = okpath.replace('media/', '')
                    por.portrait = okpath
                    por.save()
                    serializer.instance.extension.portrait = por
                if "desc" in request.data:
                    serializer.instance.extension.desc = request.data["desc"]
                if "sex" in request.data:
                    serializer.instance.extension.sex = request.data["sex"]
                if "telephone" in request.data:
                    serializer.instance.extension.telephone = request.data["telephone"]

                if "birthday" in request.data:
                    serializer.instance.extension.birthday = request.data["birthday"]
                if "projects" in request.data:
                    serializer.instance.extension.projects = request.data["projects"]
                if "modules" in request.data:
                    serializer.instance.extension.modules = request.data["modules"]
                serializer.instance.extension.city = City.objects.filter(id=1).first()
                serializer.instance.extension.save()
                

                serializer.save()
                headers = self.get_success_headers(serializer.data)
                context = {
                    'code': status.HTTP_201_CREATED,
                    'msg': '创建成功！',
                    'data': serializer.data
                }
                return Response(context, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return restful.unauthorized('验证码错误')

# 发送忘记密码验证码
class ForgetCodeViewSet(MyModelViewSet):
    serializer_class = TelCodeSerializer

    def get_queryset(self, *args, **kwargs):
        telephone = self.request.query_params.get("telephone")
        if telephone:
            return TelCode.objects.filter(telephone__exact=str(telephone))
        else:
            return TelCode.objects.filter(id=0)
    def create(self, request, *args, **kwargs):

        code = telcode(str(request.data['telephone']),'找回')
        if code == 'error':
            return restful.unauthorized('验证码获取异常')
        
        # request.data['code'] = str(code)
        # data=request.POST
        # # 记住旧的方式
        # _mutable = data._mutable
        # # 设置_mutable为True
        # data._mutable = True
        # # 改变你想改变的数据
        # data['code'] = str(code)
        # # 恢复_mutable原来的属性
        # data._mutable = _mutable

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer.instance.code = str(code)
        serializer.save()

        headers = self.get_success_headers(serializer.data)
        context = {
            'code': status.HTTP_201_CREATED,
            'msg': '创建成功！',
            'data': serializer.data
        }
        return Response(context, status=status.HTTP_201_CREATED, headers=headers)
# 忘记密码
class Forget(MyModelViewSet):
    # queryset = User.objects.filter(id=0)
    serializer_class = RegisterSerializer

    def get_queryset(self, *args, **kwargs):
        username = self.request.query_params.get("username")
        if username:
            return User.objects.filter(username__exact=username)
        else:
            return User.objects.filter(id=0)
    def create(self, request, *args, **kwargs):
        """
        更新一个模型的实例.
        """
        Truecode = TelCode.objects.filter(telephone__exact=str(request.data['telephone']),code__exact=str(request.data['code']),created_date__gte=now() - datetime.timedelta(minutes=5)).first()
        if Truecode:
            partial = kwargs.pop('partial', False)
            # instance = self.get_object()
            instance = User.objects.filter(extension__telephone__exact=str(request.data['telephone'])).first()
            
            if "password" in request.data:
                instance.set_password(request.data['password'])
                instance.save()

            serializer = self.get_serializer(
                instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            # serializer.validated_data['last_edited_by'] = request.user.extension
            # 密码
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            context = {
                'code': status.HTTP_200_OK,
                'msg': '账号' + str(instance.username) + '密码更新成功！',
                'data': serializer.data
            }

            return Response(context)
        else:
            return restful.unauthorized('验证码错误')
    def update(self, request, *args, **kwargs):
        """
        更新一个模型的实例.
        """
        Truecode = TelCode.objects.filter(telephone__exact=str(request.data['telephone']),code__exact=str(request.data['code']),created_date__gte=now() - datetime.timedelta(minutes=5)).first()
        if Truecode:
            # print('xxx')
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            instance = User.objects.filter(telephone__exact=str(request.data['telephone']))
            
            if "password" in request.data:
                instance.set_password(request.data['password'])
                instance.save()

            serializer = self.get_serializer(
                instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            # serializer.validated_data['last_edited_by'] = request.user.extension
            # 密码
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            context = {
                'code': status.HTTP_200_OK,
                'msg': '账号' + str(instance.username) + '密码更新成功！',
                'data': serializer.data
            }

            return Response(context)
        else:
            return restful.unauthorized('验证码错误')

#first
class TelCodeViews(MyModelViewSet):

    queryset = TelCode.objects.all()
    serializer_class = TelCodeSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CommonPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # filterset_fields = ['id','name']
    #search_fields = ['realname', 'user__username']
    
#first
class TelCodeOptionViews(MyModelViewSet):

    queryset = TelCode.objects.all()
    serializer_class = TelCodeOptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # filterset_fields = ['id','name']
    # search_fields = ['name',]
    
# 用户拓展
class UserExtensionViews(MyModelViewSet):
    """
    用户拓展信息列表<br>
    """
    queryset = UserExtension.objects.filter(user__is_active=True)
    serializer_class = UserExtensionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CommonPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id',]
    search_fields = ['realname', 'user__username']
# 用户拓展下拉选
class UserExtensionOptionViews(MyModelViewSet):

    queryset = UserExtension.objects.filter(user__is_active=True)
    serializer_class = UserExtensionOptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id','realname']
    search_fields = ['realname',]

class MySelf(MyModelViewSet):
    serializer_class = UserExtensionSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self, *args, **kwargs):
        return UserExtension.objects.filter(user__is_active=True,user=self.request.user)
    def update(self, request, *args, **kwargs):
        """
        更新一个模型的实例.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # 直接修改request.data,使用API提交时会报 AttributeError: This QueryDict instance is immutable错误
        # 为请求数据添加操作者和操作时间
        # request.data['user'] = request.user
        data=request.POST
        # 记住旧的方式
        _mutable = data._mutable
        # 设置_mutable为True
        data._mutable = True
        # 改变你想改变的数据
        data['user'] = request.user.pk
        # 恢复_mutable原来的属性
        data._mutable = _mutable

        # request.data['lastEditedDate'] = now()

        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        # serializer.validated_data['user'] = request.user
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
#first
class PortraitViews(MyModelViewSet):

    queryset = Portrait.objects.filter(deleted__exact='0')
    serializer_class = PortraitSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CommonPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id',]
    #search_fields = ['realname', 'user__username']
    
#first
class PortraitOptionViews(MyModelViewSet):

    queryset = Portrait.objects.filter(deleted__exact='0')
    serializer_class = PortraitOptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id',]
    # search_fields = ['name',]
    
#addcity
class CityViews(MyModelViewSet):

    # queryset = City.objects.filter(deleted__exact='0')
    serializer_class = CitySerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CommonPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # filterset_fields = ['id','name']
    #search_fields = ['realname', 'user__username']
    def get_queryset(self, *args, **kwargs):
        country = self.request.query_params.get("country")
        province = self.request.query_params.get("province")
        if country:
            return City.objects.filter(deleted__exact='0').filter(country=country)
        if province:
            return City.objects.filter(deleted__exact='0').filter(province=province)
        else:
            return City.objects.filter(deleted__exact='0')
    
#addcity
class CityOptionViews(MyModelViewSet):

    # queryset = City.objects.filter(deleted__exact='0')
    serializer_class = CityOptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # filterset_fields = ['id','name']
    # search_fields = ['name',]
    def get_queryset(self, *args, **kwargs):
        country = self.request.query_params.get("country")
        province = self.request.query_params.get("province")
        if country:
            return City.objects.filter(deleted__exact='0').filter(country=country)
        if province:
            return City.objects.filter(deleted__exact='0').filter(province=province)
        else:
            return City.objects.filter(deleted__exact='0')

# 城市树
class CityTreeViewSet(APIView):
    """
    城市树
    """
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, foramt=None):
        city_tree = []
        top_citys = City.objects.filter(deleted__exact='0', level__exact=1)
        for city in top_citys:
            city_json = self._get_city_data_child(city)
            city_tree.append(city_json)

        return restful.success('请求成功', data=city_tree)
    def _get_city_data_child(self, city):
        """
        获取所有部门的层级数据
        """
        city_json = {}
        city_json['value'] = city.id
        city_json['text'] = city.name
        children = City.objects.filter(deleted__exact='0', parent_id=city.id)
        if children:
            city_json['children'] = []
            for child in children:
                city_json['children'].append(self._get_city_data_child(child))
        return city_json
    
class CitySearchViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, foramt=None):
        city_tree = []
        top_citys = City.objects.filter(deleted__exact='0', level__exact=1)
        for city in top_citys:
            city_json = self._get_city_data_child(city)
            city_tree.append(city_json)

        return restful.success('请求成功', data=city_tree)
    def _get_city_data_child(self, city):
        """
        获取所有部门的层级数据
        """
        city_json = {}
        city_json['value'] = city.id
        city_json['name'] = city.name
        children = City.objects.filter(deleted__exact='0', parent_id=city.id)
        if children:
            city_json['submenu'] = []
            for child in children:
                city_json['submenu'].append(self._get_city_data_child(child))
        return city_json
#增加用户关注表
class FollowViews(MyModelViewSet):

    # queryset = Follow.objects.filter(deleted__exact='0')
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CommonPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id','follow']
    #search_fields = ['realname', 'user__username']
    def get_queryset(self, *args, **kwargs):
        return Follow.objects.filter(deleted__exact='0',created_by = self.request.user.extension)

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
    
#增加用户关注表
class FollowOptionViews(MyModelViewSet):

    # queryset = Follow.objects.filter(deleted__exact='0')
    serializer_class = FollowOptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id','follow']
    search_fields = ['follow',]
    
    def get_queryset(self, *args, **kwargs):
        return Follow.objects.filter(deleted__exact='0',created_by = self.request.user.extension)
    