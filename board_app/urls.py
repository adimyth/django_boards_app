from django.urls import path, re_path

from board_app.views import PostsUpdateView, PostsDeleteView, AccountUpdateView
from . import views


app_name = 'board_app'
# (?P < name > pattern)
urlpatterns = [
    path('', views.home, name='home'),
    re_path(r'^boards/(?P<pk>\d+)/(?P<slug>[\w-]+)/$', views.board_topics, name='topics'),
    re_path(r'^boards/(?P<pk>\d+)/new$', views.new_topic, name='new_topic'),
    re_path(r'^boards/(?P<pk>\d+)/(?P<board_slug>[\w-]+)/(?P<topic_id>\d+)/(?P<topic_slug>[\w-]+)$', views.posts, name='posts'),
    re_path(r'^boards/(?P<pk>\d+)/(?P<board_slug>[\w-]+)/(?P<topic_id>\d+)/(?P<topic_slug>[\w-]+)/reply$', views.posts_reply, name='posts_reply'),
    re_path(r'^boards/(?P<pk>\d+)/(?P<board_slug>[\w-]+)/(?P<topic_id>\d+)/(?P<topic_slug>[\w-]+)/edit/(?P<post_id>\d+)$', PostsUpdateView.as_view(), name='posts_edit'),
    re_path(r'^boards/(?P<pk>\d+)/(?P<board_slug>[\w-]+)/(?P<topic_id>\d+)/(?P<topic_slug>[\w-]+)/delete/(?P<post_id>\d+)$', PostsDeleteView.as_view(),
            name='posts_delete'),
    re_path(r'^account/', AccountUpdateView.as_view(), name='account')
]
