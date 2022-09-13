"""
Test for django admin modifications.
"""

from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTest(TestCase):
    # Setup function to run before each test.
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com", password="test123"
        )
        self.client.force_login(self.admin_user)  # Force login as admin user.
        # Create a regular user.
        self.user = get_user_model().objects.create_user(
            email="user@example.com", password="test123", name="test user"
        )

    def test_users_list(self):
        """Test users are listed on admin page"""
        url = reverse("admin:core_user_changelist")  # URL for users list.
        res = self.client.get(url)  # Get the response.

        self.assertContains(
            res, self.user.name
        )  # Check if user name is in the response.
        self.assertContains(
            res, self.user.email
        )  # Check if user email is in the response.

    def test_edit_user_page(self):
        """Test Edit user page works"""
        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test create user page works"""

        url = reverse("admin:core_user_add")  # URL for create user page.
        res = self.client.get(url)  # Get the response.

        self.assertEqual(res.status_code, 200)  # Check if response is 200.
