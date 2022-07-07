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
    path('sequences/<str:uuid>/', sequence.sequence, name='sequence'),
    
    # Steps
    path('steps/', step.steps, name='steps'),
    path('steps/<str:uuid>/', step.step, name='step'),
]



'''  legacy
# Sequences
path('sequences/create/', sequence.sequences_create, name='sequences-create'),
path('sequences/<str:id>/', sequence.sequences_edit, name='sequences-edit'),
path('sequences/<str:id>/delete/', sequence.sequence_delete, name='sequences-delete'),
path('sequences/<str:id>/delete/confirm/', sequence.sequence_delete_confirm, name='sequences-delete-confirm'),
path('sequences/<str:id>/deletestep/<str:step_id>/', sequence.sequence_delete_step, name='sequences-delete-step'),
path('sequences/<str:id>/addsteps/', sequence.sequence_add_steps, name='sequences-add-steps'),
path('sequences/<str:id>/addsteps/<str:step_id>/', sequence.sequence_add_steps_confirm, name='sequences-add-steps-confirm'),

# Steps
path('steps/', step.steps, name='steps'),
path('steps/create/', step.steps_create, name='steps-create'),
path('steps/<str:id>/', step.steps_edit, name='steps-edit'),
path('steps/<str:id>/delete/', step.steps_delete, name='steps-delete'),
path('steps/<str:id>/delete/confirm/', step.steps_delete_confirm, name='steps-delete-confirm'),
path('steps/<str:id>/deletestep/<str:step_id>/', step.steps_delete_step, name='steps-delete-step'),
path('steps/<str:id>/deletedecision/<str:step_id>/', step.steps_delete_decision, name='steps-delete-decision'),
path('steps/<str:id>/addsteps/', step.steps_add_steps, name='steps-add-steps'),
path('steps/<str:id>/addsteps/<str:step_id>/', step.steps_add_steps_confirm, name='steps-add-steps-confirm'),
path('steps/<str:id>/adddecisions/', step.steps_add_decisions, name='steps-add-decisions'),
path('steps/<str:id>/adddecisions/<str:step_id>/', step.steps_add_decisions_confirm, name='steps-add-decisions-confirm'),
path('steps/<str:id>/addtextmodule/', step.steps_add_textmodule, name='steps-add-textmodule'),
path('steps/<str:id>/addtextmodule/<str:explanation_id>/', step.steps_add_textmodule_confirm, name='steps-add-textmodule-confirm'),
path('steps/<str:id>/deletemodule/<str:explanation_id>/', step.steps_delete_module, name='steps-delete-module'),
path('steps/<str:id>/addcodemodule/', step.steps_add_codemodule, name='steps-add-codemodule'),
path('steps/<str:id>/addcodemodule/', step.steps_add_codemodule, name='steps-add-codemodule'),
path('steps/<str:id>/addcodemodule/<str:code_id>/', step.steps_add_codemodule_confirm, name='steps-add-codemodule-confirm'),

path('supersteps/', step.supersteps, name='supersteps'),
path('supersteps/<str:id>/delete/', step.supersteps_delete, name='supersteps-delete'),
path('supersteps/<str:id>/delete/confirm/', step.supersteps_delete_confirm, name='supersteps-delete-confirm'),
path('substeps/', step.substeps, name='substeps'),
path('substeps/<str:id>/delete/', step.substeps_delete, name='substeps-delete'),
path('substeps/<str:id>/delete/confirm/', step.substeps_delete_confirm, name='substeps-delete-confirm'),

# Explanations
path('explanations/text/', explanation.text, name='text'),
path('explanations/text/create', explanation.text_create, name='text-create'),
path('explanations/code/', explanation.code, name='code'),
path('explanations/code/create', explanation.code_create, name='code-create'),
path('explanations/<str:id>/', explanation.explanation_edit, name='explanation-edit'),
path('explanation/<str:id>/delete/', explanation.explanation_delete, name='explanation-delete'),
path('explanation/<str:id>/delete/confirm/', explanation.explanation_delete_confirm, name='explanation-delete-confirm'),

# Media
path('media/images/', media.images, name='images'),
path('media/images/upload', media.image_upload, name='image-upload'),
path('steps/<str:id>/addimage/', step.steps_add_image, name='steps-add-image'),
path('steps/<str:id>/addimage/<str:image_id>/', step.steps_add_image_confirm, name='steps-add-image-confirm'),

# AJAX
path('sequences/<str:id>/save-order/', sequence.save_sequence_order, name='save_sequence_order'),
path('sequences/<str:id>/publish/', sequence.sequence_publish, name='sequences-publish'),
path('steps/<str:id>/save-step-order/', step.save_step_order, name='save_step_order'),
path('steps/<str:id>/save-explanation-order/', step.save_explanation_order, name='save_explanation_order'),
path('steps/<str:id>/save-decision-order/', step.save_decision_order, name='save_decision_order'),
path('viewer/sequence_data/<str:id>/', viewer.view_sequence_data, name = 'view-sequence-data'),
path('viewer_preview/<str:step_api_id>/', viewer.view_step_preview, name = 'view-step-preview'),
path('viewer/<str:step_api_id>/', viewer.view_step_pre, name = 'view-step-pre'),
'''