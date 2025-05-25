from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('hello.urls')),  # Include app URLs without regex patterns
    # Remove any patterns that might be causing recursion
]