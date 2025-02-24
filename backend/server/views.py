from django.http import JsonResponse
from rest_framework.decorators import api_view


def home_view(request):
    return JsonResponse({"message": "Django API is Running!"})


@api_view(["GET"])
def keep_alive(request):
    return JsonResponse({"message": "Ping server!"})
