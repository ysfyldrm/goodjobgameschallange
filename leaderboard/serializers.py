from rest_framework import serializers
from .models import User


class UserListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        users = [User(**item) for item in validated_data]
        return User.objects.bulk_create(users)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        list_serializer_class = UserListSerializer
        model = User
        fields = '__all__'
