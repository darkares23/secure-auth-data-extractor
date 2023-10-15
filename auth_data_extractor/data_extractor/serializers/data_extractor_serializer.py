from rest_framework import serializers


class DataExtractorSerializer(serializers.Serializer):
    text = serializers.CharField(help_text="The text to be processed for data extraction.")
    email = serializers.EmailField(help_text="The email of the user who submitted the text.")
    start_date = serializers.DateField(required=False, help_text="The start date extracted from the text.")
    end_date = serializers.DateField(required=False, help_text="The end date extracted from the text.")
    min_percent = serializers.CharField(required=False, help_text="The minimum percentage extracted from the text.")
    max_percent = serializers.CharField(required=False, help_text="The maximum percentage extracted from the text.")
    max_amount = serializers.CharField(required=False, help_text="The maximum amount extracted from the text.")
