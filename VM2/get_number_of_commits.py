from datetime import datetime
import os
import requests
from collections import Counter
import re
import numpy as np
from Github_API_fetch import fetch_repo

# Needs to use personal token to access github API
# Make one with Environment Variables

def commitCount(u, r):
    ## INSPIRATION: https://gist.github.com/codsane/25f0fd100b565b3fce03d4bbd7e7bf33
    url = f"https://api.github.com/repos/{u}/{r}/commits?per_page=1"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch commits for {u}/{r} — Status code: {response.status_code}")
        return None

    # If pagination exists, use 'last' link to get commit count
    if 'last' in response.links:
        last_url = response.links['last']['url']
        return int(re.search(r'\d+$', last_url).group())
    else:
        # Only 0 or 1 commit (not paginated), count manually
        return len(response.json())

token = os.getenv("GITHUB_TOKEN")
headers = {"Authorization": f"token {token}"}

# url for Github API for repositories created after 2025-05-14
# Not archieved and with a maximum of 100 results
# url=f"https://api.github.com/search/repositories?q=created:>2025-05-14+archived:false&per_page=10"

# # Make a Get request to the Github API
# repos = requests.get(url,headers=headers)


def count_commits(repos):
    # Parse the json response from the Github API
    n_commits_list = []
    #IDEA: Extract owner dictionary to get their ID/name, also extract the repo name, then use the function below to calculate the number of commits, and alter it to also return repo name.
    for i in range(len(repos)):
        username = repos[i]["owner"]["login"]
        reponame = repos[i]["name"]
        n_commits = commitCount(username, reponame)
        print(f"Repository: {reponame} -- Username: {username} -- n-commits: {n_commits}")
        n_commits_list.append((reponame, n_commits))

    # Sort by commit count (index 1), descending
    n_commits_list_sorted = sorted(n_commits_list, key=lambda x: x[1], reverse=True)

    # Get top 10
    top_10 = n_commits_list_sorted[:10]

    # Print top 10
    print("\nTop 10 Repositories by Commit Count:")
    for name, count in top_10:
        print(f"{name}: {count} commits")
        