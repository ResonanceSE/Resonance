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

from django.urls import path
from server.controller.product_controller import (
    get_product_detailed_single_route,
    get_all_products,
    get_product_filters,
    get_product_by_category,
    get_product_detailed,
)
from .controller.auth_controller import (
    RegisterAPI,
    LoginAPI,
    LogoutAPI,
    UserAPI,
    ValidatePasswordAPI,
)
from .views import home_view, keep_alive
from .controller import admin_controller
from .controller.customer_order_controller import (
    create_order,
    get_user_orders,
    get_order_details,
    get_user_by_id,
)

urlpatterns = [
    path("", home_view),
    path("keepalive/", keep_alive),
    # Product api urls
    path("api/products/", get_all_products, name="all-products"),
    path("api/products/filters/", get_product_filters, name="product-filters"),
    path("api/products/<str:category>/", get_product_by_category, name="category"),
    path("api/products/<int:id>/", get_product_detailed_single_route, name="product"),
    path(
        "api/products/<str:category>/<int:id>/",
        get_product_detailed,
        name="product-detail",
    ),
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
    # Staff api endpoints
    path("api/staff/stats/", admin_controller.get_admin_stats, name="staff-stats"),
    path(
        "api/staff/products/", admin_controller.manage_products, name="staff-products"
    ),
    path(
        "api/staff/products/<int:product_id>/",
        admin_controller.manage_products,
        name="staff-product-detail",
    ),
    path("api/staff/orders/", admin_controller.manage_orders, name="staff-orders"),
    path(
        "api/staff/orders/<int:order_id>/",
        admin_controller.manage_orders,
        name="staff-order-detail",
    ),
    path(
        "api/user/get_user_by_id/<int:user_id>/", get_user_by_id, name="get-user-by-id"
    ),
    path("api/categories/", admin_controller.get_categories, name="categories"),
    path("api/orders/create/", create_order, name="create-order"),
    path("api/orders/", get_user_orders, name="user-orders"),
    path("api/orders/<int:order_id>/", get_order_details, name="order-details"),
]
