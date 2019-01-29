from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from markdown import markdown


class Board(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_topics_count(self):
        board = Board.objects.get(name=self)
        return board.topics.count()

    def get_posts_count(self):
        board = Board.objects.get(name=self)
        return Post.objects.filter(topic__board=board).count()

    def get_latest_post_created_at(self):
        board = Board.objects.get(name=self)
        return Post.objects.values_list('created_at', flat=True).filter(topic__board=board).order_by('created_at').last()

    def get_latest_post_created_by(self):
        board = Board.objects.get(name=self)
        try:
            return Post.objects.filter(topic__board=board).order_by('created_at').last().created_by
        except Exception:
            pass


class Topic(models.Model):

    class Meta:
        ordering = ['-views']

    subject = models.CharField(max_length=100)
    last_updated = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    board = models.ForeignKey(Board, related_name='topics', on_delete='cascade')
    created_by = models.ForeignKey(User, related_name='topics', on_delete='cascade')

    def __str__(self):
        return self.subject

    def get_posts_count(self):
        topic = Topic.objects.get(subject=self)
        return topic.posts.count()


class Post(models.Model):
    class Meta:
        ordering = ['-created_at']

    message = models.TextField(max_length=100)
    topic = models.ForeignKey(Topic, related_name='posts', on_delete='cascade')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete='cascade')
    updated_by = models.ForeignKey(User, null=True, on_delete='cascade')

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))

    # def __str__(self):
    #     return self.message
