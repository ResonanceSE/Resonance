"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from server.controller.product_controller import get_all_products, get_product_by_name
from .controller.auth_controller import (
    RegisterAPI,
    LoginAPI,
    LogoutAPI,
    UserAPI,
    ValidatePasswordAPI,
)
from .views import home_view, keep_alive

urlpatterns = [
    path("", home_view),
    path("keepalive/", keep_alive),
    path("admin/", admin.site.urls),
    path("api/products/", get_all_products, name="all-products"),
    path("api/products/<str:name>/", get_product_by_name, name="product-by-name"),
    # Auth api urls
    path("api/auth/register/", RegisterAPI.as_view()),
    path("api/auth/login/", LoginAPI.as_view()),
    path("api/auth/logout/", LogoutAPI.as_view()),
    path("api/auth/user/", UserAPI.as_view()),
    path(
        "api/auth/validate-password/",
        ValidatePasswordAPI.as_view(),
        name="validate_password",
    ),
]
