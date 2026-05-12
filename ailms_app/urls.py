from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload-resume/', views.upload_resume, name='upload_resume'),
    path('courses/', views.courses_list, name='courses_list'),
    path('course/<int:pk>/', views.course_detail, name='course_detail'),
    path('course/<int:course_id>/quiz/', views.take_quiz, name='take_quiz'),
    path('result/<int:result_id>/', views.quiz_result, name='quiz_result'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]
