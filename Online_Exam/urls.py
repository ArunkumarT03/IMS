from django.urls import path
from .views import ( ExamListCreateView, ExamDetailView, ExamQuestionListCreateView, QuestionDetailView
)

urlpatterns = [
    # Exams
    path("exams/", ExamListCreateView.as_view(), name="exam-list"),
    path("exams/<int:pk>/", ExamDetailView.as_view(), name="exam-detail"),

    # Questions
    path("exams/<int:exam_id>/questions/", ExamQuestionListCreateView.as_view(),  name="exam-question-list-create"),

    path("questions/<int:pk>/",  QuestionDetailView.as_view(),  name="question-detail"),
]
