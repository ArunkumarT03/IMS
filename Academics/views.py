from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from Academics.models import *
from Academics.serializers import *
from rest_framework import status

class CreateClassroomView(APIView):
    def get(self, request, pk=None):
        if pk:
            # Get single classroom
            try:
                classroom = ClassRoom.objects.get(pk=pk)
            except ClassRoom.DoesNotExist:
                return Response({
                    "status": 0,
                    "message": "Classroom not found"
                }, status=404)

            serializer = ClassroomSerializer(classroom)
            return Response({
                "status": 1,
                "message": "Classroom fetched successfully",
                "data": serializer.data
            }, status=200)

        # Get all classrooms
        classrooms = ClassRoom.objects.all()
        serializer = ClassroomSerializer(classrooms, many=True)
        
        return Response({
            "status": 1,
            "message": "Classrooms fetched successfully",
            "data": serializer.data
        }, status=200)


    

    def post(self, request):
        serializer = CreateClassroomSerializer(data=request.data)
        if serializer.is_valid():
            classroom = serializer.save()
            return Response({
                "status": 1,
                "message": "Classroom created successfully",
                "data": ClassroomSerializer(classroom).data
            })
        return Response({"status": 0, "errors": serializer.errors}, status=400)
    def put(self, request, pk):
        try:
            try:
                classroom = ClassRoom.objects.get(pk=pk)
            except ClassRoom.DoesNotExist:
                return Response({
                    "status": 0,
                    "message": "Classroom not found"
                }, status=404)

            serializer = CreateClassroomSerializer(classroom, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": 1,
                    "message": "Classroom updated successfully",
                    "data": ClassroomSerializer(classroom).data
            })

            return Response({"status": 0, "errors": serializer.errors}, status=400)
        except Exception as e:
            return Response({"status": 0, "error": str(e)}, status=500)
 
  

class SubjectView(APIView):
    def get(self, request, pk=None):
        if pk:  # Fetch single subject
            try:
                subject = Subject.objects.get(pk=pk)
                serializer = SubjectSerializer(subject)
                return Response({
                    "status": 1,
                    "message": "Subject fetched successfully",
                    "data": serializer.data
                }, status=200)
            except Subject.DoesNotExist:
                return Response({
                    "status": 0,
                    "message": "Subject not found"
                }, status=404)

        # Fetch all subjects
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response({
            "status": 1,
            "message": "Subjects fetched successfully",
            "data": serializer.data
        }, status=200)

    def post(self,request):
        sub_data=SubjectSerializer(data=request.data)
        try:
            if sub_data.is_valid():
                subject=sub_data.save()
                return Response({'status':1,'message':'subject created', 'data': SubjectSerializer(subject).data},status=201)
            return Response({'status':0,'error':sub_data.errors},status=400)
        except Exception as e:
            return Response({'error':str(e)},status=500)
        
    def put(self, request, pk):
        try:
            subject = Subject.objects.get(pk=pk)
        except Subject.DoesNotExist:
            return Response({
                "status": 0,
                "message": "Subject not found"
            }, status=404)

        serializer = SubjectSerializer(subject, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": 1,
                "message": "Subject updated successfully",
                "data": serializer.data
            }, status=200)

        return Response({"status": 0, "errors": serializer.errors}, status=400) 

    def delete(self, request, pk):
        try:
            subject = Subject.objects.get(pk=pk)
            subject.delete()
            return Response({
                "status": 1,
                "message": "Subject deleted successfully"
            }, status=200)

        except Subject.DoesNotExist:
            return Response({
                "status": 0,
                "message": "Subject not found"
            }, status=404)

        except Exception as e:
            return Response({
                "status": 0,
            "   error": str(e)
            }, status=500)
   



