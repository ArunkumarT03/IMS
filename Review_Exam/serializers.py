from rest_framework import serializers
from .models import StudentExamRecord

class ExamReviewSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(source="question.text",read_only =True)
    selected_answer = serializers.CharField(source="option.text",read_only = True)
    class Meta:
        model = StudentExamRecord
        fields = [
            "question_text",
            "selected_answer",
            "correct_answer",
            "is_correct",
            "mark_obtained"

        ]