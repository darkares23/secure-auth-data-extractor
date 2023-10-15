from django.urls import path

from auth_data_extractor.authentication.views.authenticate_provider import (
    authenticate_provider_get,
    authenticate_provider_post,
)
from auth_data_extractor.data_extractor.views.data_extractor_views import extract_data

urlpatterns = [
    path("authenticate/", authenticate_provider_get, name="authenticate_get"),
    path("authenticate/<str:provider>/", authenticate_provider_post, name="authenticate_post"),
    path("extract_data/", extract_data, name="extract_data"),
]
