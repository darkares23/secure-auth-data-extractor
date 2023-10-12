from django.urls import path

from auth_data_extractor.authentication.views.authenticate_provider import (
    AuthenticateProvider,
)

urlpatterns = [
    path("authenticate/", AuthenticateProvider.as_view(), name="authenticate"),
    path("authenticate/<str:provider>/", AuthenticateProvider.as_view(), name="authenticate_provider"),
]
