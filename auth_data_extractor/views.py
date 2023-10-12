import logging

from authentication.factories.authenticator_factory import AuthenticatorFactory
from authentication.serializers.google_auth_serializer import GoogleAuthSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


class AuthenticateProvider(APIView):
    permission_classes = [AllowAny]

    @permission_classes([AllowAny])
    def get(self, request, provider):
        return Response({"message": "GET method response from AuthenticateProvider."}, status=status.HTTP_200_OK)

    def post(self, request, provider):
        serializer = GoogleAuthSerializer(data=request.data)
        logger.info(serializer.initial_data)

        if serializer.is_valid():
            print("Datos serializados:", serializer.data)
            try:
                authenticator = AuthenticatorFactory.create(provider)
                user_info = authenticator.authenticate(serializer.validated_data["token"])
                return Response(user_info, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            print("Errores del serializador:", serializer.errors) 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
