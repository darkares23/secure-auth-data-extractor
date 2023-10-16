from celery import shared_task

from .authentication.factories.authenticator_factory import AuthenticatorFactory
from .models import ExtractedData, User


@shared_task(bind=True)
def authenticate_and_create_user(self, serializer_data, provider):
    try:
        # Use the AuthenticatorFactory to authenticate the user with the provided token.
        authenticator = AuthenticatorFactory.create(provider)
        user_info = authenticator.authenticate(serializer_data["token"])

        # Check if user already exists, if not, create a new user.
        user, created = User.objects.get_or_create(email=user_info["email"])
        if created:
            user.name = user_info["name"]
            user.save()

        return user_info
    except Exception as e:
        # If there's an error, Celery can retry the task.
        raise self.retry(exc=e, max_retries=3)
