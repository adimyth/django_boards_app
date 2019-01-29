from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse, resolve
from django.test import Client

from board_app.models import Topic, Post
from board_app.views import posts
from .models import Board
from django.contrib.auth.models import User
from .views import board_topics


class HomeTests(TestCase):
    fixtures = ['board_app/fixtures/board_app.json']

    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board.')
        self.homepage_url = reverse('board_app:home')
        self.signup_page_url = reverse('user_accounts_app:signup')
        self.login_page_url = reverse('user_accounts_app:login')
        self.password_reset_page_url = reverse('user_accounts_app:password_reset')
        user = User.objects.create(username='john_doe')
        user.set_password('john@123')
        user.save()

    def test_redirection_to_home_page_for_valid_user_returns_httpresponse(self):
        client = Client()
        client.login(username='john_doe', password='john@123')
        response = client.get(reverse('board_app:home'))
        self.assertTrue(type(response), HttpResponse)

    def test_redirection_to_login_page_for_invalid_user_returns_none(self):
        client = Client()
        response = client.get(reverse('board_app:home'))
        self.assertTrue(response, None)

    def test_home_page_status_code(self):
        client = Client()
        client.login(username='john_doe', password='john@123')
        response = client.get(reverse('board_app:home'))
        self.assertEquals(response.status_code, 200)

    def test_home_board_list_size(self):
        client = Client()
        client.login(username='john_doe', password='john@123')
        response = client.get(reverse('board_app:home'))
        self.assertGreater(len(response.context['all_boards']), 0)

    def test_home_page_contains_link_to_topics_page(self):
        client = Client()
        client.login(username='john_doe', password='john@123')
        response = client.get(reverse('board_app:home'))
        board_topics_url = reverse('board_app:topics', kwargs={'pk': self.board.id})
        self.assertContains(response, f'href="{board_topics_url}"')


class TopicTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django Testing', description='A sample board for testing the boards django app')
        user = User.objects.create(username='john_doe')
        user.set_password('john@123')
        user.save()

    def test_topics_page_200_status_code(self):
        client = Client()
        client.login(username='john_doe', password='john@123')
        response = client.get(reverse('board_app:topics', kwargs={'pk': self.board.id}))
        self.assertEquals(response.status_code, 200)

    def test_topics_page_404_status_code(self):
        client = Client()
        client.login(username='john_doe', password='john@123')
        response = client.get(reverse('board_app:topics', kwargs={'pk': 100}))
        self.assertEquals(response.status_code, 404)

    def test_topics_page_views(self):
        url = reverse('board_app:topics', kwargs={'pk': self.board.id})
        func, args, kwargs = resolve(url)
        self.assertEqual(func, board_topics)

    def test_topics_page_contains_link_to_homepage_and_new_topic(self):
        client = Client()
        client.login(username='john_doe', password='john@123')
        home_url = reverse('board_app:home')
        topics_url = reverse('board_app:topics', kwargs={'pk': self.board.id})
        new_topics_url = reverse('board_app:new_topic', kwargs={'pk': self.board.id})
        response = client.get(topics_url)
        self.assertContains(response, f'href="{home_url}"')
        self.assertContains(response, f'href="{new_topics_url}"')


class NewTopicTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='New Topics Testing Board', description='A board to test new topics page')
        user = User.objects.create(username='john_doe')
        user.set_password('john@123')
        user.save()

    def test_new_topic_user_authenticated(self):
        client = Client()
        client.login(username='john_doe', password='john@123')
        url = reverse('board_app:new_topic', kwargs={'pk': self.board.id})
        response = client.get(url)
        self.assertTrue(response.__dict__['context']['user'].is_authenticated)

    def test_new_topic_valid_board(self):
        client = Client()
        client.login(username='john_doe', password='john@123')
        url = reverse('board_app:new_topic', kwargs={'pk': self.board.id})
        response = client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_topic_invalid_board(self):
        client = Client()
        client.login(username='john_doe', password='john@123')
        url = reverse('board_app:new_topic', kwargs={'pk': 99})
        response = client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_new_topic_contains_link_to_board(self):
        client = Client()
        client.login(username='john_doe', password='john@123')
        board_topics_url = reverse('board_app:topics', kwargs={'pk': self.board.id})
        new_topics_url = reverse('board_app:new_topic', kwargs={'pk': self.board.id})
        response = client.get(new_topics_url)
        self.assertContains(response, f'href="{board_topics_url}"')

    def test_new_topic_csrf_on_submission(self):
        client = Client()
        client.login(username='john_doe', password='john@123')
        url = reverse('board_app:new_topic', kwargs={'pk': self.board.id})
        response = client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_topic_valid_form_data(self):
        client = Client()
        client.login(username='john_doe', password='john@123')
        sub = 'Test'
        msg = 'This is a test message'
        url = reverse('board_app:new_topic', kwargs={'pk': self.board.id})
        client.post(url, {'subject': sub, 'message': msg})
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Topic.objects.filter(subject=sub))
        self.assertTrue(Post.objects.filter(message=msg))

    def test_new_topic_invalid_form_data(self):
        client = Client()
        client.login(username='john_doe', password='john@123')
        url = reverse('board_app:new_topic', kwargs={'pk': self.board.id})
        response = client.post(url, {'subject': '', 'message': ''})
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, url)

    # simulating just the submit button click
    def test_new_topic_empty_form_data(self):
        client = Client()
        client.login(username='john_doe', password='john@123')
        url = reverse('board_app:new_topic', kwargs={'pk': self.board.id})
        response = client.post(url, {})
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, url)


class PostPageTests(TestCase):
    def setUp(self):
        user = User.objects.create(username='john_doe')
        user.set_password('john@123')
        user.save()
        self.board = Board.objects.create(name='Django Test board', description='A test board for testing posts page')
        self.topic = Topic.objects.create(subject='Welcome to app', board=self.board, created_by=user)
        Post.objects.create(message='Just a test post', topic=self.topic, created_by=user)
        self.topic_url = reverse('board_app:topics', kwargs={'pk': self.board.id})

    def test_post_page_contains_reply_button(self):
        client = Client()
        client.login(username='john_doe', password='john@123')
        url = reverse('board_app:posts', kwargs={'pk': self.board.id, 'topic_id': self.topic.id})
        response = client.get(url)
        self.assertContains(response, 'Reply')

    def test_post_page_status_code(self):
        client = Client()
        client.login(username='john_doe', password='john@123')
        url = reverse('board_app:posts', kwargs={'pk': self.board.id, 'topic_id': self.topic.id})
        response = client.get(url)
        self.assertTrue(response.status_code, 200)

    def test_post_page_resolves_posts_view(self):
        client = Client()
        client.login(username='john_doe', password='john@123')
        url = reverse('board_app:posts', kwargs={'pk': self.board.id, 'topic_id': self.topic.id})
        func, args, kwargs = resolve(url)
        self.assertEquals(func, posts)

    def test_post_page_contains_one_post_for_user(self):
        client = Client()
        client.login(username='john_doe', password='john@123')
        url = reverse('board_app:posts', kwargs={'pk': self.board.id, 'topic_id': self.topic.id})
        response = client.get(url)
        self.assertContains(response, 'Posts: 1')

    def test_post_page_contains_link_to_topic(self):
        client = Client()
        client.login(username='john_doe', password='john@123')
        url = reverse('board_app:posts', kwargs={'pk': self.board.id, 'topic_id': self.topic.id})
        response = client.get(url)
        self.assertContains(response, f'href="{self.topic_url}"')

    def test_post_page_contains_edit_button_for_test_creator(self):
        client = Client()
        client.login(username='john_doe', password='john@123')
        url = reverse('board_app:posts', kwargs={'pk': self.board.id, 'topic_id': self.topic.id})
        response = client.get(url)
        self.assertContains(response, 'Edit')
