from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse

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
        self.response = self.client.post(signup_url, self.signup_data, format="json")
        self.login_response = self.client.post(login_url, self.login_data, format="json")
        self.assertEqual(self.login_response.status_code, status.HTTP_200_OK)
        login_token = self.login_response.data['token']
        self.assertEqual(
            self.login_response.data, {"email": "judeinno@test.com", "username": "judeinno",  
            "token" : login_token}
        )
