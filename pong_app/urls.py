from django.urls import path
from .views import LoginAPIView, UserAPIView, PongGameListCreateAPIView, PongGameDetailAPIView, UserCreateAPIView

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('users/<int:user_id>/', UserAPIView.as_view(), name='user-detail'),
    path('users/create/', UserCreateAPIView.as_view(), name='user-create'),
	path('games/', PongGameListCreateAPIView.as_view(), name='game-list-create'),
    path('games/<int:pong_id>/', PongGameDetailAPIView.as_view(), name='game-detail'),
]
