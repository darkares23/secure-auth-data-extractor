from django.http import JsonResponse
from django.shortcuts import render


def get(request):
    return JsonResponse({"message": "FUTURE HOME OF AWESOME THINGS"})
