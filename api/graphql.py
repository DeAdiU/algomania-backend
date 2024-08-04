import requests
import json
from datetime import datetime
import time

# Define the URL for the GraphQL endpoint
url = 'https://leetcode.com/graphql'
headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


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
        return data
    else:
        raise Exception(f"Query failed with status code {response.status_code}")

def get_day_questions(username,solved_date):
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

    problem=[]

# Send the POST request to the GraphQL endpoint
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(solved_date)
    twenty_four_hr=60*60*24
    current_time=int(time.time())
    print(current_time)
    twenty_four_hr=60*60*24
    human_readable_date = datetime.fromtimestamp(current_time).strftime('%d-%m-%Y')

# Convert the human-readable date back to a datetime object
    date_object = datetime.strptime(human_readable_date, '%d-%m-%Y')
    epoch_time = int(date_object.timestamp())

# Convert the human-readable date back to a datetime object
    date_object = datetime.strptime(solved_date, '%d-%m-%Y')
    start_time = int(date_object.timestamp())
    end_time=start_time+twenty_four_hr
    print(start_time)
    print(end_time)
    # Print the response
    data  = response.json()['data']['recentAcSubmissionList']
    print(data)
    print(len(data))
    for i in data:
        if start_time<= int(i['timestamp'])<epoch_time :
            problem.append(i)
    return problem