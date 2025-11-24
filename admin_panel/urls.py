from django.urls import *
from admin_panel.views import *

urlpatterns=[
    path('admin_signup/',AdminSignupView.as_view(),name='admin_signup'),
]