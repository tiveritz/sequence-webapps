from django.urls import path
from administration import views


urlpatterns = [
    path('', views.dashboard, name = 'dashboard'),
    path('dashboard/', views.dashboard, name = 'dashboard'),
    path('information/', views.information, name = 'information'),
    path('howtos/', views.howtos, name = 'howtos'),
    path('howtos/create/', views.howtos_create, name = 'howtos_create'),
    path('howtos/<str:uri_id>/', views.howtos_edit, name = 'howtos_edit'),
    path('steps', views.steps, name = 'steps'),
    path('steps/<str:uri_id>/', views.steps_edit, name = 'steps_edit'),
    
    #AJAX
    path('howtos/<str:uri_id>/save-order', views.save_howto_order, name = 'save_howto_order'),
]
