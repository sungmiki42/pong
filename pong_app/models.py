from django.db import models
from django.utils import timezone

class User(models.Model):
    intra_id = models.CharField(max_length=100, unique=True)  # 외부 API ID
    register_date = models.DateTimeField(default=timezone.now)
    # last_login = models.DateTimeField(auto_now=True)
    pong_win = models.PositiveIntegerField(default=0)
    pong_lose = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.intra_id

class PongGame(models.Model):
    STATUS_CHOICES = [
        ('ONGOING', 'Ongoing'),
        ('FINISHED', 'Finished'),
        ('CANCELED', 'Canceled'),
    ]

    created_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ONGOING')
    winner_id = models.ForeignKey(User, related_name='games_won', on_delete=models.SET_NULL, null=True, blank=True)
    loser_id = models.ForeignKey(User, related_name='games_lost', on_delete=models.SET_NULL, null=True, blank=True)
    winner_score = models.PositiveIntegerField(null=True, blank=True)
    loser_score = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"Game {self.id} ({self.status})"
