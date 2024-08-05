from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import User,Submission,TeacherQuestion
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email', 'password', 'name', 'leetcodeId']

    def validate(self,data):
        if '@' not in data['email']:
            raise serializers.ValidationError('not a valid email id')
        try:
            validate_password(data['password'])
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return data

    def create(self, validated_data):
        user = User(
            email=validated_data['email']
        )
        user.password = validated_data['password']
        user.name=validated_data['name']
        user.leetcodeId=validated_data['leetcodeId']
        user.save()
        return user
    
class SolutionSerializer(serializers.Serializer):
    class Meta:
        model = Submission
        fields = '__all__'

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'

class ProfQuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherQuestion
        fields = '__all__'