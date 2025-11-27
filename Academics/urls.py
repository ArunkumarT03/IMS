from django.urls import path

from Academics.views import *

urlpatterns=[
    path('classroom/',CreateClassroomView.as_view(),name='classroom'),
    path('subject/',SubjectView.as_view(),name='subject')
]