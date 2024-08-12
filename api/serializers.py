from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import User,Submission,TeacherQuestion,Team,Difficulty,Category
from django.contrib.auth.password_validation import validate_password
from django.db.models import Sum,Count

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'name', 'leetcodeId', 'score', 'team', 'user_type']

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
        fields = ['score','name','leetcodeId','email','team']
class TeamSerializer(serializers.ModelSerializer):
    team_score = serializers.SerializerMethodField()
    members = TeamUserSerializer(many=True,read_only=True)
    
    class Meta:
        model= Team
        fields = ['team_id','team_name','members','team_score']
    
    def get_team_score(self, obj):
        # Sum all members' scores
        total_score = obj.members.aggregate(total_score=Sum('score'))['total_score']
        return total_score if total_score is not None else 0
    
class UserSubmissionSerializer(serializers.ModelSerializer):
    submissions = SubmissionSerializer(many=True,read_only=True)
    class Meta:
        model = User
        fields = ['score','name','leetcodeId','email','submissions']

class UserQuesWiseSerializer(serializers.ModelSerializer):
    difficulty_wise = serializers.SerializerMethodField()
    category_wise = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'score', 'difficulty_wise', 'category_wise']

    def get_difficulty_wise(self, obj):
        # Aggregate submissions by difficulty
        submissions = Submission.objects.filter(user=obj['id'])
        
        difficulty_counts = submissions.values('difficulty').annotate(count=Count('user_id')).order_by('difficulty')
        
        result = {difficulty: 0 for difficulty in Difficulty._member_names_}
        for item in difficulty_counts:
            result[item['difficulty']] = item['count']
        
        return result
        
    
    def get_category_wise(self, obj):
        # Aggregate submissions by category
        submissions = Submission.objects.filter(user=obj['id'])
        category_counts = submissions.values('category').annotate(count=Count('user_id')).order_by('category')
        
        # Convert the aggregated data into a dictionary
        result = {category: 0 for category in Category.values}
        for item in category_counts:
            result[item['category']] = item['count']
        
        return result

class TeamQuesWiseSerializer(serializers.ModelSerializer):
    difficulty_wise = serializers.SerializerMethodField()
    category_wise = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'score', 'difficulty_wise', 'category_wise']

    def get_difficulty_wise(self, obj):
        # Aggregate submissions by difficulty
        submissions = Submission.objects.filter(user=obj)
        
        difficulty_counts = submissions.values('difficulty').annotate(count=Count('user_id')).order_by('difficulty')
        
        result = {difficulty: 0 for difficulty in Difficulty._member_names_}
        for item in difficulty_counts:
            result[item['difficulty']] = item['count']
        
        if 'Hard' not in result:
            result['Hard']=0
        return result
        
    
    def get_category_wise(self, obj):
        # Aggregate submissions by category
        submissions = Submission.objects.filter(user=obj)
        category_counts = submissions.values('category').annotate(count=Count('user_id')).order_by('category')
        
        # Convert the aggregated data into a dictionary
        result = {category: 0 for category in Category.values}
        for item in category_counts:
            result[item['category']] = item['count']
        
        return result


class TeamQuesSerializer(serializers.ModelSerializer):
    team_score = serializers.SerializerMethodField()
    members = TeamQuesWiseSerializer(many=True,read_only=True)
    
    class Meta:
        model= Team
        fields = ['team_id','team_name','members','team_score']
    
    def get_team_score(self, obj):
        # Sum all members' scores
        total_score = obj.members.aggregate(total_score=Sum('score'))['total_score']
        return total_score if total_score is not None else 0
    