from django.urls import path
from .views import *

urlpatterns = [
    path('review-exam/<int:exam_id>/<int:student_id>/',ExamReviewView.as_view()),
    path('submit-exam/',SubmitExamView.as_view())
]
