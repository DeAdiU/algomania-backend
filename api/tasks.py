# myapp/tasks.py

from celery import shared_task
import requests
from api.graphql import get_the_solution, get_day_questions, get_question_of_the_day, get_question_details
from api.serializers import SolutionSerializer, SubmissionSerializer,UserSerializer,ProfQuesSerializer
from api.models import Submission,User,TeacherQuestion

@shared_task
def call_drf_endpoint():
    # Handle the response as needed
    
    try:
        serializer = UserSerializer(User.objects.all(), many=True)
        for user in serializer.data:
            print(user)
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
        
        return {'message': 'Submissions processed and score updated'}

    except User.DoesNotExist:
        return {'error': 'User not found'}
    
