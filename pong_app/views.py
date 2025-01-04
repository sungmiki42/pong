from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound
from .models import User, PongGame
from .serializers import UserSerializer, PongGameSerializer
from django.utils import timezone

class LoginAPIView(APIView):
    def post(self, request):
        intra_id = request.data.get('intra_id')
        if not intra_id:
            return Response({"error": "intra_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(intra_id=intra_id)
        if created:
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        else:
            user.last_login = timezone.now()
            user.save()
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

class UserCreateAPIView(APIView):
    permission_classes = [AllowAny]  # 인증 없이 누구나 요청할 수 있도록 설정

    def post(self, request):
        # 요청 데이터로 serializer를 사용하여 유효성 검사
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # 유저 저장
            return Response({
                'id': user.id
            }, status=status.HTTP_201_CREATED)  # 유저가 성공적으로 생성되었을 때 반환
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserAPIView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            return Response(UserSerializer(user).data)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # 요청 사용자 권한 확인
        # if request.user != user:
        #     return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        action = request.data.get('action')  # 'win' 또는 'lose'

        if action not in ['win', 'lose']:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

        if action == 'win':
            user.pong_win += 1
        elif action == 'lose':
            user.pong_lose += 1

        user.save()
        return Response({
            'id': user.id,
            'pong_win': user.pong_win,
            'pong_lose': user.pong_lose
        }, status=status.HTTP_200_OK)

    def delete(self, request, user_id):
        try:
            # 해당 ID에 맞는 유저를 찾기
            user = User.objects.get(id=user_id)
            user.delete()  # 유저 삭제
            return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            raise NotFound(detail="User not found")  # 유저가 존재하지 않으면 404 반환

class PongGameListCreateAPIView(APIView):
    def get(self, request):
        games = PongGame.objects.all()
        return Response(PongGameSerializer(games, many=True).data)

    def post(self, request):
        serializer = PongGameSerializer(data=request.data)
        if serializer.is_valid():
            winner = serializer.validated_data.get('winner_id')
            loser = serializer.validated_data.get('loser_id')
            winner.pong_win += 1
            loser.pong_lose += 1

            serializer.save()
            winner.save()
            loser.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PongGameDetailAPIView(APIView):
    def get(self, request, pong_id):
        try:
            game = PongGame.objects.get(id=pong_id)
            return Response(PongGameSerializer(game).data)
        except PongGame.DoesNotExist:
            return Response({"error": "Game not found"}, status=status.HTTP_404_NOT_FOUND)

