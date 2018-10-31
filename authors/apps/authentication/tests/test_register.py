from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse

from ...profiles.models import Profile

User = get_user_model()
signup_url = reverse("authentication:signup")


class UserApiTestCase(APITestCase):
    def setUp(self):
        self.user_data = {
            "user": {
                "email": "daniel@test.com",
                "username": "daniel",
                "password": "testpassword#123"
            }
        }
        self.invalid_email_data = {
            "user": {
                "email": "test@testcom",
                "username": "testuser",
                "password": "testpassword1"
            }
        }
        self.invalid_username = {
            "user": {
                "email": "test@test.com",
                "username": "<@#!$%^$^",
                "password": "testpassword"
            }
        }
        self.invalid_pass_data = {
            "user": {
                "email": "test@test.com",
                "username": "testuser",
                "password": "123345678"
            }
        }
        self.pass_less8_data = {
            "user": {
                "email": "test@test.com",
                "username": "testuser",
                "password": "12345l",
            }
        }
        self.alp_pass_data = {
            "user": {
                "username": "jude",
                "email": "jude@mail.com",
                "password": "judesecret"
            }
        }

        self.no_fields = {
            "user": {
                "username": "",
                "email": "",
                "password": "judesecret"
            }
        }
        self.profile_data = {
            "profiles": {
                "username": "bruce",
                "bio": "this is a test user",
                "image": "",
                "last_name": "",
                "first_name": ""
            }
        }

    def test_register_user(self):
        self.response = self.client.post(
            signup_url, self.user_data, format="json")
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_invalid_email(self):
        self.response = self.client.post(
            signup_url, self.invalid_email_data, format="json")
        self.assertEqual(self.response.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(["Enter a valid email address."],
                         self.response.data["errors"]["email"])

    def test_register_with_invalid_username(self):
        self.response = self.client.post(
            signup_url, self.invalid_username, format="json")
        self.assertEqual(self.response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_register_with_invalid_password_numbers_only(self):
        self.response = self.client.post(
            signup_url, self.invalid_pass_data, format="json")
        self.assertEqual(self.response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_password_length(self):
        self.response = self.client.post(
            signup_url, self.pass_less8_data, format="json")
        self.assertEqual(self.response.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            ["Ensure this field has at least 8 characters."],
            self.response.data["errors"]["password"],
        )

    def test_password_not_alphanumeric(self):
        self.response = self.client.post(
            signup_url, self.alp_pass_data, format="json")
        self.assertEqual(self.response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_user_has_filled_in_Fields(self):
        self.response = self.client.post(
            signup_url, self.no_fields, format="json")
        self.assertEqual(self.response.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertIn('This field may not be blank.',
                      self.response.data["errors"]["username"])

    def test_get_short_name(self):
        """ Test model method to get username """
        profile = Profile()
        self.user = User.objects.create_user(
            username="jude", email="jude@gmail.com", password="jude#1",
            profile=profile)
        short_name = self.user.get_short_name()
        self.assertEqual(short_name, "jude")

    def test_get_full_name(self):
        """ Test property to get username """
        profile = Profile()
        self.user = User.objects.create_user(
            username="jude", email="jude@gmail.com", password="jude#1",
            profile=profile)
        full_name = self.user.get_full_name
        self.assertEqual(full_name, "jude")

    def test_registration_of_super_user(self):
        """Test that user can be registered as a super user"""
        self.assertRaises(TypeError, lambda: User.objects.create_superuser(
            username="superuser",
            email="superuser@gmail.com", password=None))
