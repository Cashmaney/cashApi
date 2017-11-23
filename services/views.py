import json
from django.http import HttpResponse

from oauth2_provider.contrib.rest_framework import OAuth2Authentication

from rest_framework import status, permissions, viewsets
from rest_framework.decorators import authentication_classes, permission_classes, api_view, detail_route
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView

from services.models import UploadModel
from services.serializers import ImageSerializer


@api_view(['GET'])
@authentication_classes([OAuth2Authentication])
@permission_classes([permissions.IsAuthenticated])
def user_profile(request):
    """
    Returns the data required by the app about the current user
    """
    user = request.user
    data = {'id': user.id, 'username': user.username, 'email': user.email}
    return HttpResponse(json.dumps(data))


class FileUpload(APIView):
    authentication_classes = (OAuth2Authentication, )
    permission_classes = (permissions.IsAuthenticated,)

    serializer_class = ImageSerializer
    parser_classes = (MultiPartParser, )

    # def get(self, request):
    #    documents_list = Document.objects.all()
    #    return render(self.request, 'file_upload.html', {'documents': documents_list})

    @staticmethod
    def post(request, filename):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            valid_data = serializer.validated_data.get('file')
            valid_data.name = filename + "." + valid_data.image.format.lower()
            UploadModel.objects.create(file=valid_data, user=request.user)
            # todo: replace with upload to s3

            response = HttpResponse(filename)
            response.status_code = status.HTTP_201_CREATED
            return response

        response = HttpResponse(filename)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return response


class ImageViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    authentication_classes = (OAuth2Authentication, )
    permission_classes = (permissions.IsAuthenticated, )

    serializer_class = ImageSerializer
    parser_classes = (MultiPartParser, )
    queryset = UploadModel.objects.all()

    def retrieve(self, request, *args, **kwargs):
        """
        Overrides the default behavior of retrieve in order to open and base64 encode the file that we want to send

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        queryset = self.get_queryset()
        query_filter = {'filename': self.kwargs.get('filename')}
        obj = get_object_or_404(queryset, **query_filter)

        self.check_object_permissions(self.request, obj)

        serializer = self.get_serializer(obj)

        response = HttpResponse(
            json.dumps({"file": self.base_64_encode(serializer.data.get('file')) }),
            content_type='image/png')
        response['Content-Disposition'] = 'attachment; filename=' + serializer.data.get('filename')

        return response

    def perform_create(self, serializer):
        """
        Overrides the default behavior of perform_create to .save the serializer

        :param serializer:
        :return:
        """
        #filename = self.kwargs.get('filename')
        serializer.save(user=self.request.user, filename=self.kwargs.get('filename'))

    @staticmethod
    def base_64_encode(fp):
        """
        Creates data URI scheme base64 string
        data:[<media type>][;base64],

        :param fp: path to file
        :return:
        """
        with open(fp, "rb") as image_file:
            import base64
            encoded_string = base64.b64encode(image_file.read())
        data_uri_str = "data:" + "image;base64," + encoded_string.decode("utf-8")
        return data_uri_str
