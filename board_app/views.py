from django.contrib.auth.models import User
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.utils.decorators import method_decorator

from board_app.forms import PostsReplyForm, UserUpdateForm
from board_app.models import Post, Topic
from .models import Board
from .forms import NewTopicForm
from django.contrib.postgres.search import SearchVector
from django.views.generic.edit import UpdateView, DeleteView


@login_required(login_url='/login/')
def home(request):
    all_boards = Board.objects.all()
    if request.method == 'POST':
        query = request.POST.get("search")
        if query != '':
            all_boards = Board.objects.annotate(search=SearchVector('name', 'description'),).filter(search=query)
    all_boards = sorted(list(all_boards),  key=lambda x: x.name)
    return render(request, 'board_app/board.html', {'all_boards': all_boards})


@login_required(login_url='/login/')
def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'board_app/topics.html', {'board': board})


# redirect to all topics when just button is clicked
# redirect to all topics when proper form is filled
# redirect to new_topics page when just spaces are passed as input
@login_required(login_url='/login/')
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user = request.user
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            print(f"USER: {user}")
            topic = form.save(commit=False)
            topic.board = board
            topic.created_by = user
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
            url = reverse('board_app:topics', kwargs={'pk': board.id})
            return redirect(url)
    else:
        form = NewTopicForm()
    return render(request, 'board_app/new_topic.html', {'board': board, 'form': form})


@login_required(login_url='/login/')
def posts(request, pk, topic_id):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_id)
    topic.views += 1
    topic.save()
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'board_app/posts.html', {'board': board, 'topic': topic})


@login_required(login_url='/login/')
def posts_reply(request, pk, topic_id):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_id)
    board = get_object_or_404(Board, pk=pk)
    user = request.user
    if request.method == 'POST':
        form = PostsReplyForm(request.POST)
        if form.is_valid():
            topic = get_object_or_404(Topic, board__pk=pk, pk=topic_id)
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
            url = reverse('board_app:posts', kwargs={'pk': board.id, 'topic_id': topic.id})
            return redirect(url)
    else:
        form = PostsReplyForm()
    return render(request, 'board_app/posts_reply.html', {'board': board, 'form': form, 'topic': topic})


@login_required(login_url='/login/')
def posts_edit(request, pk, topic_id, post_id):
    board = Board.objects.get(pk=pk)
    topic = Topic.objects.get(pk=topic_id)
    post = Post.objects.get(pk=post_id)
    form = PostsReplyForm()
    return render(request, 'board_app/edit.html', {'form': form, 'board': board, 'topic': topic, 'post': post})
    # return HttpResponse(f'This is the edit page for {board.name}, {topic.subject}, {post.message}')


class PostsUpdateView(UpdateView):
    model = Post
    form_class = PostsReplyForm
    pk_url_kwarg = 'post_id'
    template_name = 'board_app/edit.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super(PostsUpdateView, self).get_context_data(**kwargs)
        context['board'] = Board.objects.get(pk=self.kwargs.get('pk'))
        context['topic'] = Topic.objects.get(pk=self.kwargs.get('topic_id'))
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_at = timezone.now()
        post.save()
        url = reverse('board_app:posts', kwargs={'pk': post.topic.board.id,
                                                 'topic_id': post.topic.id,
                                                 })
        return redirect(url)


# The method_decorator decorator transforms a function decorator into a method decorator
# so that it can be used on an instance method
@method_decorator(login_required, name='dispatch')
class AccountUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    context_object_name = 'post'
    template_name = 'board_app/account.html'

    def get_object(self):
        print(f"User: {self.request.user.first_name}")
        return self.request.user

    def form_valid(self, form):
        form.save()
        url = reverse('board_app:home')
        return redirect(url)


@method_decorator(login_required, name='dispatch')
class PostsDeleteView(DeleteView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'board_app/posts.html'
    context_object_name = 'post'

    def get_success_url(self):
        return reverse('board_app:posts', kwargs={'pk': self.kwargs.get('pk'),
                                                  'topic_id': self.kwargs.get('topic_id')
                                                  })
