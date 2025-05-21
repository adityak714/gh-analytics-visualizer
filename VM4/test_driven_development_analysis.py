
import os
import requests
from collections import Counter
import json
import re
from datetime import datetime, timedelta, date

# GitHub API token setup
token = os.getenv("GITHUB_TOKEN")
headers = {"Authorization": f"token {token}"}


# Function to check for most popular languages in projects with unit tests
# and for projects who uses continuous integration in the development
def check_test_and_ci_files(repo):
    
    # Extract the owner and repository name from the repo
    owner = repo["owner"]["login"]
    repo_name = repo["name"]

    # Construct the URL to fetch the repository's file tree (main branch)
    contents_url = f"https://api.github.com/repos/{owner}/{repo_name}/git/trees/main?recursive=1"

    response = requests.get(contents_url, headers=headers)

    if response.status_code != 200:

        contents_url = f"https://api.github.com/repos/{owner}/{repo_name}/git/trees/master?recursive=1"
        response = requests.get(contents_url, headers=headers)

    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code} for URL: {contents_url}")
        return False, False  

    data = response.json()

    file_paths = [item['path'] for item in data['tree'] if item['type'] == 'blob']

    # === Test file patterns ===
    test_patterns = [
        r'\/tests?\/|\/specs?\/',
        r'test_.*\.py|.*_test\.py|',
        r'.*test.*\.js|.*spec.*\.js',
        r'.*Test\.java|.*Tests\.java',
        r'.*_test\.go',
        r'.*_test\.rb|test_.*\.rb',
        r'.*Test\.cs',
        r'.*Test\.cpp|.*Test\.cc|.*_test\.cpp',
        r'.*test.*\.php',
        r'.*test.*\.rs'
    ]

    # === CI/CD config patterns ===
    ci_patterns = [
        r'\.github/workflows/.*\.ya?ml',
        r'\.travis\.yml',
        r'circleci/config\.ya?ml',
        r'\.gitlab-ci\.yml',
        r'azure-pipelines\.ya?ml',
        r'jenkinsfile',
        r'\.drone\.ya?ml'
    ]

    has_tests = any(re.search(p, path, re.IGNORECASE) for path in file_paths for p in test_patterns)
    has_ci = any(re.search(p, path, re.IGNORECASE) for path in file_paths for p in ci_patterns)

    return has_tests, has_ci

def analyze_tdd_and_ci_languages(repo_list):

    repositories = repo_list

    print(f"Fetched {len(repositories)} repositories")
    
    tdd_languages = []
    tdd_ci_languages = []

    for repo in repositories:
        language = repo.get("language")
        if (language == None):
            None
        else:
            has_tests, has_ci = check_test_and_ci_files(repo)

            if has_tests:
                tdd_languages.append(language)
            if has_tests and has_ci:
                tdd_ci_languages.append(language)

        

    tdd_languages = Counter(tdd_languages).most_common(10)
    print("TDD",tdd_languages)

    tdd_ci_languages = Counter(tdd_ci_languages).most_common(10)
    print("TDD and CI",tdd_ci_languages)

