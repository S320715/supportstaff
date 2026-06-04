from django.test import TestCase, Client
from django.urls import reverse
from tasks.models import User, Project, Task
from django.utils import timezone
from datetime import timedelta


class TestUserModel(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            full_name='Test User',
            role='user',
            department='Ward A'
        )
        self.admin = User.objects.create_user(
            username='testadmin',
            password='testpass123',
            full_name='Test Admin',
            role='admin',
            department='Administration'
        )

    def test_user_is_admin_false(self):
        self.assertFalse(self.user.is_admin())

    def test_user_is_admin_true(self):
        self.assertTrue(self.admin.is_admin())

    def test_user_str(self):
        self.assertEqual(str(self.user), 'testuser')

    def test_user_full_name(self):
        self.assertEqual(self.user.full_name, 'Test User')

    def test_user_department(self):
        self.assertEqual(self.user.department, 'Ward A')


class TestProjectModel(TestCase):

    def setUp(self):
        self.admin = User.objects.create_user(
            username='testadmin',
            password='testpass123',
            full_name='Test Admin',
            role='admin',
            department='Administration'
        )
        self.project = Project.objects.create(
            name='Ward A — General Medicine',
            description='General medicine ward',
            created_by=self.admin
        )

    def test_project_str(self):
        self.assertEqual(str(self.project), 'Ward A — General Medicine')

    def test_project_created_by(self):
        self.assertEqual(self.project.created_by, self.admin)


class TestTaskModel(TestCase):

    def setUp(self):
        self.admin = User.objects.create_user(
            username='testadmin',
            password='testpass123',
            full_name='Test Admin',
            role='admin',
            department='Administration'
        )
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            full_name='Test User',
            role='user',
            department='Ward A'
        )
        self.project = Project.objects.create(
            name='Ward A',
            description='Test ward',
            created_by=self.admin
        )
        self.task = Task.objects.create(
            title='Morning medication round',
            description='Administer medications',
            due_date=timezone.now() + timedelta(hours=2),
            priority='High',
            status='Pending',
            project=self.project,
            assigned_to=self.user,
            created_by=self.admin
        )
        self.overdue_task = Task.objects.create(
            title='Overdue task',
            description='This is overdue',
            due_date=timezone.now() - timedelta(hours=1),
            priority='High',
            status='Pending',
            project=self.project,
            assigned_to=self.user,
            created_by=self.admin
        )

    def test_task_str(self):
        self.assertEqual(str(self.task), 'Morning medication round')

    def test_task_is_overdue_false(self):
        self.assertFalse(self.task.is_overdue())

    def test_task_is_overdue_true(self):
        self.assertTrue(self.overdue_task.is_overdue())

    def test_task_priority(self):
        self.assertEqual(self.task.priority, 'High')

    def test_task_status(self):
        self.assertEqual(self.task.status, 'Pending')


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(
            username='testadmin',
            password='testpass123',
            full_name='Test Admin',
            role='admin',
            department='Administration'
        )

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_task_list_requires_login(self):
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 302)

    def test_project_list_requires_login(self):
        response = self.client.get(reverse('project_list'))
        self.assertEqual(response.status_code, 302)

    def test_staff_list_requires_login(self):
        response = self.client.get(reverse('staff_list'))
        self.assertEqual(response.status_code, 302)

    def test_login_with_valid_credentials(self):
        response = self.client.post(reverse('login'), {
            'username': 'testadmin',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)

    def test_logout_redirects(self):
        self.client.login(username='testadmin', password='testpass123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)