from django.test import TestCase, Client
from django.shortcuts import reverse
from django.urls import resolve
from .views import login, signup
from django.contrib.auth.models import User


class SignUpPageTests(TestCase):
    def setUp(self):
        self.homepage_url = reverse('board_app:home')
        self.signup_page_url = reverse('user_accounts_app:signup')
        self.login_page_url = reverse('user_accounts_app:login')
        self.client = Client()

    def test_signup_page_contains_link_to_login(self):
        response = self.client.get(self.signup_page_url)
        self.assertContains(response, f'href="{self.login_page_url}"')

    def test_signup_page_on_valid_data_contains_link_to_homepage(self):
        response = self.client.post(self.signup_page_url, data={'username': 'john_doe',
                                                                'first_name': 'John',
                                                                'last_name': 'Doe',
                                                                'email': 'john@gmail.com',
                                                                'password1': 'john@123',
                                                                'password2': 'john@123'
                                                                })
        self.assertTrue(response.status_code, 200)
        self.assertContains(response, f'href="{self.homepage_url}"')  # check for link to homepage
        self.assertTrue(User.objects.exists())  # check if user has been added

    def test_signup_page_contains_invalid_data(self):
        response = self.client.post(self.signup_page_url, data={'username': '!3@#$%^&',
                                                                'first_name': '',
                                                                'last_name': 'something',
                                                                'password1': 'asdfvasd',
                                                                'password2': '12345'
                                                                })
        self.assertContains(response, f'href="{self.login_page_url}"')  # stays on the same page
        self.assertFalse(User.objects.filter(username='!3@#$%^&'))  # no user has been added

    def test_signup_page_contains_empty_data(self):
        response = self.client.post(self.signup_page_url, data={'username': '',
                                                                'first_name': '',
                                                                'last_name': '',
                                                                'password1': '',
                                                                'password2': ''
                                                                })
        func, args, kwargs = resolve(self.signup_page_url)
        self.assertContains(response, f'href="{self.login_page_url}"')  # stays on the same page
        self.assertFalse(User.objects.exists())  # no user has been added
        self.assertTrue(func, signup)    # login view is called


class LoginPageTests(TestCase):
    def setUp(self):
        self.homepage_url = reverse('board_app:home')
        self.signup_page_url = reverse('user_accounts_app:signup')
        self.login_page_url = reverse('user_accounts_app:login')
        self.password_reset_page_url = reverse('user_accounts_app:password_reset')
        self.client = Client()
        self.user = User.objects.create_user(username='john_doe', first_name='John', last_name='Doe',
                                             email='john@gmail.com', password='john@123')

    def test_login_page_redirects_to_homepage(self):
        response = self.client.post(self.login_page_url, {'username': 'john_doe',
                                                          'password': 'john@123'})
        self.assertTrue(response.status_code, 302)
        self.assertRedirects(response, self.homepage_url)

    def test_login_page_contains_link_to_signup(self):
        response = self.client.get(self.login_page_url)
        self.assertContains(response, f'href="{self.signup_page_url}"')

    def test_login_page_invalid_data(self):
        response = self.client.post(self.login_page_url, {'username': '', 'password': ''})
        self.assertFalse(response.__dict__['context']['form'].is_valid())
        self.assertContains(response, self.signup_page_url)
        self.assertTrue(response.status_code, 200)

    def test_login_page_resolves_login_view(self):
        func, args, kwargs = resolve(self.signup_page_url)
        self.assertTrue(func, login)

    def test_login_page_contains_link_to_password_reset_page(self):
        response = self.client.get(self.login_page_url)
        self.assertContains(response, self.password_reset_page_url)


class LogoutPageTests(TestCase):
    def setUp(self):
        user = User.objects.create(username='john_doe')
        user.set_password('john@123')
        user.save()
        self.login_url = reverse('user_accounts_app:login')
        self.logout_url = reverse('user_accounts_app:logout')
        self.client = Client()
        self.client.login(username='john_doe', password='john@123')

    def test_logout_has_no_user_as_john(self):
        response = self.client.get(self.logout_url)
        self.assertEquals(response.context, None)

    def test_logout_page_status_code(self):
        response = self.client.get(self.logout_url)
        self.assertTrue(response.status_code, 302)

    def test_logout_page_redirects_to_login_page(self):
        response = self.client.get(self.logout_url)
        self.assertEquals(response.url, '/login/')
