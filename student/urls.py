from django.urls import path
from student.views import *

urlpatterns=[
    path('student_signup/',StudentSignupView.as_view(),name='student_signup'),
    path('student_info/<int:id>/',StudentsView.as_view(),name='student_info'),
    path('students_data/',StudentSignupView.as_view(),name='students_data'),
 
    path('login/',GlobalLoginView.as_view(),name='login')
]