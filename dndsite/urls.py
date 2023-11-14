# dndsite/dndsite/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('dndapp/', include('dndapp.urls')),  # Include your app's URLs
    path('', include('dndapp.urls')),
    # ... other project-wide paths ...
]