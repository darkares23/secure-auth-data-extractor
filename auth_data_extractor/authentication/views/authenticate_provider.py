from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_data_extractor.authentication.factories.authenticator_factory import (
    AuthenticatorFactory,
)
from auth_data_extractor.authentication.serializers.google_auth_serializer import (
    GoogleAuthSerializer,
)


class AuthenticateProvider(APIView):
    def ge(self, request, provider):
        return Response({"detail": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, provider):
        serializer = GoogleAuthSerializer(data=request.data)

        if serializer.is_valid():
            try:
                authenticator = AuthenticatorFactory.create(provider)
                user_info = authenticator.authenticate(serializer.validated_data["token"])
                return Response(user_info, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
