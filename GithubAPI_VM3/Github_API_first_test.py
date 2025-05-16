import os
import requests
from collections import Counter

# Needs to use personal token to access github API
# Make one with Environment Variables
token = os.getenv("GITHUB_TOKEN")
headers = {"Authorization": f"token {token}"}

# url for Github API for repositories created after 2025-05-14
# Not archieved and with a maximum of 100 results
url=f"https://api.github.com/search/repositories?q=created:>2025-05-14+archived:false&per_page=100"

# Make a Get request to the Github API
repos = requests.get(url,headers=headers)

print("Statuskod:", repos.status_code)

# Parse the json response from the Github API
data = repos.json()

# Total count of repositories from the repository
item_count = data["total_count"]


def num_of_languages():
    list_of_languages = []
    for i in range(100):
        items = data["items"][i]
        language = items.get("language")

        if (language == None):
            None
        else:
            list_of_languages.append(language)
    
    
    counted_list_of_languages = Counter(list_of_languages)

    return counted_list_of_languages

print(num_of_languages())