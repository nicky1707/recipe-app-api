"""
urls mapping for the user api
"""

from django.urls import path
from user import views

app_name = "user"  # app name for reverse lookup

urlpatterns = [
    path("create/", views.CreateUserView.as_view(), name="create"),  # create user route.
    path("token/", views.CreateTokenView.as_view(), name="token"),  # create token route.
]
