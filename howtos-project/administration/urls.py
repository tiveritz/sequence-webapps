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
    
    path('steps', views.steps, name = 'steps'),
    path('steps/create/', views.steps_create, name = 'steps_create'),
    path('steps/<str:id>/', views.steps_edit, name = 'steps_edit'),
    path('steps/<str:id>/delete/', views.steps_delete, name = 'steps_delete'),
    path('steps/<str:id>/delete/confirm/', views.steps_delete_confirm, name = 'steps_delete_confirm'),
    path('steps/<str:id>/deletestep/<str:step_id>', views.steps_delete_step, name = 'steps_delete_step'),
    
    path('supersteps', views.supersteps, name = 'supersteps'),
    path('supersteps/<str:id>/delete/', views.supersteps_delete, name = 'supersteps_delete'),
    path('supersteps/<str:id>/delete/confirm/', views.supersteps_delete_confirm, name = 'supersteps_delete_confirm'),
    path('substeps', views.substeps, name = 'substeps'),
    path('substeps/<str:id>/delete/', views.substeps_delete, name = 'substeps_delete'),
    path('substeps/<str:id>/delete/confirm/', views.substeps_delete_confirm, name = 'substeps_delete_confirm'),

    #AJAX
    path('howtos/<str:id>/save-order', views.save_howto_order, name = 'save_howto_order'),
    path('steps/<str:id>/save-order', views.save_step_order, name = 'save_step_order'),
]
