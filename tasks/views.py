from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from functools import wraps
from .models import User, Project, Task


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin():
            messages.error(request, 'Access denied. Admins only.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


def landing(request):
    return render(request, 'landing.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.full_name or user.username}!')
            return redirect('dashboard')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'auth/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        department = request.POST.get('department')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'auth/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'auth/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'auth/register.html')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            full_name=full_name,
            department=department,
            role='user'
        )
        messages.success(request, 'Account created! Please log in.')
        return redirect('login')
    return render(request, 'auth/register.html')


@login_required
def dashboard(request):
    total_tasks = Task.objects.count()
    pending_tasks = Task.objects.filter(status='Pending').count()
    inprogress_tasks = Task.objects.filter(status='In Progress').count()
    completed_tasks = Task.objects.filter(status='Completed').count()
    total_projects = Project.objects.count()
    total_users = User.objects.count()

    if request.user.is_admin():
        my_tasks = Task.objects.order_by('due_date')[:5]
    else:
        my_tasks = Task.objects.filter(assigned_to=request.user).order_by('due_date')[:5]

    return render(request, 'dashboard.html', {
        'total_tasks': total_tasks,
        'pending_tasks': pending_tasks,
        'inprogress_tasks': inprogress_tasks,
        'completed_tasks': completed_tasks,
        'total_projects': total_projects,
        'total_users': total_users,
        'my_tasks': my_tasks,
    })


@login_required
def task_list(request):
    tasks = Task.objects.order_by('due_date')
    return render(request, 'tasks/list.html', {'tasks': tasks})


@login_required
def task_create(request):
    projects = Project.objects.all()
    users = User.objects.all()
    if request.method == 'POST':
        task = Task.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            due_date=request.POST.get('due_date'),
            priority=request.POST.get('priority'),
            status=request.POST.get('status'),
            project_id=request.POST.get('project_id'),
            assigned_to_id=request.POST.get('assigned_to'),
            created_by=request.user
        )
        messages.success(request, 'Task created successfully!')
        return redirect('task_list')
    return render(request, 'tasks/create.html', {'projects': projects, 'users': users})


@login_required
def task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'tasks/view.html', {'task': task})


@login_required
def task_edit(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if not request.user.is_admin() and task.assigned_to != request.user:
        messages.error(request, 'You do not have permission to edit this task.')
        return redirect('task_list')
    projects = Project.objects.all()
    users = User.objects.all()
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.due_date = request.POST.get('due_date')
        task.priority = request.POST.get('priority')
        task.status = request.POST.get('status')
        task.project_id = request.POST.get('project_id')
        task.assigned_to_id = request.POST.get('assigned_to')
        task.save()
        messages.success(request, 'Task updated successfully!')
        return redirect('task_view', task_id=task.id)
    return render(request, 'tasks/edit.html', {'task': task, 'projects': projects, 'users': users})


@login_required
@admin_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.delete()
        messages.info(request, 'Task deleted.')
        return redirect('task_list')
    return redirect('task_list')


@login_required
def task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['Pending', 'In Progress', 'Completed']:
            task.status = new_status
            task.save()
            messages.success(request, 'Status updated!')
    return redirect('task_view', task_id=task.id)


@login_required
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'projects/list.html', {'projects': projects})


@login_required
@admin_required
def project_create(request):
    if request.method == 'POST':
        Project.objects.create(
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            created_by=request.user
        )
        messages.success(request, 'Project created successfully!')
        return redirect('project_list')
    return render(request, 'projects/create.html')


@login_required
@admin_required
def project_edit(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        project.name = request.POST.get('name')
        project.description = request.POST.get('description')
        project.save()
        messages.success(request, 'Project updated!')
        return redirect('project_list')
    return render(request, 'projects/edit.html', {'project': project})


@login_required
@admin_required
def project_delete(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        project.delete()
        messages.info(request, 'Project deleted.')
    return redirect('project_list')


@login_required
@admin_required
def staff_list(request):
    staff = User.objects.order_by('full_name')
    return render(request, 'admin/staff.html', {'staff': staff})


@login_required
@admin_required
def staff_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.info(request, f'{user.full_name} has been removed.')
    return redirect('staff_list')


@login_required
def refresh_tasks(request):
    if request.user.is_admin():
        tasks = Task.objects.order_by('due_date')
    else:
        tasks = Task.objects.filter(assigned_to=request.user).order_by('due_date')
    data = [{
        'id': t.id,
        'title': t.title,
        'status': t.status,
        'priority': t.priority,
        'due_date': t.due_date.strftime('%d %b %H:%M')
    } for t in tasks]
    return JsonResponse(data, safe=False)