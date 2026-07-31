from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'status', 'start_date', 'end_date')
    search_fields = ('name', 'organization__name')
    list_filter = ('status', 'organization')
