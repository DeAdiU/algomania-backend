from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,generics
from .serializers import UserSerializer, SubmissionSerializer, ProfQuesSerializer, TeamSerializer, TeamUserSerializer,UserQuesWiseSerializer,TeamQuesSerializer
from .models import User, Submission, TeacherQuestion,Team
from .graphql import get_user_profile, get_the_solution, get_day_questions, get_question_of_the_day, get_question_details
import datetime
import jwt  
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework import viewsets


class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = generate_jwt_token(user)
            return Response({'token': token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email)
            user_type = user.user_type
            serializer = TeamUserSerializer(user)
            if user.password == password:
                token = generate_jwt_token(user)
                return Response({'token': token, 'user_type': user_type, 'user':serializer.data}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_user_from_token(request):
    token = request.META.get('HTTP_AUTHORIZATION', '').replace('Bearer ', '')
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user = User.objects.get(id=payload['user_id'])
        serializer = UserSerializer(user)
        return serializer.data
    except jwt.ExpiredSignatureError:
        return Response({'error': 'Signature expired'}, status=status.HTTP_401_UNAUTHORIZED)
    except jwt.DecodeError:
        return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_profile(request):
    user = get_user_from_token(request)

    if isinstance(user, Response):
        return user  # Error response from get_user_from_token

    # Assuming get_user_profile is a function that takes a username and returns profile data
    profile_data = get_user_profile(user['leetcodeId'])

    if profile_data is None:
        return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

    return Response({"user": user, "profile": profile_data}, status=status.HTTP_200_OK)


def generate_jwt_token(user):
    payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token


class UserViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer


@api_view(['POST'])
def push_submissions(request):
    try:
        user = get_user_from_token(request)
        leetcodeId = user['leetcodeId']
        potd = get_question_of_the_day()
        all_submissions = get_day_questions(leetcodeId)
        prof_ques = TeacherQuestion.objects.all()
        serializer = ProfQuesSerializer(prof_ques, many=True)
        
        user_instance = User.objects.get(id=user['id'])
        
        for i in all_submissions:
            solution = get_the_solution(leetcodeId, potd, serializer.data, i)
            solution['user'] = user['id']
            submission_id = solution['submission_id']
            if Submission.objects.filter(submission_id=submission_id).exists():
                print('no')
                break
            else:
                submission_serializer = SubmissionSerializer(data=solution)
                if submission_serializer.is_valid():
                    submission_serializer.save()
                    print('yes')
                    user_instance.score += solution['points']
        
        user_instance.save()
        
        return Response({'message': 'Submissions processed and score updated'}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def get_recent_submissions(request):
    try :
        user=get_user_from_token(request)
        done_submissions=Submission.objects.filter(user=user['id'])
        serializer=SubmissionSerializer(done_submissions, many=True)
        data=serializer.data
        data.sort(key=lambda x: datetime.datetime.strptime(x['submission_time'], "%Y-%m-%dT%H:%M:%SZ").timestamp(),reverse=True)
        return Response({'message':'inserted everything','data':data[:10]}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProfQuesViewSet(viewsets.ModelViewSet):
    queryset = TeacherQuestion.objects.all()
    serializer_class = ProfQuesSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamQuesSerializer

@api_view(['PATCH'])
def update_team_id(request):
    try:
        user = get_user_from_token(request)
        team_id = request.data.get('team_id')

        if not team_id:
            return Response({'error': 'team_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the Team instance using the correct field name
        try:
            team_instance = Team.objects.get(team_id=team_id)
        except Team.DoesNotExist:
            return Response({'error': 'Team not found'}, status=status.HTTP_404_NOT_FOUND)
        
        user_instance = User.objects.get(id=user['id'])  # Ensure 'id' is the correct field for the User model
        user_instance.team = team_instance  # Assign the Team instance
        user_instance.save()
        
        return Response({'message': 'Team ID updated successfully'}, status=status.HTTP_200_OK)
    
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

      

@api_view(['GET'])
def get_teams(request):
    try:
        user = get_user_from_token(request)
        team_id = user['team']
        if not team_id:
            return Response({'error': 'Team not found'}, status=status.HTTP_404_NOT_FOUND)
        team_f = Team.objects.get(team_id=team_id)
    except Team.DoesNotExist:
        return Response({'error': 'Team not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = TeamSerializer(team_f)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_top(request):
    try:
        user=get_user_from_token(request)
        user_top=User.objects.all().order_by('-score')[:1]
        serializer = UserSerializer(user_top, many=True)
        user_data = serializer.data
        print(user_data)
        teams_data = TeamSerializer(Team.objects.all(), many=True).data
        teams_data.sort(key=lambda x: x['team_score'], reverse=True)
        print(teams_data)
        team_id = user['team']
        team_f = Team.objects.get(team_id=team_id)
        serializer = TeamSerializer(team_f)
        return Response({"team": teams_data, "user": user_data, "user_team": serializer.data}, status=status.HTTP_200_OK)
        
    except Team.DoesNotExist:
        return Response({'error': 'Team not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def user_detail(request):
    user = get_user_from_token(request)
    
    if user is None:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserQuesWiseSerializer(user)
    data=serializer.data
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def all_teams_summary(request):
    teams = Team.objects.all()
    serializer = TeamQuesSerializer(teams, many=True)
    data=serializer.data
    teamsData=[]
    for i in data:
        ok_temp={}
        ok_temp['teamName']=i['team_name']
        ok_temp['members']=[]
        for j in i['members']:
            temp={}
            temp['name']=j['name']
            temp['points']=j['score']
            temp['easy']=j['difficulty_wise']['Easy']
            temp['medium']=j['difficulty_wise']['Medium']
            temp['hard']=j['difficulty_wise']['Hard']
            temp['potd']=j['category_wise']['POTD']
            temp['staff']=j['category_wise']['PROF']
            ok_temp['members'].append(temp)
        teamsData.append(ok_temp)
    print(teamsData)
    return Response(teamsData, status=status.HTTP_200_OK)
