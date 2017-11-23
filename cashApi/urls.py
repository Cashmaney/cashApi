from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from services import views as app_views
from services.views import ImageViewSet

image_list = ImageViewSet.as_view({
     'get': 'list',
 })

image_detail = ImageViewSet.as_view({
    'get': 'retrieve',
    'post': 'create'
})

#router = DefaultRouter()
#router.register(r'images', app_views.ImageViewSet, 'image')

urlpatterns = [
    url(r'^admin/',
        admin.site.urls),
    url(r'^auth/', include('rest_framework_social_oauth2.urls')),
    url(r'^profile/', app_views.user_profile, name='user_profile'),
    url(r'^upload/(?P<filename>[^/]+)$', app_views.FileUpload.as_view(), name='img_upload'),
    url(r'^images/$', image_list, name='image_list'),
    url(r'^images/(?P<filename>[^/]+)$', image_detail, name='image_detail')

]
