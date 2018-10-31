from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator


User = get_user_model()
class UserApiTestCase(APITestCase):
    def setUp(self):
        self.signup_data = {
            "user": {
                "email": "test@test.com",
                "username": "testuser",
                "password": "testpassword",
            }
        }
        self.login_data = {
            "user": {
                "email": "test@test.com",
                "password": "testpassword",
            }
        }
        url = reverse("authentication:signup")
        self.client.post(url, self.signup_data, format="json")
    
    def test_login_with_unverified_user(self):
        url = reverse("authentication:login")
        response = self.client.post(url, self.login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"errors": {"error": [
            "Your account is not verified, Please check your email to verify your account"
                ]
            }})

    def test_invalid_verification_link(self):
        uid = "c3VsYUBzdWxhLnN1bGE"
        activation_token = "50v-5be6aefa4ae337efe17b"
        url = reverse("authentication:activate_account", args=(uid, activation_token,))
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_correct_verification_link(self):
        user = User.objects.get(email=self.login_data["user"]["email"])
        uid = force_text(urlsafe_base64_encode(user.email.encode("utf8")))
        activation_token = default_token_generator.make_token(user)
        url = reverse("authentication:activate_account", args=(uid, activation_token,))
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verified_user(self):
        user = User.objects.get(email=self.login_data["user"]["email"])
        uid = force_text(urlsafe_base64_encode(user.email.encode("utf8")))
        activation_token = default_token_generator.make_token(user)
        url = reverse("authentication:activate_account", args=(uid, activation_token,))
        self.client.get(url, format="json")
        response = self.client.get(url, format="json")
        response_message={"message":'Your account is already verified, Please login.'}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, response_message)




