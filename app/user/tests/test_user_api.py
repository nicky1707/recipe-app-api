"""Tests for the user api"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient  # Rest Test helper module for mock client.
from rest_framework import status  # Rest Test helper module for status code check.

CREATE_USER_URL = reverse("user:create")  # app_name:url_name returns url by name.
TOKEN_URL = reverse("user:token")  # get token from token url.


def create_user(**params):
    """Helper function to create new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public features of users API (public)"""

    def setUp(self):  # setup client
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            "email": "test@example.com",
            "password": "testpass123",
            "name": "Test Name",
        }
        res = self.client.post(CREATE_USER_URL, payload)  # create user

        self.assertEqual(
            res.status_code, status.HTTP_201_CREATED
        )  # check output return created success code.
        user = get_user_model().objects.get(email=payload["email"])  # get user from db
        self.assertTrue(
            user.check_password(payload["password"])
        )  # return true if matches with the password hash stored in the database.
        self.assertNotIn(
            "password", res.data
        )  # check password is not in response data.

    def test_user_with_email_exists_error(self):
        """Test creating a user that already exists fails"""
        payload = {
            "email": "test@example.com",
            "password": "testpass123",
            "name": "Test Name",
        }

        create_user(**payload)  # create user with payload.
        res = self.client.post(
            CREATE_USER_URL, payload
        )  # create again with existing credentials
        self.assertEqual(
            res.status_code, status.HTTP_400_BAD_REQUEST
        )  # check output return bad request code.

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = {"email": "test@example.com", "password": "pw", "name": "Test Name"}
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(
            res.status_code, status.HTTP_400_BAD_REQUEST
        )  # check output return bad request code.
        user_exists = get_user_model().objects.filter(email=payload["email"]).exists()
        self.assertFalse(user_exists)  # check user not exists

    def test_create_token_for_user(self):
        """Test that a token is generated for the user authentication"""
        # user_details = {
        #     "name": "Test Name",
        #     "email": "test@example.com",
        #     "password": "testpass123",
        # }
        create_user(email="test@example.com", password="testpass123")  # creates a user.
        # create_user(**user_details)  # create user with payload.

        payload = {"email":'test@example.com', "password":'testpass123'}  # payload with correct password.
        res = self.client.post(TOKEN_URL, payload)  # Get login token.

        self.assertIn("token", res.data)  # check token in response data.
        self.assertEqual(
            res.status_code, status.HTTP_200_OK
        )  # check output return success code.

    def test_create_token_bad_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email="test@example.com", password="testpass123")  # creates a user.

        payload = {
            "email": "test@example.com",
            "password": "wrong123",
        }  # payload with wrong password.
        res = self.client.post(TOKEN_URL, payload)  # Get login token.

        self.assertNotIn("token", res.data)  # check token not in response data.
        self.assertEqual(
            res.status_code, status.HTTP_400_BAD_REQUEST
        )  # check output return bad request code.

    def test_create_token_blank_password(self):
        """Test that token is not created if user doesn't exist"""
        payload = {
            "email": "test@example.com",
            "password": "",
        }  # payload with blank password.
        res = self.client.post(TOKEN_URL, payload)  # Get login token.

        self.assertNotIn("token", res.data)  # check token not in response data.
        self.assertEqual(
            res.status_code, status.HTTP_400_BAD_REQUEST
        )  # check output return bad request code.
