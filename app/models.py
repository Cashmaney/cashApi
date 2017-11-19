import os

from django.contrib.auth.models import User
from django.db import models

from app.apps import AppConfig
from cashApi import settings
from social_django.models import AbstractUserSocialAuth, DjangoStorage, USER_MODEL

def user_directory_path(self, filename):
    dir_path = '/home/bob/IdeaProjects/cashApi/'
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    user_directory = dir_path + AppConfig.name + '/Storage/' + 'user_{0}'.format(self.user.id)
    user_file = user_directory + '/{0}'.format(filename)
    if not os.path.exists(user_directory):
        os.makedirs(user_directory)
    return user_file


class UploadModel(models.Model):
    file = models.ImageField(upload_to=user_directory_path)
    #file = models.ImageField()

    uploaded_at = models.DateTimeField(auto_now_add=True)
    #user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='documents')
    user = models.ForeignKey(User, related_name='upload_model_key')


class CustomUserSocialAuth(AbstractUserSocialAuth):
    user = models.ForeignKey(USER_MODEL, related_name='custom_social_auth',
                             on_delete=models.CASCADE)


class CustomDjangoStorage(DjangoStorage):
    user = CustomUserSocialAuth

