from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework import serializers
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response


from .models import Profile, User
from .serializers import ProfileSerializer
from .renderers import ProfileJSONRenderer


class ProfileRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    """Allow users  to retrieve and edit their profiles Params: username: A username is needed in order to get a specific profile.
     """
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer

    def retrieve(self, request, username, *args, **kwargs):

        user = get_object_or_404(User, username=username)

        serializer = self.serializer_class(user.profile)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, username, *args, **kwargs):

        serializer_data = request.data.get('profiles', {})
        user = get_object_or_404(User, username=username)

        serializer_data = {
            'first_name': serializer_data.get('first_name', request.user.profile.last_name),
            'last_name': serializer_data.get('last_name', request.user.profile.last_name),
            'bio': serializer_data.get('bio', request.user.profile.bio),
            'image': serializer_data.get('image', request.user.profile.image)
        }

        serializer = self.serializer_class(
            request.user.profile,
            data=serializer_data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.update(request.user.profile, serializer_data)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileListAPIView(ListAPIView):
    """Allow user to view other user profiles"""
    permission_classes = (IsAuthenticated, )
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
