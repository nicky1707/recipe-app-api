"""
Views for the User API
"""

from rest_framework import generics # generic class based view
from rest_framework.authtoken.views import ObtainAuthToken # obtain auth token
from rest_framework.settings import api_settings # api settings
from user.serializers import (
    UserSerializer, # user serializer
    AuthTokenSerializer
)

class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer # serializer class

class CreateTokenView(ObtainAuthToken): # inherit from ObtainAuthToken
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer # custom token serializer class.
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES # default renderer classes for browsable.