# AssignSubject POST view
class AssignSubjectView(APIView):
    
    def get(self, request, pk=None):
        if pk:
            try:
                assignment = AssignSubject.objects.get(pk=pk)
                serializer = AssignSubjectListSerializer(assignment)
                return Response({
                    "status": 1,
                    "message": "Assignment fetched successfully",
                    "data": serializer.data
                })
            except AssignSubject.DoesNotExist:
                return Response({"status": 0, "message": "Assignment not found"}, status=404)
        else:
            assignments = AssignSubject.objects.all()
            serializer = AssignSubjectListSerializer(assignments, many=True)
            return Response({
                "status": 1,
                "message": "Assigned subjects fetched successfully",
                "data": serializer.data
            })

     
    def post(self, request):
        try:
            serializer = CreateAssignSubjectSerializer(data=request.data)
        
            if serializer.is_valid():
                assigned = serializer.save()

                response = []
                for a in assigned:
                    response.append({
                        "id": a.id,
                        "classroom": a.classroom.id,
                        "section": a.section.id,
                        "subject": a.subject.subject_name,
                        "teacher": [t.name for t in a.teacher.all()]
                })

                return Response({
                    "status": 1,
                    "message": "Assignments saved successfully!",
                    "data": response
                }, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"status": 0, "error": str(e)}, status=500)

 
    def put(self, request, pk):
        
        try:
            try:
                instance = AssignSubject.objects.get(pk=pk)
            except AssignSubject.DoesNotExist:
                return Response({"status": 0, "message": "Assignment not found"}, status=404)

            serializer = CreateAssignSubjectSerializer(instance, data=request.data)

            if serializer.is_valid():
                updated = serializer.save()

                return Response({
                    "status": 1,
                    "message": "Assignment updated successfully!",
                    "data": {
                        "id": updated.id,
                        "classroom": updated.classroom.id,
                        "section": updated.section.id,
                        "subject": updated.subject.subject_name,
                        "teacher": [t.name for t in updated.teacher.all()]
                }
            })

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"status": 0, "error": str(e)}, status=500)
 
class SubjectTeachersAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                subjects = [Subject.objects.get(pk=pk)]
            except Subject.DoesNotExist:
                return Response({"error": "Subject not found"}, status=404)
        else:
            subjects = Subject.objects.all()

        data = []
        for s in subjects:
            assignments = AssignSubject.objects.filter(subject=s)

            teacher_map = {}   # ← store unique teachers by ID

            for assign in assignments:
                for t in assign.teacher.all():
                    teacher_map[t.id] = {
                        "id": t.id,
                        "name": t.name
                    }

            data.append({
                "id": s.id,
                "subject": s.subject_name,
                "teachers": list(teacher_map.values())  # ← unique list
            })

        if pk and data:
            return Response(data[0])
        return Response(data)

        
# AssignClassTeacher POST view
class AssignClassTeacherView(APIView):
    
    def get(self, request, pk=None):
        if pk:
            try:
                assignment = AssignClassTeacher.objects.get(pk=pk)
                serializer = AssignClassTeacherListSerializer(assignment)
                return Response({
                    "status": 1,
                    "message": "Class teacher assignment fetched successfully",
                    "data": serializer.data
                })
            except AssignClassTeacher.DoesNotExist:
                return Response({"status": 0, "message": "Assignment not found"}, status=404)
        else:
            queryset = AssignClassTeacher.objects.all()
            serializer = AssignClassTeacherListSerializer(queryset, many=True)
            return Response({
                "status": 1,
                "message": "Assigned class teachers fetched successfully",
                "data": serializer.data
             })
    def post(self, request):
        serializer = AssignMultipleTeachersSerializer(data=request.data)

        if serializer.is_valid():
            result = serializer.save()
            return Response({
                "status": 1,
                "message": "Teachers assigned successfully",
                "data": result
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": 0,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, pk):
       
        try:
            instance = AssignClassTeacher.objects.get(pk=pk)
        except AssignClassTeacher.DoesNotExist:
            return Response({"status": 0, "message": "Assignment not found"}, status=404)

        serializer = AssignMultipleTeachersSerializer(instance, data=request.data)
        if serializer.is_valid():
            updated = serializer.save()
            return Response({
                "status": 1,
                "message": "Class teacher assignment updated successfully",
                "data": updated
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 