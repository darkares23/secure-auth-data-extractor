from abc import ABC, abstractmethod


class AuthenticatorInterface(ABC):
    @abstractmethod
    def authenticate(self, token: str) -> dict:
        pass
