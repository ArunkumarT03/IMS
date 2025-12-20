from django.urls import path
from .views import StudentDashboardView

urlpatterns = [
    path('student-dashboard/', StudentDashboardView.as_view(), name='student-dashboard'),
]
