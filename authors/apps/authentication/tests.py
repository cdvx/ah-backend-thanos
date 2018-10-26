from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model


User = get_user_model()
class UserApiTestCase(APITestCase):
    def setUp(self):
        user = User(username='testuser', email='test@test.com')
        user.set_password("testpassword")
        user.save()
       

    def test_single_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)