from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.permissions import AllowAny

class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]

def verify_token(uidb64, token):
    try:
        # Decode the uidb64 to get the user's ID
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    # If user is found and the token is valid, return the user
    if user is not None and default_token_generator.check_token(user, token):
        return user
    return None
