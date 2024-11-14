from django.urls import path
from .views import Taskassignment,TaskDeleteView,TaskUpdateView,AllTaskListView,StaffTaskListView,TaskStatusUpdateView

urlpatterns = [
    path('tasks/', Taskassignment.as_view(), name='task-create'),
    path('tasks/delete/<int:pk>/', TaskDeleteView.as_view()),
    path('tasks/update/<int:pk>/', TaskUpdateView.as_view()),
    path('tasks/all/', AllTaskListView.as_view()),
    path('tasks/staff/',StaffTaskListView.as_view()),
    path('tasks/status/<int:pk>/', TaskStatusUpdateView.as_view(),)

    
    
   
]