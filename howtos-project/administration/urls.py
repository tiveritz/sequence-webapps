from django.urls import path
from administration import views


urlpatterns = [
    path('', views.dashboard, name = 'dashboard'),
    path('dashboard/', views.dashboard, name = 'dashboard'),
    path('information/', views.information, name = 'information'),
    
    path('howtos/', views.howtos, name = 'howtos'),
    path('howtos/create/', views.howtos_create, name = 'howtos_create'),
    path('howtos/<str:id>/', views.howtos_edit, name = 'howtos_edit'),
    path('howtos/<str:id>/delete/', views.howtos_delete, name = 'howtos_delete'),
    path('howtos/<str:id>/delete/confirm/', views.howtos_delete_confirm, name = 'howtos_delete_confirm'),
    path('howtos/<str:id>/deletestep/<str:step_id>', views.howtos_delete_step, name = 'howtos_delete_step'),
    path('howtos/<str:id>/addstep/', views.howtos_add_step, name = 'howtos_add_step'),
    #path('howtos/<str:id>/addstep/<str:step_id>', views.howtos_add_step, name = 'howtos_add_step'),
    
    path('steps', views.steps, name = 'steps'),
    path('steps/create/', views.steps_create, name = 'steps_create'),
    path('steps/<str:id>/', views.steps_edit, name = 'steps_edit'),
    
    path('supersteps', views.supersteps, name = 'supersteps'),
    path('substeps', views.substeps, name = 'substeps'),

    #AJAX
    path('howtos/<str:id>/save-order', views.save_howto_order, name = 'save_howto_order'),
    path('steps/<str:id>/save-order', views.save_step_order, name = 'save_step_order'),
]
