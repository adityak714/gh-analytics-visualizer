import requests
import re
import time

# Needs to use personal token to access github API
# Make one with Environment Variables

def commitCount(u, r, token):
    
    headers = {"Authorization": f"token {token}"}
    ## INSPIRATION: https://gist.github.com/codsane/25f0fd100b565b3fce03d4bbd7e7bf33
    url = f"https://api.github.com/repos/{u}/{r}/commits?per_page=1"
    response = requests.get(url, headers=headers)
    if response.status_code == 403:
            print("Sleeping...")
            print(response.text)  # eller response.json()
            time.sleep(3605)
        
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


# url for Github API for repositories created after 2025-05-14
# Not archieved and with a maximum of 100 results
# url=f"https://api.github.com/search/repositories?q=created:>2025-05-14+archived:false&per_page=10"

# # Make a Get request to the Github API
# repos = requests.get(url,headers=headers)


def count_commits(repos, token):
    
    # Parse the json response from the Github API
    n_commits_list = []
    n_repos = len(repos)

    #IDEA: Extract owner dictionary to get their ID/name, also extract the repo name, then use the function below to calculate the number of commits, and alter it to also return repo name.
    for i in range(n_repos):
        
        print("Number of repos left: ", n_repos - i)

        username = repos[i]["owner"]["login"]
        reponame = repos[i]["name"]
        n_commits = commitCount(username, reponame, token)
        

    
        if n_commits is not None:
            print(f"Repository: {reponame} -- Username: {username} -- n-commits: {n_commits}")
            n_commits_list.append((reponame, n_commits))
        else:
            print(f"⚠️ Skipping {reponame} due to missing commit count")

    # Sort by commit count (index 1), descending
    n_commits_list_sorted = sorted(n_commits_list, key=lambda x: x[1], reverse=True)

    # Get top 10
    top_10 = n_commits_list_sorted[:10]

    # Print top 10
    print("\nTop 10 Repositories by Commit Count:")
    for name, count in top_10:
        print(f"{name}: {count} commits")
        