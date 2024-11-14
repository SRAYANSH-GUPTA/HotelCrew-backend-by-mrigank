from django.urls import path
from .views import Taskassignment

urlpatterns = [
    path('tasks/', Taskassignment.as_view(), name='task-create'),
]