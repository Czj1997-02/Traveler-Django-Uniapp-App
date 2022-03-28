"""traveler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls


from django.conf.urls.static import static
from traveler.settings import MEDIA_URL, MEDIA_ROOT

from user import views as UserViews
# from module import views as ModuleViews
from files import views as FilesViews
from blog import views as BlogViews
from deploy import views as DeployViews
from place import views as PlaceViews
# from team import views as TeamViews
from trip import views as TripViews

router = routers.DefaultRouter()
router.register(r'swiper',DeployViews.SwiperViews, basename='swiper')
router.register(r'notice',DeployViews.NoticeViews, basename='notice')

router.register(r'rc', UserViews.RegisterCodeViewSet, basename='rc')
router.register(r'register', UserViews.Register, basename='register')
router.register(r'fc', UserViews.ForgetCodeViewSet, basename='fc')
router.register(r'forget', UserViews.Forget, basename='forget')
router.register(r'code', UserViews.TelCodeViews, basename='code')
router.register(r'myself',UserViews.MySelf, basename='myself')
router.register(r'user-extension', UserViews.UserExtensionViews, basename='user-extension')
router.register(r'user-extension-option', UserViews.UserExtensionOptionViews, basename='user-extension-option')
router.register(r'portrait', UserViews.PortraitViews, basename='portrait')
router.register(r'follow', UserViews.FollowViews, basename='follow')
# router.register(r'', UserViews.PortraitOptionViews, basename='')

router.register(r'imgs', FilesViews.ImagesViews, basename='imgs')
# router.register(r'imgs-option', FilesViews.ImagesOptionViews, basename='imgs-option')
router.register(r'files', FilesViews.FilesViews, basename='files')
# router.register(r'files-option', FilesViews.FilesOptionViews, basename='files-option')

router.register(r'blog', BlogViews.BlogViews, basename='blog')
router.register(r'blog-option', BlogViews.BlogOptionViews, basename='blog-option')
router.register(r'blog-type', BlogViews.BlogTypeViews, basename='blog-type')
router.register(r'blog-type-option', BlogViews.BlogTypeOptionViews, basename='blog-type-option')
router.register(r'blog-tags', BlogViews.BlogTagsViews, basename='blog-tags')
router.register(r'blog-tags-option', BlogViews.BlogTagsOptionViews, basename='blog-tags-option')
router.register(r'type-blog', BlogViews.Typ2BlogViews, basename='type-blog')
router.register(r'type-blog-option', BlogViews.Typ2BlogOptionViews, basename='type-blog-option')
router.register(r'blog-talk', BlogViews.BlogTalkViews, basename='blog-talk')
router.register(r'blog-talk-option', BlogViews.BlogTalkOptionViews, basename='blog-talk-option')
router.register(r'blog-collect', BlogViews.BlogCollectViews, basename='blog-collect')
router.register(r'blog-praise', BlogViews.BlogPraiseViews, basename='blog-praise')

router.register(r'place', PlaceViews.PlaceViews, basename='place')
router.register(r'place-option', PlaceViews.PlaceOptionViews, basename='place-option')
router.register(r'place-type', PlaceViews.PlaceTypeViews, basename='place-type')
router.register(r'place-type-option', PlaceViews.PlaceTypeOptionViews, basename='place-type-option')
router.register(r'type-place', PlaceViews.Typ2PlaceViews, basename='type-place')
router.register(r'type-place-option', PlaceViews.Typ2PlaceOptionViews, basename='type-place-option')
router.register(r'place-talk', PlaceViews.PlaceTalkViews, basename='place-talk')
router.register(r'place-talk-option', PlaceViews.PlaceTalkOptionViews, basename='place-talk-option')
router.register(r'place-collect', PlaceViews.PlaceCollectViews, basename='place-collect')
router.register(r'place-praise', PlaceViews.PlacePraiseViews, basename='place-praise')

router.register(r'trip', TripViews.TripViews, basename='trip')
router.register(r'trip-option', TripViews.TripOptionViews, basename='trip-option')
router.register(r'trip-type', TripViews.TripTypeViews, basename='trip-type')
router.register(r'trip-type-option', TripViews.TripTypeOptionViews, basename='trip-type-option')
router.register(r'type-trip', TripViews.Typ2TripViews, basename='type-trip')
router.register(r'type-trip-option', TripViews.Typ2TripOptionViews, basename='type-trip-option')
router.register(r'trip-talk', TripViews.TripTalkViews, basename='trip-talk')
router.register(r'trip-talk-option', TripViews.TripTalkOptionViews, basename='trip-talk-option')
router.register(r'trip-collect', TripViews.TripCollectViews, basename='trip-collect')
router.register(r'trip-praise', TripViews.TripPraiseViews, basename='trip-praise')
router.register(r'place-in-trip', TripViews.PlacesInTripViews, basename='place-in-trip')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('docs/', include_docs_urls(title="Traveler接口文档")),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),  
    path(r'mdeditor/', include('mdeditor.urls')),
    path('login/', UserViews.Login.as_view(), name='my_token'),
    path('city-tree/', UserViews.CityTreeViewSet.as_view(), name='city_tree'),
    path('city-search/', UserViews.CitySearchViewSet.as_view(), name='city-search'),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
