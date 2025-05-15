import os
import requests

# Needs to use personal token to access github API
# Make one with Environment Variables
token = os.getenv("GITHUB_TOKEN")
headers = {"Authorization": f"token {token}"}

# url for Github API for repositories created after 2025-05-14
# Not archieved and with a maximum of 100 results
url=f"https://api.github.com/search/repositories?q=created:>2025-05-14+archived:false&per_page=10"

# Make a Get request to the Github API
repos = requests.get(url,headers=headers)

# Parse the json response from the Github API
data = repos.json()

# Total count of repositories from the repository
item_count = data["total_count"]

# The first repository
items = data["items"][0]

# Print all keys/categories in the first repository
for key in items.keys():
    print(key)

# Print the entire first repository
print(items)

