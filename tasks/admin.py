from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Project, Task


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'full_name', 'email', 'role', 'department']
    fieldsets = UserAdmin.fieldsets + (
        ('MediTask Info', {'fields': ('role', 'department', 'full_name')}),
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'created_at']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority', 'status', 'assigned_to', 'due_date']