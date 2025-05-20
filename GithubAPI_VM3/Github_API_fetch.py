import os
import requests
from datetime import date
from datetime import datetime, timedelta
from producent_VM3 import send_to_pulsar

# Needs to use personal token to access github API
# Make one with Environment Variables
token = os.getenv("GITHUB_TOKEN")
headers = {"Authorization": f"token {token}"}

# Fetches and returns a list of repositories 
def fetch_repo(date):
    print("Current date: "+date)
    # Initialize a list to store repositories
    repos_list = []

    # Maximum of 100 per page can be loaded, so we iterate over 10 pages where each page gives us 100 repositories
    for i in range(1,2):
        
        # url for Github API for repositories created during specified date
        # Not archieved and with a maximum of 100 results
        url=f"https://api.github.com/search/repositories?q=created:{date}+archived:false&per_page=10&page={i}"

        # Make a Get request to the Github API
        repos = requests.get(url,headers=headers)

        # Check if response is OK
        if repos.status_code != 200:
            print(f"Error: Received status code {repos.status_code} for URL: {url}")
            break

        try:
            repos = repos.json()
        except requests.exceptions.JSONDecodeError:
            print(f"Error: Invalid JSON response for URL: {url}")
            break
        
        # Store all repositories in "items"
        items = repos.get("items",[])

        # If there are no more repositories, we break the loop
        if not items:
            break

        # Add the repositories to the list
        repos_list.extend(items)
    return repos_list




