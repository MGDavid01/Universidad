from django.urls import path

from core import views

app_name = 'core'

urlpatterns = [
    path('list_bank/', views.ListBank.as_view(), name='list_bank'),
]