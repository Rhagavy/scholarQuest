import imp
from django.urls import path,include
from .import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.homePage, name="home"),
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('profile/', views.profilePage, name="profile"),
    path('create-course/', views.courseCreation, name="createCourse"),

    #Password reset urls
    # path('password-reset', auth_views.PasswordResetView.as_view(), name="reset_password"),

    # path('password-reset-sent', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),

    # path('password-reset/<uid64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),

    # path('password-reset-complete', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    path('', include('django.contrib.auth.urls')),
    #path(r'^password_reset/$', auth_views.password_reset),
    # path(r'^password_reset/$', auth_views.password_reset, name='password_reset'), 
    # path(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'), 
    # path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, name='password_reset_confirm'), 
    # path(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
]