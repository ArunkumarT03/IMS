from django.urls import path
from student.views import *

urlpatterns=[
    path('student_signup/',StudentSignupView.as_view(),name='student_signup'),
 
    path('login/',GlobalLoginView.as_view(),name='login')
]