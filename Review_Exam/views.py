from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import StudentExamRecord
from .serializers import ExamReviewSerializer
from rest_framework import status
from Online_Exam.models import Exam,Option  



class ExamReviewView(APIView):
    def get(self, request, exam_id,student_id):
        records = StudentExamRecord.objects.filter(exam_id=exam_id,student_id=student_id)
        serializer = ExamReviewSerializer(records,many=True)

        if not records.exists():
            return Response(
                {
                    "status": 0,
                    "message": "No exam record found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
            
        return Response(
            {
                "status": 1,
                "message": "Exam review loaded successfully",
                "data": serializer.data
            }
        )
class SubmitExamView(APIView):
    def post(self, request):
        try:
            exam_id = request.data.get("exam_id")
            answers = request.data.get("answers", [])
            student_id = request.data.get("student_id")  

            if not student_id:
                return Response(
                    {"status": 0, "message": "student_id required"},
                    status=status.HTTP_400_BAD_REQUEST
            )

            exam = Exam.objects.get(id=exam_id)

            for ans in answers:
                option = Option.objects.get(id=ans["option_id"])
                question = option.question

                correct_option = question.options.filter(is_correct=True).first()

                StudentExamRecord.objects.create(
                    student_id=student_id,
                    exam=exam,
                    question=question,
                    option=option,
                    select_answer=option.text,
                    correct_answer=correct_option.text if correct_option else "",
                    is_correct=option.is_correct,
                    mark_obtained=1 if option.is_correct else 0
                )

            return Response(
                {"status": 1, "message": "Exam submitted successfully"},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({'error':str(e)},status=500)
