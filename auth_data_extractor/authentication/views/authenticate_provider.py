import logging

from rest_framework import status
from rest_framework.response import Response

from auth_data_extractor.authentication.factories.authenticator_factory import (
    AuthenticatorFactory,
)
from auth_data_extractor.authentication.serializers.google_auth_serializer import (
    GoogleAuthSerializer,
)
from auth_data_extractor.models import User

logger = logging.getLogger(__name__)

from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


@api_view(["GET"])
@permission_classes([AllowAny])
def authenticate_provider_get(request, *args, **kwargs):
    return Response({"message": "GET method response from AuthenticateProvider."})


@extend_schema(request=GoogleAuthSerializer)
@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def authenticate_provider_post(request, provider):
    """
    Handle authentication based on the provided provider (e.g., Google).

    Args:
        request (HttpRequest): The HTTP request object.
        provider (str): The name of the authentication provider (e.g., 'google').

    Returns:
        Response: A DRF Response object containing user information on successful authentication,
                  or an error message on failure.

    Notes:
        - This view expects a POST request with a serialized token for the specified provider.
        - The authentication process uses the `AuthenticatorFactory` to create an appropriate
          authenticator for the given provider.
    """
    serializer = GoogleAuthSerializer(data=request.data)
    logger.info(serializer.initial_data)

    if serializer.is_valid():
        try:
            authenticator = AuthenticatorFactory.create(provider)
            user_info = authenticator.authenticate(serializer.validated_data["token"])
            user, created = User.objects.get_or_create(email=user_info["email"])
            if created:
                user.name = user_info["name"]
                user.save()

            return Response(user_info, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
