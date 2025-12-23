from django.urls import *
from admin_panel.views import *

urlpatterns=[
    path('admin_signup/',AdminSignupView.as_view(),name='admin_signup'),
    path('admin_approvel/<str:pk>/',ApproveStudentView.as_view(),name='admin_approvel'),
    path('admindashboard/',AdminDashboard.as_view(),name='admindashboard')
]