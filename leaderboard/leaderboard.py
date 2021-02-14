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
    #add user point value to redis
    redis_instance.zadd('leaderboard', {str(user_id): int(point)})
    #get user rank
    rank = redis_instance.zrevrank('leaderboard', str(user_id))
    #store user rank in database
    User.objects.filter(user_id=user_id).update(rank=float(rank + 1))


def change_rank(user_id, point):
    #remove old point to redis
    redis_instance.zrem('leaderboard', str(user_id))
    #add new point to redis
    redis_instance.zadd('leaderboard', {str(user_id): int(point)})
    #get user new rank
    rank = redis_instance.zrevrank('leaderboard', str(user_id))
    #store user new rank
    User.objects.filter(user_id=user_id).update(rank=float(rank + 1))


def check_score(user_id):
    #check user rank
    return redis_instance.zscore('leaderboard', str(user_id))


def adjust_ranks(old_point, new_point):
    #filter users between changed new users old point value and new point value
    user_id = User.objects.filter(point__lte=new_point, point__gte=old_point).values_list('user_id', flat=True)
    for user_id in user_id:
        #get new users rank
        rank = redis_instance.zrevrank('leaderboard', str(user_id))
        #store them in the database
        User.objects.filter(user_id=user_id).update(rank=float(rank + 1))


class leaderboard(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class specificLeaderboard(APIView):

    def get_object(self, country):
        try:
            return User.objects.get(country__iexact=country)

        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, country):
        user = User.objects.filter(country__iexact=country)
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class userDetailsAPIView(APIView):

    def get_object(self, user_id):
        try:
            return User.objects.get(user_id=user_id)

        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, user_id):
        user = User.objects.get(user_id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class userCreate(APIView):
    def post(self, request):
        # checks the request is multiple
        if isinstance(request.data, list):
            serializer = UserSerializer(data=request.data, many=True)
            if serializer.is_valid():
                #process each request seperately
                for serializer in serializer.validated_data:
                    display_name = serializer['display_name']
                    #checks user display name exist in the database
                    if not User.objects.filter(display_name__iexact=display_name).values_list('display_name', flat=True):
                        new_serializer = UserSerializer(data=serializer)
                        if new_serializer.is_valid():
                            new_serializer.save()
                            user_id = json.loads(json.dumps(new_serializer.data))['user_id']
                            point = float(json.loads(json.dumps(new_serializer.data))['point'])
                            #add user to redis
                            set_rank(user_id, point)
                            #adjust ranks between point values
                            adjust_ranks(0, point)
                return Response(status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #checks the request is single
        elif isinstance(request.data, dict):
            new_serializer = UserSerializer(data=request.data)
            if new_serializer.is_valid():
                #checks user display name exist in the database
                display_name = json.loads(json.dumps(new_serializer.validated_data))['display_name']
                if not User.objects.filter(display_name__iexact=display_name).values_list('display_name', flat=True):
                    new_serializer.save()
                    user_id = json.loads(json.dumps(new_serializer.data))['user_id']
                    point = float(json.loads(json.dumps(new_serializer.data))['point'])
                    #add user to redis
                    set_rank(user_id, point)
                    #adjust ranks between point values
                    adjust_ranks(0, point)
                return Response(status=status.HTTP_201_CREATED)
            return Response(new_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class submitScore(APIView):

    def get_object(self, user_id):
        try:
            return User.objects.get(user_id=user_id)

        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, user_id):
        new_point = json.loads(json.dumps(request.data))['point']
        if User.objects.filter(user_id=user_id).values_list('user_id', flat=True):
            # store user's old point
            old_point = check_score(user_id)
            if old_point < float(new_point):
                User.objects.filter(user_id=user_id).update(point=new_point)
                #change user's
                change_rank(user_id, new_point)
                #adjust ranks between point values
                adjust_ranks(old_point, new_point)
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
