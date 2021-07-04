from django.urls import include, path
from .views import general_views, howtos, steps, explanations


urlpatterns = [
    # Dashboard
    path('', include("django.contrib.auth.urls")),
    path('', general_views.login, name = 'login'),
    path('logout/', general_views.logout, name = 'logout'),
    path('dashboard/', general_views.dashboard, name = 'dashboard'),

    # Information
    path('information/', general_views.information, name = 'information'),
    
    # How To's
    path('howtos/', howtos.howtos, name = 'howtos'),
    path('howtos/create/', howtos.howtos_create, name = 'howtos_create'),
    path('howtos/<str:id>/', howtos.howtos_edit, name = 'howtos_edit'),
    path('howtos/<str:id>/delete/', howtos.howtos_delete, name = 'howtos_delete'),
    path('howtos/<str:id>/delete/confirm/', howtos.howtos_delete_confirm, name = 'howtos_delete_confirm'),
    path('howtos/<str:id>/deletestep/<str:step_id>/', howtos.howtos_delete_step, name = 'howtos_delete_step'),
    path('howtos/<str:id>/addsteps/', howtos.howtos_add_steps, name = 'howtos_add_steps'),
    path('howtos/<str:id>/addsteps/<str:step_id>/', howtos.howtos_add_steps_confirm, name = 'howtos_add_steps_confirm'),
    
    # Steps
    path('steps/', steps.steps, name = 'steps'),
    path('steps/create/', steps.steps_create, name = 'steps_create'),
    path('steps/<str:id>/', steps.steps_edit, name = 'steps_edit'),
    path('steps/<str:id>/delete/', steps.steps_delete, name = 'steps_delete'),
    path('steps/<str:id>/delete/confirm/', steps.steps_delete_confirm, name = 'steps_delete_confirm'),
    path('steps/<str:id>/deletestep/<str:step_id>/', steps.steps_delete_step, name = 'steps_delete_step'),
    path('steps/<str:id>/addsteps/', steps.steps_add_steps, name = 'steps_add_steps'),
    path('steps/<str:id>/addsteps/<str:step_id>/', steps.steps_add_steps_confirm, name = 'steps_add_steps_confirm'),
    
    path('supersteps/', steps.supersteps, name = 'supersteps'),
    path('supersteps/<str:id>/delete/', steps.supersteps_delete, name = 'supersteps_delete'),
    path('supersteps/<str:id>/delete/confirm/', steps.supersteps_delete_confirm, name = 'supersteps_delete_confirm'),
    path('substeps/', steps.substeps, name = 'substeps'),
    path('substeps/<str:id>/delete/', steps.substeps_delete, name = 'substeps_delete'),
    path('substeps/<str:id>/delete/confirm/', steps.substeps_delete_confirm, name = 'substeps_delete_confirm'),

    # Explanations
    path('explanations/text/', explanations.text, name = 'text'),
    path('explanations/text/create', explanations.text_create, name = 'text-create'),
    path('explanations/code/', explanations.code, name = 'code'),

    # AJAX
    path('howtos/<str:id>/save-order/', howtos.save_howto_order, name = 'save_howto_order'),
    path('steps/<str:id>/save-order/', steps.save_step_order, name = 'save_step_order'),
]
