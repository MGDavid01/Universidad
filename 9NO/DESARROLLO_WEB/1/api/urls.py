from django.urls import path
from api.view import (
    BankCreateApiView,
    BankListApiView,
    BankDetailAPIView,
    BankUpdateApiView,
    BankDeleteApiView,
    AccountCreateApiView,
    AccountListApiView,
    AccountDetailApiView,
    AccountUpdateApiView,
    AccountDeleteApiView,
)

urlpatterns = [
    # Bank
    path('bank/create/', BankCreateApiView.as_view(), name='bank-create'),
    path('bank/list/', BankListApiView.as_view(), name='bank-list'),
    path('bank/detail/<int:pk>/', BankDetailAPIView.as_view(), name='bank-detail'),
    path('bank/update/<int:pk>/', BankUpdateApiView.as_view(), name='bank-update'),
    path('bank/delete/<int:pk>/', BankDeleteApiView.as_view(), name='bank-delete'),

    # Account
    path('account/create/', AccountCreateApiView.as_view(), name='account-create'),
    path('account/list/', AccountListApiView.as_view(), name='account-list'),
    path('account/detail/<int:pk>/', AccountDetailApiView.as_view(), name='account-detail'),
    path('account/update/<int:pk>/', AccountUpdateApiView.as_view(), name='account-update'),
    path('account/delete/<int:pk>/', AccountDeleteApiView.as_view(), name='account-delete'),
]
