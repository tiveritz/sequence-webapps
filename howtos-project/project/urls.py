from django.urls import path
from project import views


urlpatterns = [
    path('', views.home, name = 'home'),
    path('viewer/', views.viewer, name = 'viewer'),
    path('viewer/<str:uri_id>/', views.view_howto, name = 'view-howto'),
    path('viewer/<str:howto_uri_id>/<str:step_uri_id>/<str:ref_id>/', views.view_step, name = 'view-step'),
]
