import re
from rest_framework.exceptions import APIException


class Validator():

    def starts_with_letter(field, value):
        if re.compile("[a-zA-Z]+").match(value):
            return value
        else:
            raise APIException({
                "error": field + " Must start with a letter"
                })
