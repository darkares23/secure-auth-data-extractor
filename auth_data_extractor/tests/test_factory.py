from unittest.mock import patch

from django.test import Client, TestCase
from django.urls import reverse

from auth_data_extractor.authentication.factories.authenticator_factory import (
    AuthenticatorFactory,
)
from auth_data_extractor.authentication.providers.google_authenticator import (
    GoogleAuthenticator,
)


class FunctionalTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_authenticate_get_route(self):
        response = self.client.get(reverse("authenticate_get"))
        # Check for expected status code or response content, etc.
        self.assertEqual(response.status_code, 200)

    @patch("google.oauth2.id_token.verify_oauth2_token")
    def test_authenticate_post_route(self, mock_verify):
        mock_payload = {"name": "Test User", "email": "testuser@example.com"}
        mock_verify.return_value = mock_payload

        data = {"token": "YOUR_TEST_TOKEN"}
        response = self.client.post(reverse("authenticate_post", args=["google"]), data)

        self.assertEqual(response.status_code, 200)

    def test_authenticator_factory_google(self):
        authenticator = AuthenticatorFactory.create("google")
        self.assertIsInstance(authenticator, GoogleAuthenticator)

    def test_authenticator_factory_invalid_provider(self):
        with self.assertRaises(ValueError) as context:
            AuthenticatorFactory.create("invalid_provider")
        self.assertEqual(str(context.exception), "Unknown provider: invalid_provider")

    @patch("google.oauth2.id_token.verify_oauth2_token")
    def test_google_authenticator_success(self, mock_verify):
        mock_payload = {"name": "Test User", "email": "testuser@example.com"}
        mock_verify.return_value = mock_payload

        authenticator = GoogleAuthenticator()
        result = authenticator.authenticate("VALID_TEST_TOKEN")
        self.assertIn("name", result)
        self.assertIn("email", result)
        self.assertEqual(result["name"], mock_payload["name"])
        self.assertEqual(result["email"], mock_payload["email"])

    def test_google_authenticator_failure(self):
        # Assuming you have an INVALID_TEST_TOKEN for testing purposes
        authenticator = GoogleAuthenticator()
        with self.assertRaises(ValueError) as context:
            authenticator.authenticate("INVALID_TEST_TOKEN")
        self.assertEqual(str(context.exception), "Invalid or expired token")
