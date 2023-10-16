from django.conf import settings
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

from ..interfaces.authenticator_interface import AuthenticatorInterface


class GoogleAuthenticator(AuthenticatorInterface):
    def authenticate(self, token: str) -> dict:
        try:
            # Verify the token using Google's libraries
            idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), settings.GOOGLE_CLIENT_ID)

            # If verification is successful, return the user's information
            return {"name": idinfo["name"], "email": idinfo["email"]}

        except ValueError:
            # If there's any issue with the verification, raise an exception
            raise ValueError("Invalid or expired token")
