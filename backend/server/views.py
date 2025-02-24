from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

def home_view(request):
    return JsonResponse({"message": "Django API is Running!"})

@api_view(["GET"])
def keep_alive(request):
    return JsonResponse({'message': 'Ping server!'})
