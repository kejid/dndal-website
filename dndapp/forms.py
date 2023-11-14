# dndapp/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, UserProfile, Character, GameSession, PlayerReview, GameLog, TradeLog, DowntimeLog, Complaint, GameApplication

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('notify_on_new_games',)

class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'rating', 'reviews', 'played_games']

class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ['name', 'race', 'classes', 'alignment', 'backstory', 'lifestyle', 'level', 'gold', 'downtime', 'factions', 'player_comment', 'external_link']

class GameSessionForm(forms.ModelForm):
    class Meta:
        model = GameSession
        fields = ['master', 'players', 'date', 'description', 'location', 'tier', 'player_limit', 'game_art']

class PlayerReviewForm(forms.ModelForm):
    class Meta:
        model = PlayerReview
        fields = ['reviewed', 'game_session', 'rating', 'comment']

class GameLogForm(forms.ModelForm):
    class Meta:
        model = GameLog
        fields = ['date_played', 'adventure_code', 'adventure_name', 'downtime_earned', 'gold_earned', 'items_dropped', 'level_gained', 'faction_rank_increase', 'story_awards']

class TradeLogForm(forms.ModelForm):
    class Meta:
        model = TradeLog
        fields = ['traded_with', 'items_received', 'items_given', 'downtime_spent']

    def clean_downtime_spent(self):
        downtime_spent = self.cleaned_data['downtime_spent']
        character = self.instance.character
        # Ensure the character has enough downtime points
        if downtime_spent > character.downtime:
            raise forms.ValidationError("Not enough downtime points")
        return downtime_spent

class DowntimeLogForm(forms.ModelForm):
    class Meta:
        model = DowntimeLog
        fields = ['activity_description', 'downtime_spent']

    def clean_downtime_spent(self):
        downtime_spent = self.cleaned_data['downtime_spent']
        character = self.instance.character
        # Ensure the character has enough downtime points
        if downtime_spent > character.downtime:
            raise forms.ValidationError("Not enough downtime points")
        return downtime_spent
    
class UserProfilePrivacyForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['public_profile', 'show_online_status']

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['against_user', 'against_game_session', 'details']

class GameApplicationForm(forms.ModelForm):
    class Meta:
        model = GameApplication
        fields = ['character']

class GameSessionCompletionForm(forms.ModelForm):
    class Meta:
        model = GameSession
        fields = ['is_finished']
        # Add any other fields relevant to game completion

