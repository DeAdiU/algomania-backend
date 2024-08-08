from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import User,Submission,TeacherQuestion,Team
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'name', 'leetcodeId', 'score', 'team']

    def validate(self, data):
        if '@' not in data['email']:
            raise serializers.ValidationError('Not a valid email id')
        try:
            validate_password(data['password'])
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return data

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            name=validated_data['name'],
            leetcodeId=validated_data['leetcodeId'],
            password=validated_data['password'],
            team_id=validated_data.get('team_id', None),
            score=validated_data.get('score', 0)
              # Default score to 0 if not provided
        )
        
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        instance.leetcodeId = validated_data.get('leetcodeId', instance.leetcodeId)
        instance.team_id = validated_data.get('team_id', instance.team_id)
        instance.score = validated_data.get('score', instance.score)  # Update score if provided
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance
    
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


class TeamUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['score','name','leetcodeId','email']
class TeamSerializer(serializers.ModelSerializer):
    members = TeamUserSerializer(many=True,read_only=True)
    class Meta:
        model= Team
        fields = ['team_name','members']
    
class UserSubmissionSerializer(serializers.ModelSerializer):
    submissions = SubmissionSerializer(many=True,read_only=True)
    class Meta:
        model = User
        fields = ['score','name','leetcodeId','email','submissions']

