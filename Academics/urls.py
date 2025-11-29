from django.urls import path

from Academics.views import *

urlpatterns=[
    path('classroom/',CreateClassroomView.as_view(),name='classroom'),
    path('subject/',SubjectView.as_view(),name='subject'),
    path('assign-subject/', AssignSubjectView.as_view(),name='assign_subject'),
    path('assign-class-teacher/', AssignClassTeacherView.as_view(),name='assign_class_teacher'),
]