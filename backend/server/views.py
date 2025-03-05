from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.conf import settings

def home_view(request):
    return JsonResponse({"message": f"Allowed origins: {', '.join(settings.CORS_ALLOWED_ORIGINS)}"})


@api_view(["GET"])
def keep_alive(request):
    return JsonResponse({"message": "Ping server!"})

@api_view(["GET"])
def debug_cors(request):
    print(f"Request origin: {request.headers.get('origin')}")
    print(f"CORS settings: {settings.CORS_ALLOWED_ORIGINS}")