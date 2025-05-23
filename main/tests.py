from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Point, Table, CalculationResult, Post, Profile
from .forms import RegisterForm, LoginForm, PostForm, GraphForm
from . import gauss, gauss_step, gradient
import json

class FullCoverageTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.point = Point.objects.create(x_value=0.4, y_value=1.2)
        self.table = Table.objects.create(title='Тестовая таблица', solution='x+y', temperature=298)
        self.table.points.add(self.point)
        self.result = CalculationResult.objects.create(
            user=self.user,
            title='Тестовый расчет',
            param_a=1.0,
            param_b=2.0,
            table=self.table,
            iterations=10,
            exec_time=0.5,
            algorithm='TestAlgo',
            average_op=5.5,
            table_data=json.dumps([{"x2": 0.4, "gmod": 1.1, "gexp": 1.2, "sigma": 5.0, "delta": 0.1}])
        )

    def test_forum_list_view(self):
        Post.objects.create(title='Форум', content='Контент', author=self.user)
        response = self.client.get(reverse('forum_list'))
        self.assertEqual(response.status_code, 200)

    def test_forum_detail_view(self):
        post = Post.objects.create(title='Подробно', content='Контент', author=self.user, calculation_result=self.result)
        response = self.client.get(reverse('forum_detail', args=[post.id]))
        self.assertEqual(response.status_code, 200)

    def test_forum_delete_view(self):
        post = Post.objects.create(title='Удаление', content='...', author=self.user)
        response = self.client.post(reverse('forum_delete', args=[post.id]))
        self.assertEqual(response.status_code, 302)

    def test_profile_view(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_home_page_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_register_form_valid(self):
        form = RegisterForm(data={
            'username': 'newuser',
            'email': 'test@example.com',
            'password1': 'abc123def456',
            'password2': 'abc123def456',
        })
        self.assertTrue(form.is_valid())

    def test_login_form_valid(self):
        form = LoginForm(data={'username': 'testuser', 'password': '12345'})
        self.assertTrue(form.is_valid())

    def test_post_form_invalid_missing_title(self):
        form = PostForm(data={'content': 'текст'})
        self.assertFalse(form.is_valid())

    def test_graph_form_initialization(self):
        form = GraphForm(initial={
            'parameter_a': 1.0,
            'parameter_b': 2.0,
            'table_choice': str(self.table.id),
        })
        self.assertEqual(form.initial['parameter_a'], 1.0)

    def test_get_table_data_valid_json(self):
        data = self.result.get_table_data()
        self.assertIsInstance(data, list)

    def test_get_table_data_invalid_json(self):
        self.result.table_data = 'not-a-json'
        self.result.save()
        self.assertEqual(self.result.get_table_data(), 'not-a-json')

    def test_logout_view(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_str_point(self):
        self.assertEqual(str(self.point), "0.4, 1.2")

    def test_str_table(self):
        self.assertEqual(self.table.title, "Тестовая таблица")

    def test_str_result(self):
        self.assertIn("testuser", str(self.result))

    def test_post_str(self):
        post = Post.objects.create(title='Тестовый пост', content='...', author=self.user)
        self.assertEqual(str(post), 'Тестовый пост')

    def test_profile_str(self):
        profile, _ = Profile.objects.get_or_create(user=self.user)
        self.assertEqual(str(profile), f"Profile of {self.user.username}")

    def test_forum_create_view_get(self):
        response = self.client.get(reverse('forum_create'))
        self.assertEqual(response.status_code, 200)

    def test_forum_edit_view_get(self):
        post = Post.objects.create(title='Редактировать', content='...', author=self.user)
        response = self.client.get(reverse('forum_edit', args=[post.id]))
        self.assertEqual(response.status_code, 200)

    def test_forum_edit_view_post_invalid(self):
        post = Post.objects.create(title='Редактировать', content='...', author=self.user)
        response = self.client.post(reverse('forum_edit', args=[post.id]), data={'title': '', 'content': 'Обновлено'})
        self.assertEqual(response.status_code, 200)

    def test_forum_list_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('forum_list'))
        self.assertEqual(response.status_code, 302)

    def test_profile_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)

    def test_create_post_form_valid(self):
        form = PostForm(data={'title': 'Заголовок', 'content': 'Контент'}, user=self.user)
        self.assertTrue(form.is_valid())

    def test_create_post_form_invalid_empty(self):
        form = PostForm(data={}, user=self.user)
        self.assertFalse(form.is_valid())

    def test_post_form_has_fields(self):
        form = PostForm(user=self.user)
        self.assertIn('title', form.fields)
        self.assertIn('content', form.fields)

    def test_gauss_algorithm_output(self):
        result = gauss.gauss([self.table], 0)
        a, b, iterations, exec_time, *_ = result
        self.assertIsInstance(a, float)
        self.assertIsInstance(b, float)
        self.assertIsInstance(iterations, int)
        self.assertGreater(exec_time, 0)

    def test_gauss_step_algorithm_output(self):
        result = gauss_step.gauss_step([self.table], 0)
        a, b, iterations, exec_time, *_ = result
        self.assertIsInstance(a, float)
        self.assertIsInstance(b, float)
        self.assertIsInstance(iterations, int)
        self.assertGreater(exec_time, 0)


