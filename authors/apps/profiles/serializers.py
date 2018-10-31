from rest_framework import serializers

from .models import Profile
from.validators import is_profile_valid


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for creating a profile"""
    username = serializers.CharField(source='user.username')
    bio = serializers.CharField(allow_blank=True, required=False,
                                min_length=5,
                                max_length=255)
    first_name = serializers.CharField(allow_blank=True, required=False,
                                       min_length=2, max_length=50)
    last_name = serializers.CharField(allow_blank=True, required=False,
                                      min_length=2,
                                      max_length=50)

    def validate(self, data):
        bio = data.get('bio', None)
        first_name = data.get('first_name', None)
        last_name = data.get("last_name", None)

        validator = is_profile_valid(self, bio, first_name, last_name)
        return {'bio': bio, 'first_name': first_name, 'last_name': last_name}

    class Meta:
        model = Profile
        fields = ['username', 'bio', 'image', 'first_name',
                  'last_name', 'created_at', 'updated_at']

