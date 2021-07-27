from django.urls import path
from project import views


urlpatterns = [
    path('', views.home, name = 'home'),
    path('viewer', views.viewer, name = 'viewer'),
    path('viewer/render/<str:uri_id>/', views.render_howto, name = 'render_howto'),
]
