import jwt
import requests

from ..interfaces.authenticator_interface import AuthenticatorInterface


class GoogleAuthenticator(AuthenticatorInterface):
    GOOGLE_PUBLIC_KEYS_URL = "https://www.googleapis.com/oauth2/v3/certs"

    def authenticate(self, token: str) -> dict:
        # Fetch Google's public keys
        response = requests.get(self.GOOGLE_PUBLIC_KEYS_URL)
        jwks = response.json()

        # Verify the token. This will raise an error if the token is invalid.
        header = jwt.get_unverified_header(token)
        public_key = jwks[header["kid"]]
        payload = jwt.decode(token, public_key, algorithms=["RS256"], audience="YOUR_GOOGLE_CLIENT_ID")

        # Return user's information
        return {"name": payload["name"], "email": payload["email"]}
