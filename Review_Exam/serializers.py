from rest_framework import serializers
from .models import StudentExamRecord



class ExamReviewSerializer(serializers.ModelSerializer):
    exam_id = serializers.IntegerField(source="exam.id")
    quiz_title = serializers.CharField(source="exam.title")
    start_time = serializers.DateTimeField(source="exam.start_time")
    end_time = serializers.DateTimeField(source="exam.end_time")
    time_limit = serializers.IntegerField(source="exam.time_limit")
    attempts_allowed = serializers.IntegerField(source="exam.attempts_allowed")

    attempts_made = serializers.SerializerMethodField()
    marks_obtained = serializers.IntegerField(source="total_marks")

    class Meta:
        model = StudentExamRecord       
        fields = [
            "exam_id",
            "quiz_title",
            "start_time",
            "end_time",
            "time_limit",
            "attempts_allowed",
            "attempts_made",
            "marks_obtained",
        ]

    def get_attempts_made(self, obj):
        submissions = StudentExamRecord.objects.filter(
            student=obj.student, exam=obj.exam
        ).values('submitted_at').distinct().count()
    
    # Cap attempts by allowed attempts
        return min(submissions, obj.exam.attempts_allowed)
