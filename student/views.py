from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from student.serializers import *
from django.contrib.auth import authenticate,login
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.timezone import localtime
from instructor.models import *
from rest_framework.permissions import IsAuthenticated 
# Create your views here.
class StudentSignupView(APIView):
    def get(self,request):
        try:
            st_datas=Student.objects.all()
            serializer=StudentSerializer(st_datas,many=True)
            return Response({'message':serializer.data},status=200)
        except Exception as e:
            return Response({'error':str(e)},status=500)
    def post(self, request):
        try:
            
            serializer = StudentSerializer(
                data=request.data,
                context={"request": request}
            )

            if serializer.is_valid():
                serializer.save()
                return Response({"status": 1, "message": "Student created successfully"}, status=201)

            return Response({"status": 0, "errors": serializer.errors}, status=400)
        except Exception as e:
            return Response({'error':str(e)},status=500)
    
class StudentsView(APIView):

    # Get single student object (not Response)
    def get_object(self, id):
        try:
            return Student.objects.get(pk=id)
        except Student.DoesNotExist:
            return None

    # -------- GET SINGLE STUDENT --------
    def get(self, request, id):
        student = self.get_object(id)
        if not student:
            return Response({"error": "Student not found"}, status=404)

        serializer = StudentSerializer(student)
        return Response(serializer.data, status=200)

    # -------- UPDATE STUDENT (PUT) --------
    def put(self, request, id):
        student = self.get_object(id)
        if not student:
            return Response({"error": "Student not found"}, status=404)

        serializer = StudentSerializer(student, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)

        return Response({'error': serializer.errors}, status=400)


        
    
class GlobalLoginView(APIView):
    def post(self, request):
        try:
            email = request.data.get("email")
            password = request.data.get("password")

            if not email or not password:
                return Response(
                    {"status": 0, "message": "Email and password required"},
                    status=400
                )

            user = authenticate(request, email=email, password=password)

            if not user:
                return Response(
                    {"status": 0, "message": "Invalid email or password"},
                    status=400
                )

            response_data = {
                "status": 1,
                "message": f"{user.role} login successful",
                "role": user.role,
                "email": user.email,
            }

            # 🎓 STUDENT
            if user.role == "student":
                if not hasattr(user, "student_profile"):
                    return Response(
                        {"status": 0, "message": "Student profile missing"},
                        status=400
                    )

                if user.student_profile.status != "approved":
                    return Response(
                        {"status": 0, "message": "Student not approved yet"},
                        status=403
                    )

                student=user.student_profile
                classroom_id = student.section.cls_id

                section_id = student.section_id

                response_data.update({
                        "student_id": student.id,
                        "classroom_id": classroom_id,
                        "section_id": section_id,
                    })

            # 👨‍🏫 INSTRUCTOR
            elif user.role == "instructor":
                if not hasattr(user, "instructor_profile"):
                    return Response(
                        {"status": 0, "message": "Instructor profile missing"},
                        status=400
                    )

                response_data["instructor_id"] = user.instructor_profile.id

            # 👑 ADMIN
            elif user.role == "admin":
                if not hasattr(user, "admin_profile"):
                    return Response(
                        {"status": 0, "message": "Admin profile missing"},
                        status=400
                    )

                response_data["admin_id"] = user.admin_profile.id

            # login + JWT
            login(request, user)
            refresh = RefreshToken.for_user(user)

            response_data.update({
                "last_login": localtime(user.last_login).strftime("%Y-%m-%d %H:%M:%S"),
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            })

            return Response(response_data, status=200)

        except Exception as e:
            return Response(
                {"status": 0, "error": str(e)},
                status=500
            )
class InstructorStudentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user

            # ---------------------------------
            # If instructor → use own profile
            # ---------------------------------
            if Instructor.objects.filter(user=user).exists():
                instructor = Instructor.objects.get(user=user)

            # ---------------------------------
            # If admin → instructor_id REQUIRED
            # ---------------------------------
            elif user.is_staff or user.is_superuser:
                instructor_id = request.query_params.get("instructor_id")

                if not instructor_id:
                    return Response(
                        {
                            "status": 0,
                            "error": "instructor_id is required for admin"
                        },
                        status=400
                    )

                instructor = Instructor.objects.get(id=instructor_id)

            else:
                return Response(
                    {
                        "status": 0,
                        "error": "You do not have permission"
                    },
                    status=403
                )

            # ---------------------------------
            # Get instructor section students
            # ---------------------------------
            section_ids = AssignClassTeacher.objects.filter(
                teacher=instructor
            ).values_list("section_id", flat=True)

            students = Student.objects.filter(
                section_id__in=section_ids
            )

            serializer = StudentSerializer(students, many=True)

            return Response(
                {
                    "status": 1,
                    "data": serializer.data
                },
                status=200
            )

        except Instructor.DoesNotExist:
            return Response(
                {
                    "status": 0,
                    "error": "Instructor not found"
                },
                status=404
            )

        except Exception as e:
            return Response(
                {
                    "status": 0,
                    "error": str(e)
                },
                status=500
            )
