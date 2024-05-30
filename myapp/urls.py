from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('firstjet/', include('firstjet.urls')),  # Remplacez 'your_app' par le nom de votre application
]
