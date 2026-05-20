from django.contrib import admin
from django.urls import path
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing, name='landing'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/new/', views.task_create, name='task_create'),
    path('tasks/<int:task_id>/', views.task_view, name='task_view'),
    path('tasks/<int:task_id>/edit/', views.task_edit, name='task_edit'),
    path('tasks/<int:task_id>/delete/', views.task_delete, name='task_delete'),
    path('tasks/<int:task_id>/status/', views.task_status, name='task_status'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/new/', views.project_create, name='project_create'),
    path('projects/<int:project_id>/edit/', views.project_edit, name='project_edit'),
    path('projects/<int:project_id>/delete/', views.project_delete, name='project_delete'),
    path('admin-panel/staff/', views.staff_list, name='staff_list'),
    path('admin-panel/staff/<int:user_id>/delete/', views.staff_delete, name='staff_delete'),
    path('api/tasks/refresh/', views.refresh_tasks, name='refresh_tasks'),
]