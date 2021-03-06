from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'game_planner_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('players/', views.PlayersListView.as_view(), name='players'),
    path('profile/<str:pk>', views.ProfileView.as_view(), name='profile'),
    path('manage_profile/', views.manage_profile, name='manage_profile'),
    path('create_game/', views.create_game, name='create_game'),
    path('games/', login_required(views.GamesListView.as_view()), name='games'),
    path('games/<str:pk>/', views.game_detail, name='game_detail'),
    path('manage_game/<str:pk>/', views.manage_game, name='manage_game'),
    path('friend_requests/', views.friend_requests, name='friend_requests'),
    path('notification_read/', views.notification_read, name='notification_read'),
    path('mark_all_as_read/', views.mark_all_as_read, name='mark_all_as_read'),
    path('manage_participation/', views.manage_participation, name='manage_participation'),
]