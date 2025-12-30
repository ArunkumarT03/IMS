from django.urls import path
from .views import *

urlpatterns = [
    path('instructors/', InstructorCreateView.as_view(), name='instructor-list-create'),
    path('instructors/<int:id>/', InstructorCreateView.as_view()),
    path('instructors-subjects/', InstructorSubjectsAPIView.as_view(), name='instructors-subjects-list'),
    path('instructors-subjects/<int:instructor_id>/', InstructorSubjectsAPIView.as_view(), name='instructors-subjects-detail'),
    path('instructors_update/<int:id>/', InstructorUpdateView.as_view(),name='instructors_update'),
]
