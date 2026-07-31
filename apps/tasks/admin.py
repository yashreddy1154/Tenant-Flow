from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'status', 'priority', 'assignee')
    search_fields = ('title', 'project__name')
    list_filter = ('status', 'priority')
