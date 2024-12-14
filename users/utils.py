from .models import UserToken, Profile
import six
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        try:
            account = Profile.objects.get(user=user)
            is_verified = account.is_verified
        except ObjectDoesNotExist:
            is_verified = False  # Default to False if the profile does not exist
        return (six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(is_verified))

generate_token = TokenGenerator()

def generate_user_token(user):
    # Create a new token for the user
    user_token = UserToken.objects.create(user=user)
    return user_token.token
