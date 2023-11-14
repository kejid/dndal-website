# dndapp/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # Import views from your app

urlpatterns = [
    # path('', views.homepage, name='homepage'),  # Define the homepage URL pattern
    path('', views.upcoming_games, name='upcoming_games'),
    path('upcoming_games/', views.upcoming_games, name='upcoming_games'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('users/', views.users_view, name='users'),
    path('accounts/profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('character/create/', views.create_character, name='create_character'),
    path('character/edit/<int:character_id>/', views.edit_character, name='edit_character'),
    path('character_list/', views.character_list, name='character_list'),
    path('game-session/create/', views.create_game_session, name='create_game_session'),
    path('game-session/edit/<int:session_id>/', views.edit_game_session, name='edit_game_session'),
    path('review/create/', views.create_player_review, name='create_player_review'),
    path('notifications/', views.view_notifications, name='view_notifications'),
    path('notifications/read/<int:notification_id>/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('character/logs/<int:character_id>/', views.view_character_logs, name='view_character_logs'),
    path('character/<int:character_id>/gamelog/add/', views.add_or_edit_gamelog, name='add_gamelog'),
    path('character/<int:character_id>/gamelog/edit/<int:log_id>/', views.add_or_edit_gamelog, name='edit_gamelog'),
    path('character/<int:character_id>/tradelog/add/', views.add_or_edit_tradelog, name='add_tradelog'),
    path('character/<int:character_id>/tradelog/edit/<int:log_id>/', views.add_or_edit_tradelog, name='edit_tradelog'),
    path('character/<int:character_id>/downtimelog/add/', views.add_or_edit_downtimelog, name='add_downtimelog'),
    path('character/<int:character_id>/downtimelog/edit/<int:log_id>/', views.add_or_edit_downtimelog, name='edit_downtimelog'),
    path('profile/privacy-settings/', views.edit_privacy_settings, name='edit_privacy_settings'),
    path('review/add/<int:session_id>/', views.add_player_review, name='add_player_review'),
    path('user-statistics/<int:user_id>/', views.view_user_statistics, name='view_user_statistics'),
    path('game-statistics/<int:session_id>/', views.view_game_statistics, name='view_game_statistics'),
    path('complaints/submit/', views.submit_complaint, name='submit_complaint'),
    path('complaints/view/', views.view_complaints, name='view_complaints'),
    path('game-session/apply/<int:session_id>/', views.apply_to_game, name='apply_to_game'),
    path('game-sessions/create/', views.create_game_session, name='create_game_session'),
    path('game-sessions/edit/<int:session_id>/', views.edit_game_session, name='edit_game_session'),
    path('game-sessions/', views.game_sessions, name='game_sessions'),
]
