from django.urls import path, re_path

from board_app.views import PostsUpdateView, PostsDeleteView, AccountUpdateView
from . import views


app_name = 'board_app'
# (?P < name > pattern)
urlpatterns = [
    path('boards/', views.home, name='home'),
    re_path(r'^boards/(?P<pk>\d+)$', views.board_topics, name='topics'),
    re_path(r'^boards/(?P<pk>\d+)/new$', views.new_topic, name='new_topic'),
    re_path(r'^boards/(?P<pk>\d+)/topics/(?P<topic_id>\d+)$', views.posts, name='posts'),
    re_path(r'^boards/(?P<pk>\d+)/topics/(?P<topic_id>\d+)/reply$', views.posts_reply, name='posts_reply'),
    re_path(r'^boards/(?P<pk>\d+)/topics/(?P<topic_id>\d+)/edit/(?P<post_id>\d+)$', PostsUpdateView.as_view(), name='posts_edit'),
    re_path(r'^boards/(?P<pk>\d+)/topics/(?P<topic_id>\d+)/delete/(?P<post_id>\d+)$', PostsDeleteView.as_view(),
            name='posts_delete'),
    re_path(r'^account/', AccountUpdateView.as_view(), name='account')
]
