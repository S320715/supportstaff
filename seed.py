import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meditask.settings')
django.setup()

from django.utils import timezone
from datetime import timedelta
from tasks.models import User, Project, Task

print('Clearing old data...')
Task.objects.all().delete()
Project.objects.all().delete()
User.objects.all().delete()

print('Creating users...')
admin = User.objects.create_superuser(
    username='ashu',
    email='ashu@meditask.com',
    password='Ashu@123',
    full_name='Ashu',
    role='admin',
    department='Administration'
)

u1 = User.objects.create_user(username='j.oconnor', email='j.oconnor@meditask.com',
    password='User@123', full_name='James O\'Connor', role='user', department='Ward A')
u2 = User.objects.create_user(username='p.sharma', email='p.sharma@meditask.com',
    password='User@123', full_name='Priya Sharma', role='user', department='Ward A')
u3 = User.objects.create_user(username='d.chen', email='d.chen@meditask.com',
    password='User@123', full_name='David Chen', role='user', department='Ward B')
u4 = User.objects.create_user(username='a.patel', email='a.patel@meditask.com',
    password='User@123', full_name='Aisha Patel', role='user', department='Ward B')
u5 = User.objects.create_user(username='m.brown', email='m.brown@meditask.com',
    password='User@123', full_name='Michael Brown', role='user', department='All Wards')
u6 = User.objects.create_user(username='l.kowalski', email='l.kowalski@meditask.com',
    password='User@123', full_name='Linda Kowalski', role='user', department='All Wards')
u7 = User.objects.create_user(username='r.taylor', email='r.taylor@meditask.com',
    password='User@123', full_name='Robert Taylor', role='user', department='Pharmacy')
u8 = User.objects.create_user(username='e.williams', email='e.williams@meditask.com',
    password='User@123', full_name='Emma Williams', role='user', department='Emergency')
u9 = User.objects.create_user(username='h.ali', email='h.ali@meditask.com',
    password='User@123', full_name='Hassan Ali', role='user', department='Outpatients')

print('Creating projects...')
p1 = Project.objects.create(name='Ward A — General Medicine', description='General medicine ward tasks', created_by=admin)
p2 = Project.objects.create(name='Ward B — Cardiology', description='Cardiology ward tasks', created_by=admin)
p3 = Project.objects.create(name='Emergency Department', description='Emergency department tasks', created_by=admin)
p4 = Project.objects.create(name='Outpatients', description='Outpatient clinic tasks', created_by=admin)
p5 = Project.objects.create(name='Pharmacy Support', description='Pharmacy support tasks', created_by=admin)

print('Creating tasks...')
now = timezone.now()
Task.objects.create(title='Morning medication round', description='Administer morning medications to all Ward A patients',
    due_date=now + timedelta(hours=2), priority='High', status='Pending', project=p1, assigned_to=u2, created_by=admin)
Task.objects.create(title='Patient vitals check', description='Record vitals for all Ward A patients',
    due_date=now + timedelta(hours=1), priority='Critical', status='In Progress', project=p1, assigned_to=u1, created_by=admin)
Task.objects.create(title='ECG monitoring', description='Monitor ECG readings for Ward B patients',
    due_date=now + timedelta(hours=3), priority='Critical', status='Pending', project=p2, assigned_to=u3, created_by=admin)
Task.objects.create(title='Ward B bed changes', description='Change bed linen for all Ward B patients',
    due_date=now + timedelta(hours=4), priority='Medium', status='Pending', project=p2, assigned_to=u4, created_by=admin)
Task.objects.create(title='Emergency triage support', description='Assist with triage documentation',
    due_date=now + timedelta(hours=1), priority='Critical', status='In Progress', project=p3, assigned_to=u8, created_by=admin)
Task.objects.create(title='Porter patient transfer', description='Transfer patients from Emergency to wards',
    due_date=now + timedelta(hours=2), priority='High', status='Pending', project=p3, assigned_to=u5, created_by=admin)
Task.objects.create(title='Pharmacy stock check', description='Check and restock ward medication supplies',
    due_date=now + timedelta(hours=5), priority='Medium', status='Pending', project=p5, assigned_to=u7, created_by=admin)
Task.objects.create(title='Outpatient clinic setup', description='Prepare outpatient clinic rooms',
    due_date=now + timedelta(hours=1), priority='High', status='Completed', project=p4, assigned_to=u9, created_by=admin)

print('Database seeded successfully!')
print('Admin login: ashu / Ashu@123')
print('Staff login: p.sharma / User@123')