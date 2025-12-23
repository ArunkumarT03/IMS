from django.urls import path
from .views import *

urlpatterns = [
    path('student-dashboard/', StudentDashboardView.as_view(), name='student-dashboard'),
    path('instructor-dashboard/',InstructorDashboardView.as_view(),name='instructor-dashboard')
]
