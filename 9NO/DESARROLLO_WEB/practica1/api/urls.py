from django.urls import path
from api.view import (
    BankCreateApiView,
    BankListApiView,
    BankDetailAPIView,
    BankUpdateApiView,
    BankDeleteApiView,
    UserCreateApiView,
    UserListApiView,
    UserDetailApiView,
    UserUpdateApiView,
    UserDeleteApiView,
)

urlpatterns = [
    # Bank
    path('bank/create/', BankCreateApiView.as_view(), name='bank-create'),
    path('bank/list/', BankListApiView.as_view(), name='bank-list'),
    path('bank/detail/<int:pk>/', BankDetailAPIView.as_view(), name='bank-detail'),
    path('bank/update/<int:pk>/', BankUpdateApiView.as_view(), name='bank-update'),
    path('bank/delete/<int:pk>/', BankDeleteApiView.as_view(), name='bank-delete'),

    # User
    path('user/create/', UserCreateApiView.as_view(), name='user-create'),
    path('user/list/', UserListApiView.as_view(), name='user-list'),
    path('user/detail/<int:pk>/', UserDetailApiView.as_view(), name='user-detail'),
    path('user/update/<int:pk>/', UserUpdateApiView.as_view(), name='user-update'),
    path('user/delete/<int:pk>/', UserDeleteApiView.as_view(), name='user-delete'),
]
