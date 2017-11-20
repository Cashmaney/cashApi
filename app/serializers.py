from rest_framework import serializers
from .models import UploadModel

class Base64ImageField(serializers.ImageField):
    """
    Handles data in the data URI scheme (see: https://en.wikipedia.org/wiki/Data_URI_scheme)
        e.g -- data:[<media type>][;base64],

    :param Description:
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.

    I.G: Adopted from:
    https://stackoverflow.com/questions/28036404/django-rest-framework-upload-image-the-submitted-data-was-not-a-file#28036805

    Another option was to download and import the django-extra-fields package, but this works as well

    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate a random file name:
            file_name = str(uuid.uuid4())[:12]
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    @staticmethod
    def get_file_extension(file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class ImageSerializer(serializers.HyperlinkedModelSerializer):

    file = Base64ImageField(
        max_length=None, use_url=False,
    )
    user = serializers.ReadOnlyField(source='user.username')
    filename = serializers.ReadOnlyField()

    class Meta:
        model = UploadModel
        fields = ('file', 'id', 'user', 'filename')