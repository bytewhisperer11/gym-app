from djongo import models
from django.contrib.auth.models import AbstractUser

# Custom user model (if needed, otherwise use Django's default)
class User(AbstractUser):
    email = models.EmailField(unique=True)
    # Add additional fields if needed

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    members = models.ManyToManyField('User', related_name='teams')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('run', 'Running'),
        ('walk', 'Walking'),
        ('strength', 'Strength Training'),
        ('other', 'Other'),
    ]
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    duration_minutes = models.PositiveIntegerField()
    distance_km = models.FloatField(null=True, blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} on {self.date}"

class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    activities = models.ManyToManyField('Activity', related_name='workouts')
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='workouts')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Leaderboard(models.Model):
    team = models.OneToOneField('Team', on_delete=models.CASCADE, related_name='leaderboard')
    total_points = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Leaderboard for {self.team.name}"
