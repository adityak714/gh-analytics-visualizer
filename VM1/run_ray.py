
# Send the list of repositories to pulsar using send_to_pulsar() denna kod ger mig 1000 repo per dag,  medans denna inte gör det: from datetime import datetime, timedelta, date
from datetime import datetime, timedelta, date
import ray
# from Github_API_fetch import fetch_repo
from producer import send_to_pulsar
import os
from count_languages import num_of_languages
import time

# Initialize Ray
ray.init(address="auto", runtime_env={"working_dir": "."})        # address="ray-head:6379")

import requests
import time
import logging
logging.getLogger("ray").setLevel(logging.WARNING)


# Needs to use personal token to access github API
# Make one with Environment Variables

# Fetches and returns a list of repositories 
def fetch_repo(date, token):

    headers = {"Authorization": f"token {token}"}

    # Initialize a list to store repositories
    repos_list = []
    print(date)
    # Maximum of 100 per page can be loaded, so we iterate over 10 pages where each page gives us 100 repositories
    for i in range(1,6):

        # url for Github API for repositories created during specified date
        # Not archieved and with a maximum of 100 results
        url=f"https://api.github.com/search/repositories?q=created:{date}+archived:false&per_page=100&page={i}"

        # Make a Get request to the Github API
        repos = requests.get(url,headers=headers)

        # If maximum request limit has been reached, sleep for 60 seconds
        if repos.status_code == 403:
            print("Sleeping...")
            time.sleep(60)
            continue

        # If not autheried, break loop
        if repos.status_code == 401:
            print("Unautherized")
            break
        
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

# Set date range for fetching repositories
start_date = datetime.strptime("2025-05-19", "%Y-%m-%d")
todays_date = datetime.strptime(date.today().strftime("%Y-%m-%d"), "%Y-%m-%d")

dates = [(start_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((todays_date - start_date).days + 1)]

@ray.remote
def fetch_and_return(date, token):
    try:
        repos = fetch_repo(date, token)
        print(f"Fetched {len(repos)} repos for {date}")
        return repos
    except Exception as e:
        print(f"Error fetching data for {date}: {e}")
        return []

def main():    

    # Start timer to check how long it takes
    t0 = time.time()

    # Retrieve the github token that has been set as a environment variable
    token = os.getenv("GITHUB_TOKEN")
    
    # Launch distributed fetch jobs using Ray
    futures = [fetch_and_return.remote(date_str, token) for date_str in dates]
    results = ray.get(futures)

    # Flatten the list of repositories from all days into one single list 
    list_of_repos = [repo for sublist in results for repo in sublist]
    print(f"\nTotal repositories fetched: {len(list_of_repos)}")

    # Creates a list of lists to prehibit to large messages being sent. 
    # Each chunk is 100 
    chunks = [list_of_repos[i:i + 100] for i in range(0, len(list_of_repos), 100)]

    #Send each chunk in chunks as topics in pulsar
    for i, chunk in enumerate(chunks):
        print(f"Sent {len(chunk)} repos")
        send_to_pulsar(chunk, False)

    # Once all chunks has been looped through, we send a shutdown signal to the consumers
    send_to_pulsar([], True)
    
    # Show total of repos sent
    print(f"Sent a total of {len(list_of_repos)} repos")

    # Print top 10 most occuring in list_of_repo
    print(num_of_languages(list_of_repos).most_common(10))

    # Total time it took to run run.py
    t1 = time.time()
    total = t1-t0
    
    print(f"Total time it took: {total}s")
    
if __name__ == "__main__":
    main() 
