from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'name', 'leetcodeId']

    def create(self, validated_data):
        user = User(
            email=validated_data['email']
        )
        user.password = validated_data['password']
        user.name=validated_data['name']
        user.leetcodeId=validated_data['leetcodeId']
        user.save()
        return user
    