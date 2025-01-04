from rest_framework import serializers
from .models import User, PongGame

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'intra_id', 'register_date', 'pong_win', 'pong_lose']

class PongGameSerializer(serializers.ModelSerializer):
    # winner_id = serializers.StringRelatedField()
    # loser_id = serializers.StringRelatedField()
    # winner_id = serializers.IntegerField()
    # loser_id = serializers.IntegerField()
    # winner_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    # loser_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = PongGame
        fields = ['id', 'created_date', 'status', 'winner_id', 'loser_id', 'winner_score', 'loser_score']
