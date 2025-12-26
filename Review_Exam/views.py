from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import StudentExamRecord
from .serializers import ExamReviewSerializer
from rest_framework import status
from Online_Exam.models import Exam,Option,Question 
from django.shortcuts import get_object_or_404 
from student.models import Student
from django.db import transaction
from django.utils import timezone



from django.db.models import Sum

class ExamReviewView(APIView):

    def get(self, request, exam_id, student_id):
        try:
            exam = get_object_or_404(Exam, id=exam_id)
            now = timezone.now()

            attempt = StudentExamRecord.objects.filter(
                exam_id=exam_id,
                student_id=student_id
            ).order_by('-submitted_at').first()

            # 🔹 Determine exam status
            if now > exam.end_time:
                exam_status = 'expired'
            elif attempt:
                exam_status = 'completed'
            else:
                exam_status = 'not_started_yet'

            total_score = 0
            review_data = {}

            # 🔹 If student has attempted, calculate marks
            if attempt:
                total_score = StudentExamRecord.objects.filter(
                    student_id=student_id,
                    exam_id=exam_id,
                    submitted_at=attempt.submitted_at
                ).aggregate(total=Sum('mark_obtained'))['total'] or 0

                review_data = ExamReviewSerializer(attempt).data

            # 🔹 Final response data
            review_data.update({
                "status": exam_status,
                "can_attend": False,                 # expired / completed → false
                "can_view_answers": now>exam.end_time,
                "total_score": total_score
            })

            return Response({
                "status": 1,
                "message": "Exam review loaded successfully",
                "data": review_data
            })

        except Exception as e:
            return Response(
                {"status": 0, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class SubmitExamView(APIView):

    def post(self, request):
        student = get_object_or_404(Student, id=request.data.get("student_id"))
        exam = get_object_or_404(Exam, id=request.data.get("exam_id"))
        answers = request.data.get("answers", [])

        now = timezone.now()

        # ⏰ Exam time validation
        if now < exam.start_time:
            return Response(
                {"status": 0, "message": "Exam has not started yet"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if now > exam.end_time:
            return Response(
                {"status": 0, "message": "Exam time is over"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 🔁 Max attempts check
        submissions = StudentExamRecord.objects.filter(
            student=student,
            exam=exam
        ).values('submitted_at').distinct().count()

        if submissions >= exam.attempts_allowed:
            return Response(
                {"status": 0, "message": "Maximum attempts reached"},
                status=status.HTTP_400_BAD_REQUEST
            )

        total_marks = 0
        submission_time = now

        try:
            with transaction.atomic():
                for a in answers:
                    question_id = a.get("question_id")
                    option_id = a.get("option_id")

                    if not question_id or not option_id:
                        return Response(
                            {"status": 0, "message": "question_id and option_id are required"},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                    question = get_object_or_404(
                        Question,
                        id=question_id,
                        exam=exam
                    )

                    option = get_object_or_404(
                        Option,
                        id=option_id,
                        question=question
                    )

                    mark = question.marks if option.is_correct else 0
                    total_marks += mark

                    correct_option = question.options.filter(is_correct=True).first()

                    StudentExamRecord.objects.create(
                        student=student,
                        exam=exam,
                        question=question,
                        option=option,
                        select_answer=option.text,
                        correct_answer=correct_option.text if correct_option else "",
                        is_correct=option.is_correct,
                        mark_obtained=mark,
                        submitted_at=submission_time
                    )

                # Update total marks for this submission
                StudentExamRecord.objects.filter(
                    student=student,
                    exam=exam,
                    submitted_at=submission_time
                ).update(total_marks=total_marks)

            return Response(
                {
                    "status": 1,
                    "message": "Exam submitted successfully",
                    "total_marks": total_marks
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"status": 0, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )