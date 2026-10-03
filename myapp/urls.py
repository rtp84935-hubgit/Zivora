"""
URL configuration for sample2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import include, path
from django.conf.urls.static import static
from myapp import views
from sample2 import settings

urlpatterns = [
    path('login/',views.login_load),
    path('signup/',views.signup),
    path('signupost/',views.signupost),
    path('seller_signup/',views.seller_signup),
    path('seller_signup_post/',views.seller_signup_post),
    path('home/',views.home),
    path('view_profile/',views.view_profile),
    path('edit_profile/<id>/',views.edit_profile),
    path('edit_profile_post/',views.edit_profile_post),
    path('change_password/',views.change_password),
    path('change_password_post/',views.change_password_post),
    path('seller_home/',views.seller_home),
    path('add_products/',views.add_products),
    path('add_product_post/',views.add_product_post),
    path('view_products/',views.view_products),
    path('edit_product/<id>',views.edit_product),
    path('edit_product_post/',views.edit_product_post),
    path('delete_product/<id>',views.delete_product),
    path('view_seller_profile/',views.view_seller_profile),
    path('seller_edit_profile/<id>/',views.seller_edit_profile),
    path('seller_edit_profile_post/',views.seller_edit_profile_post),
    path('view_user_products/',views.view_user_products),
    path('view_cart/',views.view_cart),
    path('addtocartget/<id>',views.addtocartget),
    path('AddtoCart_post/',views.AddtoCart_post),
    path('remove_cart/<id>',views.remove_cart),
    path('buyproduct/<int:id>/<int:pid>/<int:amount>/<int:quantity>/',views.buyproduct),
    path('buy_product_user/<int:pid>/<int:amount>/<int:quantity>/',views.buy_product_user),
    path('view_OrderDetails/',views.view_OrderDetails),
    path('logout/',views.logout_function),
    path('purchase/<id>',views.purchase),
    path('direct_buy/<id>',views.direct_buy),
    path('add_feedback/<id>',views.add_feedback),
    path('add_feedback_product/<id>',views.add_feedback_product),
    path('add_feedback_product_post/',views.add_feedback_product_post),
    path('add_feedback_post/',views.add_feedback_post),
    path('Return_Order/<id>',views.Return_Order),
    path('Return_Order_post/',views.Return_Order_post),
    path('seller_return/',views.seller_return),
    path('delete_return/<id>',views.delete_return),
    path('delete_all_return/',views.delete_all_return),
    path('accept/<id>/', views.accept),
    path('reject/<id>/', views.reject),
    path('view_return/',views.view_return),
    path('view_used_products/',views.view_used_products),
    path('manage_myproduct/',views.manage_myproduct),
    path('add_myproducts/',views.add_myproducts),
    path('add_myproducts_post/',views.add_myproducts_post),
    path('view_myproducts/',views.view_myproducts),
    path('delete_myproduct/<id>',views.delete_myproduct),
    path('view_others_products/',views.view_others_products),
    path('send_request/<id>',views.send_request),
    path('view_request/',views.view_request),
    path('accept_request/<id>',views.accept_request),
    path('reject_request/<id>',views.reject_request),
    path('view_used_purchase_status/',views.view_used_purchase_status),
    path('view_contacts/',views.view_contacts),
    path('add_offers/<id>',views.add_offers),
    path('add_offers_post/',views.add_offers_post),
    path('change_offers/<id>',views.change_offers),
    path('change_offer_post/',views.change_offer_post),
    path('view_seller_order_details/',views.view_seller_order_details),
    path('total_buy/',views.total_buy),
    path('useremailcheck/',views.useremailcheck),
    # path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-users/', views.admin_users, name='admin_users'),
    path('admin-user-view/<int:id>/', views.admin_user_view, name='admin_user_view'),
    path('admin-ban-user/<int:id>/', views.admin_ban_user, name='admin_ban_user'),
    path('admin-unban-user/<int:id>/', views.admin_unban_user, name='admin_unban_user'),
    path('admin-sellers/', views.admin_sellers, name='admin_sellers'),
    path('admin-seller-view/<int:id>/', views.admin_seller_view, name='admin_seller_view'),
    path('admin-verify-seller/<int:id>/', views.admin_verify_seller, name='admin_verify_seller'),
    path('admin-reject-seller/<int:id>/', views.admin_reject_seller, name='admin_reject_seller'),
    path('admin-ban-seller/<int:id>/', views.admin_ban_seller, name='admin_ban_seller'),
    path('admin-unban-seller/<int:id>/', views.admin_unban_seller, name='admin_unban_seller'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
]