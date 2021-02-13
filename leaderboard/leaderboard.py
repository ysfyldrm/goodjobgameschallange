import json
from .models import User
from rest_framework.views import APIView
from rest_framework import status
import redis
from rest_framework.response import Response
from .serializers import UserSerializer

redis_instance = redis.Redis(host='localhost',
                             port='6379',
                             db=0)


def set_rank(user_id, point):
    redis_instance.zadd('leaderboard', {str(user_id): int(point)})
    rank = redis_instance.zrevrank('leaderboard', str(user_id))
    User.objects.filter(user_id=user_id).update(rank=rank+1)


def change_rank(user_id, point):
    redis_instance.zrem('leaderboard', str(user_id))
    redis_instance.zadd('leaderboard', {str(user_id): int(point)})
    rank = redis_instance.zrevrank('leaderboard', str(user_id))
    User.objects.filter(user_id=user_id).update(rank=rank+1)


def check_score(user_id):
    return redis_instance.zscore('leaderboard', str(user_id))


def adjust_ranks():
    point = User.objects.values_list('point', flat=True)
    user_id = User.objects.values_list('user_id', flat=True)
    for user_id, point in zip(user_id, point):
        rank = redis_instance.zrevrank('leaderboard', str(user_id))
        User.objects.filter(user_id=user_id).update(rank=rank+1)


class leaderboard(APIView):
    def get(self, request):
        adjust_ranks()
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class specificLeaderboard(APIView):

    def get_object(self, country):
        try:
            return User.objects.get(country=country)

        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, country):
        adjust_ranks()
        user = User.objects.filter(country=country)
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class userDetailsAPIView(APIView):

    def get_object(self, user_id):
        try:
            return User.objects.get(user_id=user_id)

        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, user_id):
        adjust_ranks()
        user = User.objects.get(user_id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class userCreate(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            display_name = json.loads(json.dumps(serializer.validated_data))['display_name']
            if not User.objects.filter(display_name=display_name).values_list('display_name', flat=True):
                serializer.save()
                user_id = json.loads(json.dumps(serializer.data))['user_id']
                point = json.loads(json.dumps(serializer.data))['point']
                set_rank(user_id, point)
                adjust_ranks()
                return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class submitScore(APIView):

    def get_object(self, user_id):
        try:
            return User.objects.get(user_id=user_id)

        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, user_id):
        point = json.loads(json.dumps(request.data))['point']
        User.objects.filter(user_id=user_id).update(point=point)
        try:
            User.objects.filter(user_id=user_id).get()
            if check_score(user_id) < point:
                adjust_ranks()
                change_rank(user_id, point)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_200_OK)
