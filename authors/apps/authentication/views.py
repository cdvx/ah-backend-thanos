from rest_framework import status
from django.core.mail import send_mail
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.exceptions import APIException
from rest_framework.views import APIView
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.conf import settings
from datetime import datetime, timedelta
import jwt
import re


from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer,
    UpdatePasswordSerializer,
    SendPasswordResetEmailSerializer
)
from .send_email_util import SendEmail

User = get_user_model()


class RegistrationAPIView(generics.CreateAPIView):
    """
    post:
    Register a user.
    """
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.get(email=user["email"])
        uid = force_text(urlsafe_base64_encode(user.email.encode("utf8")))
        activation_token = default_token_generator.make_token(user)
        self.email = user.email

        self.mail_subject = "Activate your Authors Haven account."
        self.message = """
            Hi {},
            Please click on the link to confirm your registration,
            {}://{}/api/user/activate/{}/{}""".format(user.username,
                                                      request.scheme,
                                                      request.get_host(),
                                                      uid,
                                                      activation_token)
        SendEmail.send_email(self, self.mail_subject, self.message, self.email)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.CreateAPIView):
    """
        post:
        Login a user.
    """
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't actually have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
#     permission_classes = (IsAuthenticated,)
#     renderer_classes = (UserJSONRenderer,)
#     serializer_class = UserSerializer

#     def retrieve(self, request, *args, **kwargs):
#         # There is nothing to validate or save here. Instead, we just want the
#         # serializer to handle turning our `User` object into something that
#         # can be JSONified and sent to the client.
#         serializer = self.serializer_class(request.user)

#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def update(self, request, *args, **kwargs):
#         serializer_data = request.data.get('user', {})

#         # Here is that serialize, validate, save pattern we talked about
#         # before.
#         serializer = self.serializer_class(
#             request.user, data=serializer_data, partial=True
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(serializer.data, status=status.HTTP_200_OK)


class AccountVerificationAPIView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)

    def get(self, request, uidb64, activation_token):
        try:
            email = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(email=email)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(
            user, activation_token):

            if user.is_verified == True:
                message = {
                    "message":
                    'Your account is already verified, Please login.'}
                return Response(message, status=status.HTTP_200_OK)
            user.is_verified = True
            user.save()
            message = {
                "message":
                'Email confirmed. Now you can login your account.'}
            return Response(message, status=status.HTTP_200_OK)

        return Response({"error": 'Activation link is invalid or expired !!'},
                        status=status.HTTP_400_BAD_REQUEST)


class SendEmailPasswordReset(generics.CreateAPIView):

    permission_classes = (AllowAny,)
    serializer_class = SendPasswordResetEmailSerializer

    def post(self, request):

        self.email = request.data.get('email')
        dt = datetime.now()+timedelta(days=1)
        reset_password_token = jwt.encode({'email': self.email, 'exp': int(
            dt.strftime('%s'))}, settings.SECRET_KEY, 'HS256').decode('utf-8')
        self.mail_subject = "Reset your password for your Authors Haven account."
        self.message = """
            Hi,
            Please click on the link to reset your password,
            {}://{}/api/user/reset_password/{}""".format(request.scheme,
                                                         request.get_host(),
                                                         reset_password_token)
        SendEmail.send_email(self, self.mail_subject, self.message, self.email)
        return Response({"message":
                         "We have sent you an email to reset your password",
                         'reset_password_token': reset_password_token},
                        status=status.HTTP_200_OK)


class ResetPassword(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    look_url_kwarg = 'reset_password_token'
    serializer_class = UpdatePasswordSerializer

    def put(self, request, *args, **kwargs):
        token = self.kwargs.get(self.look_url_kwarg)
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        print(new_password, confirm_password)
        if (new_password != confirm_password):
            raise APIException({"error": "The passwords do not match"})
        elif (
            re.compile(
                r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'
            ).search(new_password)
                is None):
            raise APIException({"error":
                                "Ensure your password is alphanumeric, with Minimum eight characters, at least one letter, one number and one special character"}
                               )
        print(new_password, confirm_password)
        decode_token = jwt.decode(
            token, settings.SECRET_KEY, algorithms=['HS256'])
        user = User.objects.get(email=decode_token['email'])
        user.set_password(new_password)
        user.save()
        return Response({'message':
                         'your has successfully changed your password'},
                        status=status.HTTP_201_CREATED)
