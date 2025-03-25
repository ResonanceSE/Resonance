from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.conf import settings


def home_view(request):
    return JsonResponse(
        {"message": f"Allowed origins: {', '.join(settings.ALLOWED_HOSTS)}"}
    )


@api_view(["GET"])
def keep_alive(request):
    return JsonResponse({"message": "Ping server!"})
#settings.CORS_ALLOWED_ORIGINS,