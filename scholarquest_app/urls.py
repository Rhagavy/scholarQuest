import imp
from django.urls import path,include
from .import views

from django.contrib.auth import views as auth_views

#urls for pages
urlpatterns = [
    path('', views.homePage, name="home"),
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('profile/<str:pk>', views.profilePage, name="profile"),
    path('profile/edit-profile/<str:pk>',views.editProfile, name="editProfile"),
    path('create-course/', views.courseCreation, name="createCourse"),
    path('current-courses/', views.currentCourse, name="currentCourses"),
    path('edit-course/<str:pk>', views.editCourse, name="editCourse"),
    path('user-dash/',views.userDash, name="userDash"),
    path('important-dates/',views.importantDates ,name="importantDates"),
    path('important-dates/<str:frq>',views.importantDates ,name="importantDates"),
    path('edit-tasks/<str:pk>', views.editTasks, name="editTasks"),
    

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