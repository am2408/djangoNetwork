from django.contrib import admin
from django.urls import path
from .views import apiTest

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', apiTest, name='api_test'),
    path('', apiTest, name='home'),  # Ajoutez ce chemin pour rediriger la racine vers apiTest
]