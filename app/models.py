import os

from django.contrib.auth.models import User
from django.db import models

from app.apps import AppConfig
from cashApi import settings
from social_django.models import AbstractUserSocialAuth, DjangoStorage, USER_MODEL


def user_directory_path(self, generated_filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    user_directory = settings.MEDIA_ROOT + 'user_{0}'.format(self.user.id)

    gen_name, gen_ext = generated_filename.split('.')

    user_file = user_directory + '/{0}'.format(self.filename) + '.' + gen_ext
    if not os.path.exists(user_directory):
        os.makedirs(user_directory)
    return user_file


class UploadModel(models.Model):
    file_id = models.IntegerField(default='0')
    filename = models.CharField(max_length=100, blank=True, default='')
    file = models.ImageField(upload_to=user_directory_path)
    #file = models.ImageField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    #user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='documents')
    user = models.ForeignKey(User, related_name='upload_model_key', on_delete=models.CASCADE)


class CustomUserSocialAuth(AbstractUserSocialAuth):
    user = models.ForeignKey(USER_MODEL, related_name='custom_social_auth',
                             on_delete=models.CASCADE)


class CustomDjangoStorage(DjangoStorage):
    user = CustomUserSocialAuth

