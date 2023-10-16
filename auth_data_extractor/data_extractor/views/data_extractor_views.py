import logging

from django.http import JsonResponse

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
    if request.method == "POST":
        text = request.data.get("text") if isinstance(request.data, dict) else request.POST.get("text")

        # Determine which strategy to use based on text content
        if "consecutive Contribution Periods" in text or "The first Contribution Period under this Plan" in text:
            extractor = InitialContributionPeriodExtractor()
        elif "Offering Period means" in text or "An eligible Employee may become" in text:
            extractor = OfferingPeriodExtractor()
        elif "The first Offering Period under the Plan" in text or "Successive Offering Periods" in text:
            extractor = SuccessiveOfferingPeriodExtractor()
        else:
            return JsonResponse({"error": "Unrecognized input format"}, status=400)

        try:
            # Extract data and return as JSON
            result = extractor.extract_data(text)

            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST method allowed"}, status=405)
