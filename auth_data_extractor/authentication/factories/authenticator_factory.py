from ..providers.google_authenticator import GoogleAuthenticator


class AuthenticatorFactory:
    @staticmethod
    def create(provider: str):
        if provider == "google":
            return GoogleAuthenticator()
        raise ValueError(f"Unknown provider: {provider}")
