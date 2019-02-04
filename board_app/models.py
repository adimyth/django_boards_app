from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from markdown import markdown
from django.utils.text import slugify


# 1. fields of the model
# 2. Meta
# 3. def __str__
# 4. other special methods
# 5. save
# 6. other methods
class Board(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100)
    slug = models.SlugField(null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Board, self).save(*args, **kwargs)

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
        except Exception as e:
            print(f"Exception: {e}")


class Topic(models.Model):
    subject = models.CharField(max_length=100)
    last_updated = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    board = models.ForeignKey(Board, related_name='topics', on_delete='cascade')
    created_by = models.ForeignKey(User, related_name='topics', on_delete='cascade')
    slug = models.SlugField(null=True)

    class Meta:
        ordering = ['-views']

    def __str__(self):
        return self.subject

    def save(self, *args, **kwargs):
        self.slug = slugify(self)
        super(Topic, self).save(*args, **kwargs)

    def get_posts_count(self):
        topic = Topic.objects.get(subject=self)
        return topic.posts.count()


class Post(models.Model):
    message = models.TextField(max_length=100)
    topic = models.ForeignKey(Topic, related_name='posts', on_delete='cascade')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete='cascade')
    updated_by = models.ForeignKey(User, null=True, on_delete='cascade')

    class Meta:
        ordering = ['-created_at']

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))
