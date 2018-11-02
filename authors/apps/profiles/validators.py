import re

from rest_framework import serializers


def is_profile_valid(self, bio, last_name, first_name):
    """This function contains the validations for the profile"""

    if re.compile('[!@#$%^&*:;?><.]').match(bio):
        raise serializers.ValidationError(
            {'bio': 'Please do not start your bio with a symbol and do not use only symbols.'}
        )

    if re.compile('[!@#$%^&*:;?><.]').match(first_name):
        raise serializers.ValidationError(
            {'last_name': 'Please do not start your last name with a symbol and do not use only symbols.'}
        )

    if re.compile('[!@#$%^&*:;?><.]').match(last_name):
        raise serializers.ValidationError(
            {'first_name': 'Please do not start your first name with a symbol and do not use only symbols.'}
        )
