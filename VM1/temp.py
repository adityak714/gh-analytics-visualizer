import os
import requests
from datetime import datetime, timedelta, date
import ray
import pulsar
import json

# GitHub token setup
token = os.getenv("GITHUB_TOKEN")
headers = {"Authorization": f"token {token}"}

# Fetches and returns a list of repositories 
def fetch_repo(date):
    print(f"Current date: {date}")
    repos_list = []

    # Fetch up to 1000 repositories (10 pages of 100 each)
    for i in range(1, 11):
        url = f"https://api.github.com/search/repositories?q=created:{date}+archived:false&per_page=100&page={i}"
        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f"Error: Received status code {response.status_code} for URL: {url}")
                break

            repos = response.json().get("items", [])
            if not repos:
                break

            repos_list.extend(repos)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {date}: {e}")
            break

    return repos_list

# Function that sends list of repositories to Pulsar
def send_to_pulsar(repo_list):
    try:
        client = pulsar.Client("pulsar://130.238.28.110:6650")
        producer = client.create_producer("persistent://public/default/repos-raw")

        for repo in repo_list:
            producer.send(json.dumps(repo).encode('utf-8'))

        producer.close()
        client.close()
    except Exception as e:
        print(f"Error sending to Pulsar: {e}")

# Initialize Ray
ray.init(address="auto")

# Set date range for fetching repositories
start_date = datetime.strptime("2025-05-10", "%Y-%m-%d")
todays_date = datetime.strptime(date.today().strftime("%Y-%m-%d"), "%Y-%m-%d")
dates = [(start_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((todays_date - start_date).days + 1)]

@ray.remote
def fetch_and_return(date):
    try:
        repos = fetch_repo(date)
        print(f"Fetched {len(repos)} repos for {date}")
        return repos
    except Exception as e:
        print(f"Error fetching data for {date}: {e}")
        return []

def main():
    # Fetch repository data in parallel
    repo_futures = [fetch_and_return.remote(date) for date in dates]
    repo_list = ray.get(repo_futures)

    # Flatten the list of lists into a single list
    all_repos = [repo for sublist in repo_list for repo in sublist]

    print(f"Total repositories fetched: {len(all_repos)}")
    send_to_pulsar(all_repos)

if __name__ == "__main__":
    main()
