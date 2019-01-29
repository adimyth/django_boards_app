from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'user_accounts_app'
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user_accounts_app/login.html'), name='logout'),
    path('login/', views.login_form, name='login'),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='user_accounts_app/password_reset_form.html',
             email_template_name='user_accounts_app/password_reset_email.html',
             subject_template_name='user_accounts_app/password_reset_subject.txt'
         ),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='user_accounts_app/password_reset_done.html'),
        name='password_reset_done'),
    re_path('reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
            auth_views.PasswordResetConfirmView.as_view(template_name='user_accounts_app/password_reset_confirm.html'),
            name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='user_accounts_app/password_reset_complete.html'),
         name='password_reset_complete'),
]
