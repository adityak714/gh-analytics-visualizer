import json, requests, os
from urllib.parse import urlparse, parse_qs

"""
This Pulsar function is for finding the top 10 most frequently updated GitHub projects (i.e., most commits in a project).
It comes as a middleman, filtering out just the metadata it is made for (Programming Language used).

This subscribes to "repos-raw" (where GitHub API responses are fetched), and emits at a * new * topic "top-10-programming-languages", 
that the end consumer will subscribe to.
"""

"""
A consumer currently is subscribing to:
    'persistent://public/default/repos-raw',
    to which the producer sends the whole project info as JSON.

    "... for repos in repo: ..." (probably one by one?) 
"""

token = os.getenv("GITHUB_TOKEN")
headers = {"Authorization": f"token {token}"}

def process(input): 
    # the input is in the form of JSON, of metadata of one or multiple projects
    most_committed_projects = []

    for i in range(100):
        items = input["items"][i]
        repo_address = items.get("full_name")
        repo_default_branch = items.get("default_branch")

        ###############################        
        # 1: Get the SHA of the default branch at the repo
        ###############################

        url = f"https://api.github.com/repos/{repo_address}/git/refs/heads/{repo_default_branch}"
        sha = requests.get(url,headers=headers)["object"]["sha"]

        # Example: 
        # https://api.github.com/repos/pytorch/pytorch/git/refs/heads/main 
        # or 
        # https://api.github.com/repos/xai-org/grok-prompts/git/refs/heads/master (can vary from repo to repo)
        # Get the SHA from here ^

        ###############################
        # 2: Substitute it in the second_url to get the commit count
        ###############################

        second_url = f"https://api.github.com/repos/pytorch/pytorch/commits?sha={sha}&per_page=1&page=1" # to get all commits
        req = requests.get(second_url,headers=headers)

        # Access the response headers to get the last page (i.e. the commit count)
        response_h = req.headers["Link"].split(",")

        # [::-1] is for reversing, to have key as the link attributes, and values being the page locations
        headers_link = dict(element.split(";")[::-1] for element in response_h)
        last_page = urlparse(headers_link.get(' rel="last"').replace(">", "").replace("<", ""))

        # using url parsing library to quickly get the last page (each commit was put in one page)
        commit_count = int(parse_qs(last_page.query)["page"][0])
        print(commit_count)

        most_committed_projects.append({
            "project": repo_address,
            "commit_count": commit_count
        })

    return most_committed_projects