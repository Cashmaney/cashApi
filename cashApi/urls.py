from django.conf.urls import url, include
from django.contrib import admin

from app import views as app_views

urlpatterns = [
    url(r'^admin/',
        admin.site.urls),
    url(r'^auth/', include('rest_framework_social_oauth2.urls')),
    url(r'^profile/', app_views.user_profile, name='user_profile'),
    url(r'^upload/(?P<filename>[^/]+)$', app_views.FileUpload.as_view(), name='img_upload')
]
