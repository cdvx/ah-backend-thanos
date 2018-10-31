from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse

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

