
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('anzuelo_main.urls')),  # Include the main app's URLs
]
