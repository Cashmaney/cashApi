from django.test import TestCase
from django.test.client import RequestFactory, Client
from oauth2_provider.oauth2_validators import Application, AccessToken

from app.views import FileUpload
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
import io
from PIL import Image


class TestUploadCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.testuser = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret', is_active=True,
        is_staff=False)
        self.client = Client()
        self.func_under_test = FileUpload()

    @staticmethod
    def generate_photo_file():
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    @staticmethod
    def __create_authorization_header(token):
        return "Bearer {0}".format(token)

    def __create_token(self, user):

        self.app = Application.objects.create(
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
            redirect_uris='https://www.none.com/oauth2/callback',
            name='dummy',
            user=user
        )
        from datetime import timedelta
        from django.utils import timezone
        access_token = AccessToken.objects.create(
            user=user,
            scope='read write',
            expires=timezone.now() + timedelta(seconds=300),
            token='secret-access-token-key',
            application=self.app
        )
        return access_token

    @staticmethod
    def build_data(photo_in_bytes):
        """

        create data URI scheme data (see: https://en.wikipedia.org/wiki/Data_URI_scheme)

        data:[<media type>][;base64],

        :return:
        """
        import base64

        photo_file = base64.encodebytes(photo_in_bytes)
        data_uri_format = "data:image/png;base64," + photo_file.decode('ascii')
        return data_uri_format

    def test_details(self):
        """
        Method to test the uploading of an image file in base64 by a registered user.

        Flow: register test user
              log in the test user
              generate base64 file in the data URI format
              create POST request
              send POST request to the upload URL
              true if method returns HTTP_201, fail otherwise
        """
        response = self.client.login(username='jacob', password='top_secret')
        self.assertTrue(response)

        token = self.__create_authorization_header(self.__create_token(self.testuser))

        bytes_str = self.generate_photo_file().read()
        photo_file = self.build_data(bytes_str)

        data = {
            'file':photo_file
        }

        url = reverse('img_upload', args=[self.testuser.id])

        response = self.client.post(url, data, HTTP_AUTHORIZATION=token)

        self.assertEqual(response.status_code, 201)

