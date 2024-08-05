import requests
import json
from datetime import datetime, timezone
import time

# Define the URL for the GraphQL endpoint
url = 'https://leetcode.com/graphql'
headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def epoch_to_iso8601(epoch_timestamp, include_microseconds=False):
    dt = datetime.fromtimestamp(epoch_timestamp, tz=timezone.utc)
    if include_microseconds:
        iso8601_string = dt.isoformat(timespec='microseconds')
    else:
        iso8601_string = dt.isoformat()
    return iso8601_string


def get_user_profile(username):
    query = """
    query getUserProfile($username: String!) {
      matchedUser(username: $username) {
        username
        submitStats: submitStatsGlobal {
          acSubmissionNum {
            difficulty
            count
            submissions
          }
        }
      }
    }
    """
    variables = {
        "username": username
    }
    payload = {
        "query": query,
        "variables": variables
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        data = response.json()
        user_data = data['data']['matchedUser']
        username = user_data['username']
        submit_stats = user_data['submitStats']['acSubmissionNum']
        return submit_stats
    else:
        print(f'Failed to retrieve data. Status code: {response.status_code}')
        return response.text

def get_question_of_the_day():
    query = """
    query questionOfToday {
      activeDailyCodingChallengeQuestion {
        question {
          title
          titleSlug
        }
      }
    }
    """
    payload = {
        "query": query,
        "variables": {},
        "operationName": "questionOfToday"
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        question = data['data']['activeDailyCodingChallengeQuestion']['question']
        return question
    else:
        print(f'Failed to retrieve data. Status code: {response.status_code}')
        return response.text

def get_question_details(titleSlug):
    # Define the GraphQL query
    query = """
        query questionTitle($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                questionId
                questionFrontendId
                title
                titleSlug
                isPaidOnly
                difficulty
                likes
                dislikes
                categoryTitle
            }
        }
    """

    # Define the variables
    variables = {
        'titleSlug': titleSlug
    }

    # Define the payload
    payload = {
        'query': query,
        'variables': variables,
        'operationName': 'questionTitle'
    }


    # Send the request to the GraphQL endpoint
    response = requests.post(url, json=payload, headers=headers)

    # Check for request success
    if response.status_code == 200:
        # Extract the data from the response
        data = response.json()
        return data['data']['question']
    else:
        raise Exception(f"Query failed with status code {response.status_code}")
def get_day_questions(username):
    query = """
    query recentAcSubmissions($username: String!) {
      recentAcSubmissionList(username: $username) {
        id
        title
        titleSlug
        timestamp
      }
    }
    """
    variables = {
        "username": username,
    }
    payload = {
    "query": query,
    "variables": variables,
    "operationName": "recentAcSubmissions"
    }


# Send the POST request to the GraphQL endpoint
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    # Print the response
    data  = response.json()['data']['recentAcSubmissionList']
    return data

def get_the_solution(username,potd,teachers_questions,submission):
    solution={}
    solution['leetcodeQuestionId']=get_question_details(submission['titleSlug'])['questionFrontendId']
    solution['submission_id']=submission['id']
    solution['title']=submission['title']
    solution['titleSlug']=submission['titleSlug']
    solution['submission_time']=epoch_to_iso8601(int(submission['timestamp']))
    if submission['titleSlug']==potd['titleSlug']:
      solution['difficulty']=get_question_details(i['titleSlug'])['difficulty']
      solution['points']=4
      solution['category']='POTD'
    elif submission['titleSlug'] in teachers_questions:
      solution['difficulty']=get_question_details(i['titleSlug'])['difficulty']
      solution['points']=5
      solution['category']='PROF'
    else:
      solution['category']='NML'
      if get_question_details(submission['titleSlug'])['difficulty']=='Easy':
        solution['points']=1
        solution['difficulty']='Easy'
      elif get_question_details(submission['titleSlug'])['difficulty']=='Medium':
        solution['points']=2
        solution['difficulty']='Medium'
      elif get_question_details(submission['titleSlug'])['difficulty']=='Hard':
        solution['points']=3
        solution['difficulty']='Hard'
    return solution