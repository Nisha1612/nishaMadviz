from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('team/', views.team, name='team'),
    path('service/', views.service, name='service'),
    path('question/', views.question, name='question'),
    path('find_hospital/', views.find_hospital, name='find_hospital'),
    path('Team.html', views.redirect_team),
    path('service.html', views.redirect_service),
    path('question.html', views.redirect_question),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('user_home/', views.user_home, name='user_home'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('setting/', views.user_setting, name='settings'),
    path('user_dashboard/', views.user_dashboard, name='dashboard'),
    path('ai_usecase/<uuid:id>/', views.ai_usecase_detail, name='ai_usecase_detail'),

  
]
