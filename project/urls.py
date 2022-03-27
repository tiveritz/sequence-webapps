from django.urls import path
from project import views


urlpatterns = [
    path('', views.home, name = 'home'),
    path('viewer/', views.viewer, name = 'viewer'),
    path('viewer/<str:api_id>/', views.view_sequence, name = 'view-sequence'),
    path('viewer/<str:step_api_id>/', views.view_step, name = 'view-step'),
]
