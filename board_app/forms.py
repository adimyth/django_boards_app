from django import forms
from django.contrib.auth.models import User

from board_app.models import Post
from .models import Topic


# ModelForm is used to create forms from django models
class NewTopicForm(forms.ModelForm):
    message = forms.CharField(label='Message', label_suffix='', max_length=400, help_text="Max length is 4000")
    message.widget.attrs.update({'class': 'materialize-textarea'})

    class Meta:
        model = Topic
        fields = ['subject', 'message']


class PostsReplyForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message']


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
