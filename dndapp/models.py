from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Additional field to notify user on new games
    notify_on_new_games = models.BooleanField(default=True)
    # New field for tracking online status
    last_online = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    rating = models.FloatField(default=0.0)  # Player rating
    reviews = models.TextField(blank=True)  # Reviews from other users
    played_games = models.IntegerField(default=0)  # Total number of played games
    # New fields for privacy settings
    public_profile = models.BooleanField(default=True)
    show_online_status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
class Character(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    race = models.CharField(max_length=50)
    classes = models.CharField(max_length=200)  # To accommodate multiclassing
    alignment = models.CharField(max_length=50)
    backstory = models.TextField()
    lifestyle = models.CharField(max_length=100)
    level = models.IntegerField()
    gold = models.DecimalField(max_digits=10, decimal_places=2)
    downtime = models.IntegerField()
    factions = models.CharField(max_length=200)
    player_comment = models.TextField(blank=True)
    external_link = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name
    
class GameSession(models.Model):
    master = models.ForeignKey(CustomUser, related_name='mastered_sessions', on_delete=models.CASCADE)
    players = models.ManyToManyField(CustomUser, related_name='participated_sessions')
    date = models.DateTimeField()
    description = models.TextField()
    location = models.CharField(max_length=200)
    tier = models.IntegerField()
    player_limit = models.IntegerField(default=6)
    is_finished = models.BooleanField(default=False)
    # Placeholder for game art; actual implementation will depend on how you handle media files
    game_art = models.ImageField(upload_to='game_art/', blank=True, null=True)

    def __str__(self):
        return f"Session on {self.date.strftime('%Y-%m-%d')} at {self.location}"
    
class PlayerReview(models.Model):
    reviewer = models.ForeignKey(CustomUser, related_name='given_reviews', on_delete=models.CASCADE)
    reviewed = models.ForeignKey(CustomUser, related_name='received_reviews', on_delete=models.CASCADE)
    game_session = models.ForeignKey(GameSession, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.reviewed.username}"
    
class Notification(models.Model):
    recipient = models.ForeignKey(CustomUser, related_name='notifications', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.recipient.username}"
    
class GameLog(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    date_played = models.DateTimeField()
    adventure_code = models.CharField(max_length=100)
    adventure_name = models.CharField(max_length=200)
    downtime_earned = models.IntegerField()
    gold_earned = models.DecimalField(max_digits=10, decimal_places=2)
    items_dropped = models.TextField()
    level_gained = models.BooleanField(default=False)
    faction_rank_increase = models.BooleanField(default=False)
    story_awards = models.TextField()
    # Add any other relevant fields

    def __str__(self):
        return f"{self.adventure_name} - {self.date_played.strftime('%Y-%m-%d')}"

class TradeLog(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    traded_with = models.CharField(max_length=100)  # Name or identifier of the other party
    items_received = models.TextField()
    items_given = models.TextField()
    downtime_spent = models.IntegerField()
    trade_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Trade for {self.character.name} on {self.trade_date.strftime('%Y-%m-%d')}"

class DowntimeLog(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    activity_description = models.TextField()
    downtime_spent = models.IntegerField()
    log_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Downtime for {self.character.name} on {self.log_date.strftime('%Y-%m-%d')}"
    
class UserStatistics(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='statistics')
    total_games_played = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0.0)
    # Add other relevant statistical fields

    def __str__(self):
        return f"Statistics for {self.user.username}"

class GameStatistics(models.Model):
    game_session = models.OneToOneField(GameSession, on_delete=models.CASCADE, related_name='statistics')
    total_players = models.IntegerField(default=0)
    average_player_rating = models.FloatField(default=0.0)
    # Additional fields as required

    def __str__(self):
        return f"Statistics for Game Session on {self.game_session.date}"
    
class Complaint(models.Model):
    submitted_by = models.ForeignKey(CustomUser, related_name='submitted_complaints', on_delete=models.CASCADE)
    against_user = models.ForeignKey(CustomUser, related_name='received_complaints', on_delete=models.CASCADE, null=True, blank=True)
    against_game_session = models.ForeignKey(GameSession, on_delete=models.CASCADE, null=True, blank=True)
    details = models.TextField()
    submitted_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, default='Submitted')

    def __str__(self):
        return f"Complaint by {self.submitted_by.username}"
    
class GameApplication(models.Model):
    game_session = models.ForeignKey(GameSession, related_name='applications', on_delete=models.CASCADE)
    player = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, default='Pending')  # e.g., Pending, Approved, Rejected

    def __str__(self):
        return f"{self.player.username}'s application for {self.game_session}"