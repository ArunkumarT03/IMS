# exams/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Exam, Question
from .serializers import ExamSerializer, QuestionSerializer
from student.models import Student


# ---------------------------------------------------------------------
# EXAM LIST + CREATE
# ---------------------------------------------------------------------
class ExamListCreateView(APIView):
    permission_classes = [permissions.AllowAny]

    # GET → List all exams
    def get(self, request):
        try:
            exams = Exam.objects.all()
            serializer = ExamSerializer(exams, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({"status": 0, "error": str(e)}, status=500)
    # POST → Create exam
    def post(self, request):
        try:
            serializer = ExamSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": 1,
                    "message": "Exam created successfully",
                    "data": serializer.data
                }, status=201)

            return Response(serializer.errors, status=400)
        except Exception as e:
            return Response({"status": 0, "error": str(e)}, status=500)
 



class ExamDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    # helper
    def get_exam(self, pk):
        try:
            try:
                return Exam.objects.get(pk=pk)
            except Exam.DoesNotExist:
                return None
        except Exception as e:
            return Response({"status":0,"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
            

    # GET → Retrieve single exam
    def get(self, request, pk):
        try:
            exam = self.get_exam(pk)
            if not exam:
                return Response({"error": "Exam not found"}, status=404)

            serializer = ExamSerializer(exam)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({"status":0,"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # PUT → Update exam
    def put(self, request, pk):
        try:
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
        except Exception as e:
            return Response({"status":0,"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # DELETE → Delete exam
    def delete(self, request, pk):
        try:
            exam = self.get_exam(pk)
            if not exam:
                return Response({"error": "Exam not found"}, status=404)

            exam.delete()
            return Response({"message": "Exam deleted successfully"}, status=200)
        except Exception as e:
            return Response({"status":0,"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ExamByStudentClassSectionView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, student_id, classroom_id, section_id):
        try:
            # ---------- GET STUDENT ----------
            try:
                student = Student.objects.select_related(
                    "section",
                    "section__cls"
                ).get(id=student_id)
            except Student.DoesNotExist:
                return Response(
                    {"status": 0, "message": "Student not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # ---------- SECURITY CHECK ----------
            if (
                student.section.cls_id != classroom_id or
                student.section.id != section_id
            ):
                return Response(
                    {
                        "status": 0,
                        "message": "Student does not belong to this classroom or section"
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            # ---------- FETCH EXAMS ----------
            exams = Exam.objects.filter(
                classroom_id=classroom_id,
                sections__id=section_id
            ).distinct()

            if not exams.exists():
                return Response(
                    {"status": 0, "message": "No exams found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = ExamSerializer(
                exams,
                many=True,
                context={"section_id": section_id}
            )

            return Response(
                {"status": 1, "data": serializer.data},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"status": 0, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    
class QuestionListView(APIView):

    # GET all questions
    def get(self, request):
        try:
            questions = Question.objects.all()
            serializer = QuestionSerializer(questions, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"status":0,"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # POST a new question
    def post(self, request):
        try:
            serializer = QuestionSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                "message": "Question created successfully",
                "data": serializer.data
            }, status=201)
        except Exception as e:
            return Response({"status": 0, "error": str(e)}, status=500)


class QuestionDetailView(APIView):

    # GET single question
    def get(self,request, pk):
        try:
            try:
                question = Question.objects.get(id=pk)
            except Question.DoesNotExist:
                return Response({"error": "Question not found"}, status=404)

            serializer = QuestionSerializer(question)
            return Response(serializer.data)
        except Exception as e:
            return Response ({"status":0,"error":str(e)},status=500)

    # PUT update question
    def put(self, request, pk):
        try:
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
        except Exception as e:
            return Response({"status":0,"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # DELETE question
    def delete(self, request, pk):
        try:
            try:
                question = Question.objects.get(id=pk)
            except Question.DoesNotExist:
                return Response({"error": "Question not found"}, status=404)

            question.delete()
            return Response({"message": "Question deleted"})
        except Exception as e:
            return Response({"status":0,"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ExamQuestionsView(APIView):

    def get(self, request, exam_id):
        # Validate exam exists
        try:
            try:
                Exam.objects.get(id=exam_id)
            except Exam.DoesNotExist:
                return Response(
                    {"detail": "Exam not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            questions = Question.objects.filter(exam_id=exam_id).prefetch_related('options')
            serializer = QuestionSerializer(questions, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":0,"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)    