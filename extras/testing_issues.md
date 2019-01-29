Writing tests for views that work only for valid users, required me to simulate the login process.
Initial solution
```python
from django.contrib.auth.models import User
from django.test import Client

user = User.objects.create(username='testuser', password='12345')

c = Client()
logged_in = c.login(username='testuser', password='12345')
```

Why doesn't it work?
In the snippet above, when the User is created the actual password hash is set to be 12345. When the client calls the login method, the value of the password argument, 12345, is passed through the hash function, resulting in something like

hash('12345') = 'adkfh5lkad438....'
This is then compared to the hash stored in the database, and the client is denied access because 'adkfh5lkad438....' != '12345'

Final solution
```python
user = User.objects.create(username='testuser')
user.set_password('12345')
user.save()

c = Client()
logged_in = c.login(username='testuser', password='12345')
```

You cannot call a function that requires arguments in a template. Write a template tag or filter instead.
So, you need to be smart about it. Make use of __str__ function & overwrite it, so that it returns the most important aspect of the database model.
Then, you can use it in another functions, belonging to the same class.
Example
```python
from django.db import models

class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()

```