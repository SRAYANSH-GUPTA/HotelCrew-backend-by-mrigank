from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'department', 'status', 'assigned_to', 'assigned_by', 'hotel')
    list_filter = ('id',)

