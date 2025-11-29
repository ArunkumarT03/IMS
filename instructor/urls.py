from django.urls import path
from .views import InstructorCreateView

urlpatterns = [
    path('instructors/', InstructorCreateView.as_view(), name='instructor-list-create'),
    path('instructors/<int:id>/', InstructorCreateView.as_view()),
]
