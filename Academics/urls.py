from django.urls import path

from Academics.views import *

urlpatterns=[
    path('classroom/',CreateClassroomView.as_view(),name='classroom'),
    path('classroom/<int:pk>/', CreateClassroomView.as_view(), name='classroom_update'),
    path('subject/',SubjectView.as_view(),name='subject'),
    path("subject/<int:pk>/", SubjectView.as_view(), name="subject_detail"),
    path('assign-subject/', AssignSubjectView.as_view(),name='assign_subject'),
    path('assign-subject/<int:pk>/', AssignSubjectView.as_view(), name='update_assign_subject'), 
    path('assign-class-teacher/', AssignClassTeacherView.as_view(),name='assign_class_teacher'),
    path('assign-class-teacher/<int:pk>/',AssignClassTeacherView.as_view(),name="update_class_teacher"),
    path('subject-teacher/', SubjectTeachersAPIView.as_view(), name='subjects'),
    path('subject-teacher/<int:pk>/', SubjectTeachersAPIView.as_view(), name='subject-detail'),
    path('roles/',GetRolesOnlyView.as_view())
]
