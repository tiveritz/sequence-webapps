from django.urls import path
from administration import views


urlpatterns = [
    path('', views.dashboard, name = 'dashboard'),
]
