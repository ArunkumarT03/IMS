from django.urls import path
from users.views import *

urlpatterns=[
    path("delete/<str:role>/<int:pk>/",UserDeleteView.as_view(),name='delete')
]