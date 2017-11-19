from django.conf.urls import url, include
from django.contrib import admin

from app import views as app_views

urlpatterns = [
    # url(r'^$',
    #     app_views.home),
    url(r'^admin/',
        admin.site.urls),
    # url(r'^email-sent/',
    #     app_views.validation_sent),
    # url(r'^login/$',
    #     app_views.home),
    # url(r'^logout/$',
    #     app_views.logout),
    # url(r'^done/$',
    #     app_views.done, name='done'),
    # url(r'^ajax-auth/(?P<backend>[^/]+)/$',
    #     app_views.ajax_auth, name='ajax-auth'),
    # url(r'^email/$',
    #     app_views.require_email, name='require_email'),
    # url(r'^register-by-token/(?P<backend>[^/]+)/$',
    #     app_views.register_by_access_token, name='register_by_access_token'),
    #url(r'', include('social_django.urls')),
    url(r'^auth/', include('rest_framework_social_oauth2.urls')),
    url(r'^profile/', app_views.user_profile, name='user_profile'),
    url(r'^upload/(?P<filename>[^/]+)$', app_views.FileUpload.as_view(), name='img_upload')
]
