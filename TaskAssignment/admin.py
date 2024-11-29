from django.contrib import admin
from .models import *

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'department', 'status', 'assigned_to', 'assigned_by', 'hotel')
    list_filter = ('id',)


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('id','assigned_by','department', 'title','hotel')
    list_filter = ('id',)