# exams/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Exam, Question
from .serializers import ExamSerializer, QuestionSerializer


# ---------------------------------------------------------------------
# EXAM LIST + CREATE
# ---------------------------------------------------------------------
class ExamListCreateView(APIView):
    permission_classes = [permissions.AllowAny]

    # GET → List all exams
    def get(self, request):
        exams = Exam.objects.all()
        serializer = ExamSerializer(exams, many=True)
        return Response(serializer.data, status=200)

    # POST → Create exam
    def post(self, request):
        serializer = ExamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": 1,
                "message": "Exam created successfully",
                "data": serializer.data
            }, status=201)

        return Response(serializer.errors, status=400)


# ---------------------------------------------------------------------
# EXAM RETRIEVE + UPDATE + DELETE
# ---------------------------------------------------------------------
class ExamDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    # helper
    def get_exam(self, pk):
        try:
            return Exam.objects.get(pk=pk)
        except Exam.DoesNotExist:
            return None

    # GET → Retrieve single exam
    def get(self, request, pk):
        exam = self.get_exam(pk)
        if not exam:
            return Response({"error": "Exam not found"}, status=404)

        serializer = ExamSerializer(exam)
        return Response(serializer.data, status=200)

    # PUT → Update exam
    def put(self, request, pk):
        exam = self.get_exam(pk)
        if not exam:
            return Response({"error": "Exam not found"}, status=404)

        serializer = ExamSerializer(exam, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": 1,
                "message": "Exam updated successfully",
                "data": serializer.data
            }, status=200)

        return Response(serializer.errors, status=400)

    # DELETE → Delete exam
    def delete(self, request, pk):
        exam = self.get_exam(pk)
        if not exam:
            return Response({"error": "Exam not found"}, status=404)

        exam.delete()
        return Response({"message": "Exam deleted successfully"}, status=200)


# ---------------------------------------------------------------------
# QUESTION LIST + CREATE for specific exam
# ---------------------------------------------------------------------
class ExamQuestionListCreateView(APIView):
    permission_classes = [permissions.AllowAny]

    # GET → List questions for an exam
    def get(self, request, exam_id):
        questions = Question.objects.filter(exam_id=exam_id)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=200)

    # POST → Add question to exam
    def post(self, request, exam_id):
        try:
            exam = Exam.objects.get(id=exam_id)
        except Exam.DoesNotExist:
            return Response({"error": "Exam not found"}, status=404)

        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(exam=exam)
            return Response({
                "status": 1,
                "message": "Question created successfully",
                "data": serializer.data
            }, status=201)

        return Response(serializer.errors, status=400)


# ---------------------------------------------------------------------
# QUESTION RETRIEVE + UPDATE + DELETE
# ---------------------------------------------------------------------
class QuestionListView(APIView):

    # GET all questions
    def get(self, request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    # POST a new question
    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": "Question created successfully",
            "data": serializer.data
        }, status=201)


class QuestionDetailView(APIView):

    # GET single question
    def get(self, request, pk):
        try:
            question = Question.objects.get(id=pk)
        except Question.DoesNotExist:
            return Response({"error": "Question not found"}, status=404)

        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    # PUT update question
    def put(self, request, pk):
        try:
            question = Question.objects.get(id=pk)
        except Question.DoesNotExist:
            return Response({"error": "Question not found"}, status=404)

        serializer = QuestionSerializer(question, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "message": "Question updated successfully",
            "data": serializer.data
        })

    # DELETE question
    def delete(self, request, pk):
        try:
            question = Question.objects.get(id=pk)
        except Question.DoesNotExist:
            return Response({"error": "Question not found"}, status=404)

        question.delete()
        return Response({"message": "Question deleted"})