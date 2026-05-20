from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'Standard User'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    department = models.CharField(max_length=50, blank=True)
    full_name = models.CharField(max_length=100, blank=True)

    def is_admin(self):
        return self.role == 'admin'

    def __str__(self):
        return self.username


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects_created')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    title = models.CharField(max_length=150)
    description = models.TextField()
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_assigned')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_overdue(self):
        from django.utils import timezone
        return self.due_date < timezone.now() and self.status != 'Completed'

    def __str__(self):
        return self.title