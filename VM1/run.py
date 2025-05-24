from datetime import datetime, timedelta, date
from producer import send_to_pulsar
from Github_API_fetch import fetch_repo
import os
import time
from Q1 import num_of_languages
t0 = time.time()

token = os.getenv("GITHUB_TOKEN")

# Set dates where we want to fetch repositories
start_date = datetime.strptime("2025-05-20", "%Y-%m-%d")
todays_date = datetime.strptime(date.today().strftime("%Y-%m-%d"), "%Y-%m-%d")


list_of_repos = []
# Looping through all dates from starting until todays date.
while start_date <= todays_date:
    list_of_repos.extend(fetch_repo(start_date.strftime("%Y-%m-%d"), token))
    start_date += timedelta(days=1)

chunks = [list_of_repos[i:i + 100] for i in range(0, len(list_of_repos), 100)]


for repos in chunks:
    print(f"Sent {len(repos)} repos")
    send_to_pulsar(repos, False)


print(f"Sent a total of {len(list_of_repos)} repos")

t1 = time.time()


print(num_of_languages(list_of_repos).most_common(10))

print(f"Total of {t1-t0}s")

# Send the list of repositories to pulsar using send_to_pulsar()
