from django.urls import path
from users.views import *

urlpatterns=[
    path('delete/<str:pk>/',UserDeleteView.as_view(),name='delete')
]