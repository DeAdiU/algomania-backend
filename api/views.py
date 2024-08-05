from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, SubmissionSerializer, ProfQuesSerializer
from .models import User, Submission, TeacherQuestion
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
            if user.password == password:
                token = generate_jwt_token(user)
                return Response({'token': token}, status=status.HTTP_200_OK)
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
def get_submissions(request):
    try:
        user = get_user_from_token(request)
        leetcodeId = user['leetcodeId']
        potd=get_question_of_the_day()
        all_submissions=get_day_questions(leetcodeId)
        
        prof_ques=TeacherQuestion.objects.all()
        serializer = ProfQuesSerializer(prof_ques, many=True)
        for i in all_submissions:
            solution=get_the_solution(leetcodeId,potd,serializer.data,i)
            solution['user']=user['id']
            submission_id = solution['submission_id']
            if Submission.objects.filter(submission_id=submission_id).exists():
                print('no')
                continue
            serializer=SubmissionSerializer(data=solution)
            if serializer.is_valid():
                serializer.save()
                print('yes')
        
        done_submissions=Submission.objects.filter(user=user['id'])
        serializer=SubmissionSerializer(done_submissions, many=True)
        return Response({'message':'inserted everything','data':serializer.data}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_submissions(request):
    try :
        user=get_user_from_token(request)
        done_submissions=Submission.objects.filter(user=user['id'])
        serializer=SubmissionSerializer(done_submissions, many=True)
        return Response({'message':'inserted everything','data':serializer.data}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProfQuesViewSet(viewsets.ModelViewSet):
    queryset = TeacherQuestion.objects.all()
    serializer_class = ProfQuesSerializer