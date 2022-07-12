from django.urls import include, path

from cms.views import general
from cms.views.ajax.sequence import SequenceListFilterView
from cms.views.ajax.step import (
    StepLinkedOrderView,
    LinkStepView,
    StepListFilterView,
    StepLinkableListFilterView)
from cms.views.sequence import (
    SequenceDeleteLinkedView,
    SequenceDeleteView,
    SequenceListView,
    SequenceView)
from cms.views.step import (
    StepView,
    StepListView,
    StepDeleteView,
    StepDeleteLinkedView)


urlpatterns = [
    # Dashboard
    path('', include("django.contrib.auth.urls")),
    path('', general.login, name='login'),
    path('logout/', general.logout, name='logout'),
    path('dashboard/', general.dashboard, name='dashboard'),

    # Sequence
    path('sequences/',
         SequenceListView.as_view(),
         name='sequences'),
    path('sequences/<uuid:uuid>/',
         SequenceView.as_view(),
         name='sequence'),
    path('sequences/<uuid:uuid>/delete/',
         SequenceDeleteView.as_view(),
         name='sequence-delete'),
    path('sequences/<uuid:uuid>/steps/<uuid:super>/delete/<uuid:sub>/',
         SequenceDeleteLinkedView.as_view(),
         name='sequence-delete-linked'),

    # Step
    path('steps/',
         StepListView.as_view(),
         name='steps'),
    path('steps/<uuid:uuid>/',
         StepView.as_view(),
         name='step'),
    path('steps/<uuid:uuid>/delete',
         StepDeleteView.as_view(),
         name='step-delete'),
    path('steps/<uuid:uuid>/steps/delete/<uuid:sub>/',
         StepDeleteLinkedView.as_view(),
         name='step-delete-linked'),

    # AJAX Sequence
    path('sequences/filter/',
         SequenceListFilterView.as_view(),
         name='sequences-filter'),

    # AJAX Step
    path('steps/filter/',
         StepListFilterView.as_view(),
         name='steps-filter'),
    path('steps/<uuid:uuid>/linkable/filter/',
         StepLinkableListFilterView.as_view(),
         name='step-linkable-filter'),
    path('steps/<uuid:uuid>/steps/link/',
         LinkStepView.as_view(),
         name='link-step'),
    path('steps/<uuid:uuid>/steps/order/',
         StepLinkedOrderView.as_view(),
         name='linked-steps-order'),
]
