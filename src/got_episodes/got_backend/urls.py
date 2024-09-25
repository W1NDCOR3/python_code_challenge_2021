from django.contrib import admin
from django.urls import path, re_path
from django.http import HttpResponse

# Create a simple view for testing
def index(request):
    return HttpResponse("Welcome to Game of Thrones Episode API!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),  # Default landing page
]
