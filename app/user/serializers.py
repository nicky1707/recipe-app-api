"""
Serializers for the user API view
"""

from django.contrib.auth import get_user_model, authenticate  # User model.
from django.utils.translation import gettext as _
from rest_framework import serializers  # serializer class.


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()  # set model as user model.
        fields = ("email", "password", "name")  # fields to be serialized.
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}
        # write_only: True, password will be write only.

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token"""

    email = serializers.EmailField()  # email field.
    password = serializers.CharField(  # password field.
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    def validate(self, attrs):  # validate the email and password.
        """Validate and authenticate user"""
        email = attrs.get("emaail")
        password = attrs.get("password")
        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password,
        )
        if not user:  # if user is not authenticated.
            msg = _(
                "unable to authenticate with provided credentials"
            )  # error message.
            raise serializers.ValidationError(msg, code="authorization")  # raise error.

        attrs["user"] = user  # return user.

        return attrs
