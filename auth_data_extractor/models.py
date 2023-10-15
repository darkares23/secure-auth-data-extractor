import re

import bleach
from django.core.validators import EmailValidator
from django.db import models
from django.forms import ValidationError
from encrypted_model_fields.fields import EncryptedTextField


class TimestampedModel(models.Model):
    """
    ABSTRACT MODEL TO PROVIDE TIMESTAMP: created_at y updated_at.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(TimestampedModel):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)

    def clean(self):
        # Sanitize name
        if self.name:
            self.name = bleach.clean(self.name, strip=True)

        # Sanitize email
        if self.email:
            self.email = bleach.clean(self.email, strip=True)

            # Validate email format using Django's built-in EmailValidator
            email_validator = EmailValidator()
            try:
                email_validator(self.email)
            except ValidationError:
                raise ValidationError("Invalid email format")


class UserAuthentication(TimestampedModel):
    PROVIDER_CHOICES = [
        ("google", "Google"),
        # ... other providers
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES)
    token = models.TextField()  # In case we want to handle the token

    class Meta:
        unique_together = ["user", "provider"]


class ExtractedData(TimestampedModel):
    INPUT_TYPE_CHOICES = [
        ("initial_contribution_periods", "Initial Contribution Periods"),
        ("offering_period", "Offering Period"),
        ("successive_offering_periods", "Successive Offering Periods"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = EncryptedTextField()
    input_type = models.CharField(max_length=30, choices=INPUT_TYPE_CHOICES)

    def clean(self):
        # Delete html tags
        clean_data = re.sub("<.*?>", "", self.data)
        self.data = clean_data

        # validate imput
        valid_input_types = [choice[0] for choice in self.INPUT_TYPE_CHOICES]
        if self.input_type not in valid_input_types:
            raise ValidationError(f"Invalid input type: {self.input_type}")
