import json
from django.http import HttpResponse
from django.contrib.auth import login

from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework import status, permissions
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView

from social_django.utils import psa
from django.views.decorators.csrf import csrf_exempt
from app.models import UploadModel
from app.serializers import ImageSerializer

# from social_django.utils import load_strategy
# from app.apps import AppConfig
# from app.forms import UploadFileForm
# from google.oauth2 import id_token
# from google.auth.transport import requests
# from social_core.backends.oauth import BaseOAuth1, BaseOAuth2
# from social_core.backends.google import GooglePlusAuth
# from social_core.backends.utils import load_backends
# from io import BufferedWriter, FileIO
# import base64
# from django.shortcuts import redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import logout as auth_logout
# from django.conf import settings
# from django.http import HttpResponseBadRequest
# from .decorators import render_to
#
# def logout(request):
#     """Logs out user"""
#     auth_logout(request)
#     return redirect('/')
#
#
# @render_to('home.html')
# def home(request):
#     """Home view, displays login mechanism"""
#     if request.user.is_authenticated():
#         return redirect('done')
#
#
# @login_required
# @render_to('home.html')
# def done(request):
#     """Login complete view, displays user data"""
#     pass
#
#
# @render_to('home.html')
# def validation_sent(request):
#     """Email validation sent confirmation page"""
#     return {
#         'validation_sent': True,
#         'email': request.session.get('email_validation_address')
#     }
#
#
# @render_to('home.html')
# def require_email(request):
#     """Email required page"""
#     strategy = load_strategy()
#     partial_token = request.GET.get('partial_token')
#     partial = strategy.partial_load(partial_token)
#     return {
#         'email_required': True,
#         'partial_backend_name': partial.backend,
#         'partial_token': partial_token
#     }
#
#
# @psa('social:complete')
# def ajax_auth(request, backend):
#     """AJAX authentication endpoint"""
#     if isinstance(request.backend, BaseOAuth1):
#         token = {
#             'oauth_token': request.REQUEST.get('access_token'),
#             'oauth_token_secret': request.REQUEST.get('access_token_secret'),
#         }
#     elif isinstance(request.backend, BaseOAuth2):
#         token = request.REQUEST.get('access_token')
#     else:
#         return HttpResponseBadRequest('Wrong backend type')
#     user = request.backend.do_auth(token, ajax=True)
#
#     data = {'id': user.id, 'username': user.username}
#     return HttpResponse(json.dumps(data), mimetype='application/json')
#

# "     ""
#       Disabled.. this returns a SessionToken, we now use Oauth2 tokens, so we don't need this anymore
#       """
# @csrf_exempt
# @psa('social:complete')
# def register_by_access_token(request, backend):
#     # This view expects an access_token POST parameter, if it's needed,
#     # request.backend and request.strategy will be loaded with the current
#     # backend and strategy.
#     token = request.POST.get('access_token')
#     user = request.backend.do_auth(token)
#     if user:
#         login(request, user)
#         data = {'id': user.id, 'username': user.username}
#         return HttpResponse(json.dumps(data))
#     else:
#         return HttpResponse(status.HTTP_400_BAD_REQUEST)


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
