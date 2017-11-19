import json
from django.http import HttpResponse

from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework import status, permissions
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView

from app.models import UploadModel
from app.serializers import ImageSerializer


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
