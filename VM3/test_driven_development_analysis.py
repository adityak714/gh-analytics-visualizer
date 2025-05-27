import requests
from collections import Counter
import re
import time


# Function to check for most popular languages in projects with unit tests
# and for projects who uses continuous integration in the development
def check_test_and_ci_files(repo, token):
    
    headers = {"Authorization": f"token {token}"}
    # Extract the owner and repository name from the repo
    owner = repo["owner"]["login"]
    repo_name = repo["name"]
    # Construct the URL to fetch the repository's file tree (main branch)
    contents_url = f"https://api.github.com/repos/{owner}/{repo_name}/git/trees/main?recursive=1"

    response = requests.get(contents_url, headers=headers)
    
    # If maximum request limit has been reached, sleep for one hour seconds
    if response.status_code == 403:
        print("Sleeping...")
        print(response.text)  
        time.sleep(3605)
   
    # If not autheried, break loop

    if response.status_code == 401:
        print("Unautherized")
        return False, False  
    
    # Check if response is OK
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code} for URL: {contents_url}")
        return False, False  
    
    # Parse file paths from the response
    data = response.json()
    file_paths = [item['path'] for item in data['tree'] if item['type'] == 'blob']

    # Some typical names for test files
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

    # Some typical names for continious integration files
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

    # Check for matches with test and CI patterns in file paths
    has_tests = any(re.search(p, path, re.IGNORECASE) for path in file_paths for p in test_patterns)
    has_ci = any(re.search(p, path, re.IGNORECASE) for path in file_paths for p in ci_patterns)

    return has_tests, has_ci

def analyze_tdd_and_ci_languages(repositories, token):

    # Print total amount of repositories that has been fetched
    print(f"\n\nFetched {len(repositories)} repositories")
   
    # Lists to hold languages for repos with tests and those with both tests and CI    
    tdd_languages = []
    tdd_ci_languages = []

    i = 0
    
    total_repos = len(repositories)

    # Loop through each repository
    for repo in repositories:
        
        #Print repositories left to analyze
        repo_left = total_repos - i 
        i = i + 1
        print(f"Have a total of {repo_left} repositories left.")

        # Skip repositories with no language detected
        language = repo.get("language")
        if (language == None):
            None
        else:
            # Check for test and CI files in the repository
            has_tests, has_ci = check_test_and_ci_files(repo, token)

            # if repos with tests, append the language to tdd_languages
            if has_tests:
                tdd_languages.append(language)

            # if has both tests and ci/cd files, append to tdd_ci_languages
            if has_tests and has_ci:
                tdd_ci_languages.append(language)

    # display the 10 most occuring in tdd_languages
    tdd_languages = Counter(tdd_languages).most_common(10)
    print("TDD",tdd_languages)
    
    # display the 10 most occuring in tdd_ci_languages
    tdd_ci_languages = Counter(tdd_ci_languages).most_common(10)
    print("TDD and CI",tdd_ci_languages)

