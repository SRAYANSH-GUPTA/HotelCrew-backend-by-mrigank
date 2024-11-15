from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'attendance')
    list_filter = ('attendance', 'date', 'user')
    search_fields = ('user__email',)
    ordering = ('-date',)