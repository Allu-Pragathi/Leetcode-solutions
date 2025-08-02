import os
import json
import requests
from graphqlclient import GraphQLClient

# Config
GITHUB_REPO_PATH = os.getcwd()
LEETCODE_USERNAME = "Allu_Pragathi"

def get_leetcode_solved_problems():
    query = """
    query userProblemsSolved($username: String!) {
      allQuestionsCount {
        difficulty
        count
      }
      matchedUser(username: $username) {
        submitStats {
          acSubmissionNum {
            difficulty
            count
            submissions
          }
        }
      }
    }
    """
    variables = {"username": LEETCODE_USERNAME}
    client = GraphQLClient('https://leetcode.com/graphql')
    response = client.execute(query, variables)
    data = json.loads(response)
    return data

def get_accepted_submissions():
    url = "https://leetcode.com/api/submissions/?offset=0&limit=1000"
    
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://leetcode.com",
        "x-csrftoken": "PUT_YOUR_CSRF_TOKEN_HERE",
        "cookie": "LEETCODE_SESSION=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiMTIzNzQyNzEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjM4ODcxYzMwODc3Njc3YmUwYjRjNTJkYmE4YjEwN2VkZjhhNmVmNTY4OTA5NTBmMDlkMGRlOGM1NWQ2Zjg2ZTMiLCJzZXNzaW9uX3V1aWQiOiJiMjViYTUwMyIsImlkIjoxMjM3NDI3MSwiZW1haWwiOiJhbGx1cHJhZ2F0aGlAZ21haWwuY29tIiwidXNlcm5hbWUiOiJBbGx1X3ByYWdhdGhpIiwidXNlcl9zbHVnIjoiQWxsdV9wcmFnYXRoaSIsImF2YXRhciI6Imh0dHBzOi8vYXNzZXRzLmxlZXRjb2RlLmNvbS91c2Vycy9BbGx1X3ByYWdhdGhpL2F2YXRhcl8xNzQ4MjU4NjMwLnBuZyIsInJlZnJlc2hlZF9hdCI6MTc1NDA3NDI2NSwiaXAiOiIxMjguMTg1LjE2OC4xOTUiLCJpZGVudGl0eSI6ImQyYWQ2Nzg1ZDI1Njg1MWRkMzY2NzAzYmRjNjFhYTYxIiwiZGV2aWNlX3dpdGhfaXAiOlsiZDBlOTY2OWI5OGIyMWFiZDM4NTRmNmFhYTg5MmMyZjYiLCIxMjguMTg1LjE2OC4xOTUiXSwiX3Nlc3Npb25fZXhwaXJ5IjoxMjA5NjAwfQ.uz09gp_5Fjr6Jk-dUzvJTg3Pq4kP56dTuv0tmZOToEk; csrftoken=CpSXIAyPE3BXBj3MhGbWWlqAMFceb5TPHUhIh4WP7ebEanRaMucAa0dv9vgApK9T"
    }
    
    response = requests.get(url, headers=headers)
    data = response.json()

    accepted = []
    for sub in data.get("submissions_dump", []):
        if sub["status_display"] == "Accepted":
            accepted.append(sub)
    return accepted


def save_to_files(submissions):
    for sub in submissions:
        title_slug = sub["title_slug"]
        lang = sub["lang"]
        code = sub["code"]
        ext = {
            "python3": "py",
            "cpp": "cpp",
            "java": "java",
            "c": "c",
            "csharp": "cs",
            "javascript": "js"
        }.get(lang.lower(), "txt")

        filename = f"{title_slug}.{ext}"
        filepath = os.path.join(GITHUB_REPO_PATH, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code)
        print(f"✅ Synced: {filename}")

def git_push():
    os.system("git add .")
    os.system("git commit -m 'LeetCode Sync Update'")
    os.system("git push origin main")

if __name__ == "__main__":
    print("🔁 Fetching LeetCode accepted submissions...")
    submissions = get_accepted_submissions()
    save_to_files(submissions)
    git_push()
