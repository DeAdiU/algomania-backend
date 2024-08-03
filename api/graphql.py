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