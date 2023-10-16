import logging

from django.http import JsonResponse

from auth_data_extractor.models import ExtractedData, User

logger = logging.getLogger(__name__)

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from auth_data_extractor.data_extractor.imput_extractor import (
    InitialContributionPeriodExtractor,
    OfferingPeriodExtractor,
    SuccessiveOfferingPeriodExtractor,
)
from auth_data_extractor.data_extractor.serializers.data_extractor_serializer import (
    DataExtractorSerializer,
)


@extend_schema(request=DataExtractorSerializer)
@api_view(["POST"])
@permission_classes([AllowAny])
def extract_data(request):
    """
    Extract data from the input text based on its type. The extracted data is then saved to the database.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: A JSON response containing the extracted data or an error message.
    """
    if request.method == "POST":
        text = request.data.get("text") if isinstance(request.data, dict) else request.POST.get("text")
        email = request.data.get("email", None)

        input_type = None

        # Determine the input type and corresponding extractor
        if "consecutive Contribution Periods" in text or "The first Contribution Period under this Plan" in text:
            extractor = InitialContributionPeriodExtractor()
            input_type = "initial_contribution_periods"
        elif "Offering Period means" in text or "An eligible Employee may become" in text:
            extractor = OfferingPeriodExtractor()
            input_type = "offering_period"
        elif "The first Offering Period under the Plan" in text or "Successive Offering Periods" in text:
            extractor = SuccessiveOfferingPeriodExtractor()
            input_type = "successive_offering_periods"
        else:
            return JsonResponse({"error": "Unrecognized input format"}, status=400)

        try:
            # Extract data from the input text
            result = extractor.extract_data(text)

            # Save the extracted information to the database
            user = User.objects.get(email=email)  # Ensure the user is authenticated
            ExtractedData.objects.create(user=user, data=result, input_type=input_type)

            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST method allowed"}, status=405)
