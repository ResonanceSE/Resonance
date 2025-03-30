"""
URL configuration for server project.
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
    register,
    login,
    logout,
    get_user,
    validate_password,
    validate_reset_token,
    update_profile,
    update_address,
    forgot_password,
    reset_password,
)
from .views import home_view, keep_alive
from .controller.admin_controller import (
    manage_staff,
    get_staff_list,
    get_admin_stats,
    manage_products,
    manage_orders,
    get_categories,
)
from .controller.customer_order_controller import (
    create_order,
    get_user_orders,
    get_order_details,
    process_payment,
    get_user_by_id,
)
from .controller.product_controller import (
    upload_product_image,
    delete_product_image,
    check_product_stock,
    get_recommended_products,
)

urlpatterns = [
    path("", home_view),
    path("keepalive/", keep_alive),
    # Product api urls
    path("api/products/", get_all_products, name="all-products"),
    path(
        "api/products/recommendations/",
        get_recommended_products,
        name="recommended-products",
    ),
    path(
        "api/products/check-stock/<int:id>/",
        check_product_stock,
        name="check-product-stock",
    ),
    path("api/products/filters/", get_product_filters, name="product-filters"),
    path("api/products/<str:category>/", get_product_by_category, name="category"),
    path("api/products/<int:id>/", get_product_detailed_single_route, name="product"),
    path(
        "api/products/<str:category>/<int:id>/",
        get_product_detailed,
        name="product-detail",
    ),
    # Auth api urls
    path("api/auth/register/", register, name="register"),
    path("api/auth/login/", login, name="login"),
    path("api/auth/logout/", logout, name="logout"),
    path("api/auth/user/", get_user, name="user"),
    path("api/auth/forgot-password/", forgot_password, name="forgot_password"),
    path("api/auth/reset-password/", reset_password, name="reset_password"),
    path(
        "api/auth/validate-password/",
        validate_password,
        name="validate_password",
    ),
    path(
        "api/auth/validate-reset-token/",
        validate_reset_token,
        name="validate_reset_token",
    ),
    # Staff api endpoints
    
    path("api/admin/staff/", get_staff_list, name="staff-list"),
    path(
        "api/admin/staff/<int:staff_id>/",
        manage_staff,
        name="staff-detail",
    ),
    path("api/staff/stats/", get_admin_stats, name="staff-stats"),
    path("api/staff/products/", manage_products, name="staff-products"),
    path(
        "api/staff/products/<int:product_id>/",
        manage_products,
        name="staff-product-detail",
    ),
    path("api/staff/orders/", manage_orders, name="staff-orders"),
    path(
        "api/staff/orders/<int:order_id>/",
        manage_orders,
        name="staff-order-detail",
    ),
    path(
        "api/staff/products/<int:product_id>/upload-image/",
        upload_product_image,
        name="upload-product-image",
    ),
    path(
        "api/staff/products/<int:product_id>/delete-image/",
        delete_product_image,
        name="delete-product-image",
    ),
    path(
        "api/user/get_user_by_id/<int:user_id>/", get_user_by_id, name="get-user-by-id"
    ),
    path("api/categories/", get_categories, name="categories"),
    path("api/orders/create/", create_order, name="create-order"),
    path("api/orders/", get_user_orders, name="user-orders"),
    path("api/orders/<int:order_id>/", get_order_details, name="order-details"),
    path("api/auth/update-profile/", update_profile, name="update_profile"),
    path("api/auth/update-address/", update_address, name="update_address"),
    path("api/orders/<int:order_id>/payment/", process_payment, name="process-payment"),
]
