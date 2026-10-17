# urls.py
from django.urls import path
from api import views

app_name = "api"

urlpatterns = [
    # Users URLs
    
    path("v1/user/create/", views.CreateUserAPIView.as_view(), name="user_create"),
    path("v1/users/list/", views.UserListAPIView.as_view(), name="users_list"),
    path("v1/user/detail/<int:pk>/", views.UserDetailAPIView.as_view(), name="user_detail"),

    # Banks URLs
    path("v1/bank/create/", views.BankCreateAPIView.as_view(), name="bank_create"),
    path("v1/banks/list/", views.BankListAPIView.as_view(), name="banks_list"),
    path("v1/bank/detail/<int:pk>/", views.BankDetailAPIView.as_view(), name="bank_detail"),
    path("v1/bank/update/<int:pk>/", views.BankUpdateAPIView.as_view(), name="bank_update"),
    path("v1/bank/delete/<int:pk>/", views.BankDeleteAPIView.as_view(), name="bank_delete"),
    
    # Account Urls
    path('v1/account/create/', views.AccountCreateAPIView.as_view(), name='account-create'),
    path('v1/accounts/list/', views.AccountListAPIView.as_view(), name='accounts-list'),
    path('v1/account/detail/<int:pk>/', views.AccountDetailAPIView.as_view(), name='account-detail'),
    path('v1/account/update/<int:pk>/', views.AccountUpdateAPIView.as_view(), name='account-update'),
    path('v1/account/delete/<int:pk>/', views.AccountDeleteAPIView.as_view(), name='account-delete'),

    # Provider Urls
    path('v1/provider/create/', views.ProviderCreateAPIView.as_view(), name='provider-create'),
    path('v1/providers/list/', views.ProviderListAPIView.as_view(), name='providers-list'),
    path('v1/provider/detail/<int:pk>/', views.ProviderDetailAPIView.as_view(), name='provider-detail'),
    path('v1/provider/update/<int:pk>/', views.ProviderUpdateAPIView.as_view(), name='provider-update'),
    path('v1/provider/delete/<int:pk>/', views.ProviderDeleteAPIView.as_view(), name='provider-delete'),

    # Payment Urls
    path('v1/payment/create/', views.PaymentCreateAPIView.as_view(), name='payment-create'),
    path('v1/payments/list/', views.PaymentListAPIView.as_view(), name='payments-list'),
    path('v1/payment/detail/<int:pk>/', views.PaymentDetailAPIView.as_view(), name='payment-detail'),
    path('v1/payment/update/<int:pk>/', views.PaymentUpdateAPIView.as_view(), name='payment-update'),
    path('v1/payment/delete/<int:pk>/', views.PaymentDeleteAPIView.as_view(), name='payment-delete'),

]