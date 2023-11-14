# dndapp/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .forms import CustomUserCreationForm, UserProfileEditForm, CharacterForm, GameSessionForm, PlayerReviewForm, GameLogForm, TradeLogForm, DowntimeLogForm, UserProfilePrivacyForm, ComplaintForm, GameApplicationForm, GameSessionCompletionForm
from .models import UserProfile, Character, GameSession, Notification, GameLog, TradeLog, DowntimeLog, UserStatistics, GameStatistics, Complaint

def create_character(request):
    if request.method == 'POST':
        form = CharacterForm(request.POST)
        if form.is_valid():
            character = form.save(commit=False)
            character.user = request.user
            character.save()
            return redirect('character_detail', character.id)
    else:
        form = CharacterForm()
    return render(request, 'dndapp/create_character.html', {'form': form})

def edit_character(request, character_id):
    character = get_object_or_404(Character, id=character_id, user=request.user)
    if request.method == 'POST':
        form = CharacterForm(request.POST, instance=character)
        if form.is_valid():
            form.save()
            return redirect('character_detail', character.id)
    else:
        form = CharacterForm(instance=character)
    return render(request, 'dndapp/edit_character.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Additional logic if needed
            return JsonResponse({'success': True})
        else:
            # Form is not valid
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def edit_profile(request):
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = UserProfileEditForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileEditForm(instance=request.user.profile)
    return render(request, 'dndapp/edit_profile.html', {'form': form})

def user_profile(request):
    return render(request, 'dndapp/user_profile.html', {'user': request.user})

def create_game_session(request):
    if request.method == 'POST':
        form = GameSessionForm(request.POST)
        if form.is_valid():
            game_session = form.save(commit=False)
            game_session.master = request.user
            game_session.save()
            form.save_m2m()  # Required for ManyToMany fields
            return redirect('game_session_detail', game_session.id)
    else:
        form = GameSessionForm()
    return render(request, 'dndapp/create_game_session.html', {'form': form})

def edit_game_session(request, session_id):
    game_session = get_object_or_404(GameSession, id=session_id)

    if request.method == 'POST':
        form = GameSessionForm(request.POST, request.FILES, instance=game_session)
        if form.is_valid():
            form.save()
            return redirect('game_sessions')
    else:
        form = GameSessionForm(instance=game_session)

    return render(request, 'dndapp/edit_game_session.html', {'form': form, 'game_session': game_session})

def game_sessions(request):
    game_sessions = GameSession.objects.all()
    return render(request, 'dndapp/game_sessions.html', {'game_sessions': game_sessions})

def create_player_review(request):
    if request.method == 'POST':
        form = PlayerReviewForm(request.POST)
        if form.is_valid():
            player_review = form.save(commit=False)
            player_review.reviewer = request.user
            player_review.save()
            return redirect('review_detail', player_review.id)
    else:
        form = PlayerReviewForm()
    return render(request, 'dndapp/create_player_review.html', {'form': form})

def add_player_review(request, session_id):
    game_session = get_object_or_404(GameSession, id=session_id)
    if request.method == 'POST':
        form = PlayerReviewForm(request.POST)
        if form.is_valid():
            player_review = form.save(commit=False)
            player_review.reviewer = request.user
            player_review.game_session = game_session
            player_review.save()
            return redirect('game_session_detail', session_id)
    else:
        form = PlayerReviewForm(initial={'game_session': game_session})
    return render(request, 'dndapp/add_player_review.html', {'form': form, 'game_session': game_session})

def view_notifications(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    return render(request, 'dndapp/notifications.html', {'notifications': notifications})

def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    return redirect('view_notifications')

def view_character_logs(request, character_id):
    character = get_object_or_404(Character, id=character_id, user=request.user)
    game_logs = GameLog.objects.filter(character=character).order_by('-date_played')
    trade_logs = TradeLog.objects.filter(character=character).order_by('-trade_date')
    downtime_logs = DowntimeLog.objects.filter(character=character).order_by('-log_date')

    return render(request, 'dndapp/character_logs.html', {
        'character': character,
        'game_logs': game_logs,
        'trade_logs': trade_logs,
        'downtime_logs': downtime_logs
    })

def add_or_edit_gamelog(request, character_id, log_id=None):
    character = get_object_or_404(Character, id=character_id, user=request.user)
    gamelog = GameLog.objects.get(id=log_id) if log_id else None
    if request.method == 'POST':
        form = GameLogForm(request.POST, instance=gamelog)
        if form.is_valid():
            new_log = form.save(commit=False)
            new_log.character = character
            new_log.save()
            return HttpResponseRedirect(reverse('view_character_logs', args=[character_id]))
    else:
        form = GameLogForm(instance=gamelog)
    return render(request, 'dndapp/edit_gamelog.html', {'form': form, 'character': character})

def add_or_edit_tradelog(request, character_id, log_id=None):
    character = get_object_or_404(Character, id=character_id, user=request.user)
    tradelog = TradeLog.objects.get(id=log_id) if log_id else None
    if request.method == 'POST':
        form = TradeLogForm(request.POST, instance=tradelog)
        if form.is_valid():
            new_log = form.save(commit=False)
            new_log.character = character
            # Update character's downtime
            character.downtime -= new_log.downtime_spent
            character.save()
            new_log.save()
            return HttpResponseRedirect(reverse('view_character_logs', args=[character_id]))
    else:
        form = TradeLogForm(instance=tradelog)
    return render(request, 'dndapp/edit_tradelog.html', {'form': form, 'character': character})

def add_or_edit_downtimelog(request, character_id, log_id=None):
    character = get_object_or_404(Character, id=character_id, user=request.user)
    downtimelog = DowntimeLog.objects.get(id=log_id) if log_id else None
    if request.method == 'POST':
        form = DowntimeLogForm(request.POST, instance=downtimelog)
        if form.is_valid():
            new_log = form.save(commit=False)
            new_log.character = character
            # Update character's downtime
            character.downtime -= new_log.downtime_spent
            character.save()
            new_log.save()
            return HttpResponseRedirect(reverse('view_character_logs', args=[character_id]))
    else:
        form = DowntimeLogForm(instance=downtimelog)
    return render(request, 'dndapp/edit_downtimelog.html', {'form': form, 'character': character})

def edit_privacy_settings(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = UserProfilePrivacyForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = UserProfilePrivacyForm(instance=profile)
    return render(request, 'dndapp/edit_privacy_settings.html', {'form': form})


def view_user_statistics(request, user_id):
    user_statistics = get_object_or_404(UserStatistics, user_id=user_id)
    return render(request, 'dndapp/user_statistics.html', {'user_statistics': user_statistics})

def view_game_statistics(request, session_id):
    game_statistics = get_object_or_404(GameStatistics, game_session_id=session_id)
    return render(request, 'dndapp/game_statistics.html', {'game_statistics': game_statistics})

def submit_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.submitted_by = request.user
            complaint.save()
            return redirect('complaint_submitted')  # Redirect to a confirmation page
    else:
        form = ComplaintForm()
    return render(request, 'dndapp/submit_complaint.html', {'form': form})

def view_complaints(request):
    complaints = Complaint.objects.filter(submitted_by=request.user).order_by('-submitted_on')
    return render(request, 'dndapp/view_complaints.html', {'complaints': complaints})

def complete_game_session(request, session_id):
    game_session = get_object_or_404(GameSession, id=session_id, master=request.user)
    if request.method == 'POST':
        form = GameSessionCompletionForm(request.POST, instance=game_session)
        if form.is_valid():
            form.save()
            # Logic to auto-create GameLog entries and handle rewards
            return redirect('game_session_detail', session_id)
    else:
        form = GameSessionCompletionForm(instance=game_session)
    return render(request, 'dndapp/complete_game_session.html', {'form': form, 'game_session': game_session})

def apply_to_game(request, session_id):
    game_session = get_object_or_404(GameSession, id=session_id)
    if request.method == 'POST':
        form = GameApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.game_session = game_session
            application.player = request.user
            application.save()
            return redirect('game_session_detail', session_id)
    else:
        form = GameApplicationForm()
    return render(request, 'dndapp/apply_to_game.html', {'form': form, 'game_session': game_session})

def homepage(request):
    # Your view logic here
    return render(request, 'home.html')

def character_list(request):
    # Your view logic here
    return render(request, 'character_list.html')

def upcoming_games(request):
    # Your view logic here
    return render(request, 'upcoming_games_template.html')

def users_view(request):
    # Your view logic here
    return render(request, 'users.html')

def profile(request):
    # Add your view logic here
    return render(request, 'profile.html')  