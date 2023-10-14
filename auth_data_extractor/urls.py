from django.urls import path

from auth_data_extractor.views import (
    authenticate_provider_get,
    authenticate_provider_post,
)

urlpatterns = [
    path("authenticate/", authenticate_provider_get, name="authenticate_get"),
    path("authenticate/<str:provider>/", authenticate_provider_post, name="authenticate_post"),
]
