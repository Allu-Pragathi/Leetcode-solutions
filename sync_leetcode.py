import os
import json
import requests
from graphqlclient import GraphQLClient

GITHUB_REPO_PATH = os.getcwd()
LEETCODE_USERNAME = os.getenv("LEETCODE_USERNAME")
LEETCODE_COOKIE = os.getenv("LEETCODE_COOKIE")

def get_accepted_submissions():
    url = "https://leetcode.com/api/submissions/?offset=0&limit=1000"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://leetcode.com",
        "cookie": LEETCODE_COOKIE
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    return [sub for sub in data.get("submissions_dump", []) if sub["status_display"] == "Accepted"]

def save_to_files(submissions):
    for sub in submissions:
        title_slug = sub["title_slug"]
        lang = sub["lang"]
        code = sub["code"]
        ext = {
            "python3": "py", "cpp": "cpp", "java": "java",
            "c": "c", "csharp": "cs", "javascript": "js"
        }.get(lang.lower(), "txt")
        filename = f"{title_slug}.{ext}"
        filepath = os.path.join(GITHUB_REPO_PATH, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code)
        print(f"✅ Synced: {filename}")

if __name__ == "__main__":
    print("🔁 Fetching LeetCode accepted submissions...")
    submissions = get_accepted_submissions()
    save_to_files(submissions)
