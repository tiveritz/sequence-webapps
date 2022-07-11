from django.urls import include, path
from cms.views import explanation, general, media, sequence, step, viewer
from django.views.generic import TemplateView


urlpatterns = [
    # Dashboard
    path('', include("django.contrib.auth.urls")),
    path('', general.login, name='login'),
    path('logout/', general.logout, name='logout'),
    path('dashboard/', general.dashboard, name='dashboard'),
    
    # Sequences
    path('sequences/', sequence.sequences, name='sequences'),
    path('sequences/<uuid:uuid>/', sequence.sequence, name='sequence'),
    path('sequences/<uuid:uuid>/delete/', sequence.sequence_delete, name='sequence-delete'),
    path('sequences/<uuid:uuid>/steps/<uuid:super>/delete/<uuid:sub>/', sequence.delete_linked, name='sequence-delete-linked'),
    
    # Steps
    path('steps/', step.steps, name='steps'),
    path('steps/<uuid:uuid>/', step.step, name='step'),
    path('steps/<uuid:uuid>/delete', step.step_delete, name='step-delete'),
    path('steps/<uuid:uuid>/steps/delete/<uuid:sub>/', step.delete_linked, name='step-delete-linked'),
    
    # AJAX
    path('sequences/filter/', sequence.sequences_filter, name='sequences-filter'),

    path('steps/<uuid:uuid>/steps/order/', step.linked_step_order, name='linked-steps-order'),
    path('steps/filter/', step.steps_filter, name='steps-filter'),
    
    path('steps/<uuid:uuid>/linkable/filter/', step.step_linkable_filter, name='step-linkable-filter'),
    path('steps/<uuid:uuid>/steps/link/', step.link_step, name='link-step'),
]
