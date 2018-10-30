from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()
signup_url = reverse("authentication:signup")
login_url = reverse("authentication:login")

class UserApiTestCase(APITestCase):
    def setUp(self):

        self.signup_data = {
            "user": {
                "email": "judeinno@test.com",
                "username": "judeinno",
                "password": "testpassword#123",
            }
        }
        self.login_data = {
            "user": {
                "email": "judeinno@test.com",
                "password": "testpassword#123",
            }
        }
    
    def test_login_user(self):
        # Register User
        self.response = self.client.post(signup_url, self.signup_data, format="json")

        #  Verify user account
        user = User.objects.get(email=self.login_data["user"]["email"])
        uid = force_text(urlsafe_base64_encode(user.email.encode("utf8")))
        activation_token = default_token_generator.make_token(user)
        url = reverse("authentication:activate_account", args=(uid, activation_token,))
        self.client.get(url, format="json")

        # Test user login
        self.login_response = self.client.post(login_url, self.login_data, format="json")
        self.assertEqual(self.login_response.status_code, status.HTTP_200_OK)
        login_token = self.login_response.data['token']
        self.assertEqual(
            self.login_response.data, {"email": "judeinno@test.com", "username": "judeinno",  
            "token" : login_token}
        )
