from datetime import datetime, timedelta, date
from producer import send_to_pulsar
from Github_API_fetch import fetch_repo
import os
import time
from count_languages import num_of_languages

#Start timer to se how long everything takes
t0 = time.time()

# Retrieve the github token that has been set as a environment variable
token = os.getenv("GITHUB_TOKEN")

# Set dates where we want to fetch repositories
start_date = datetime.strptime("2025-05-20", "%Y-%m-%d")
todays_date = datetime.strptime(date.today().strftime("%Y-%m-%d"), "%Y-%m-%d")

# Create a empty list for repos
list_of_repos = []

# Looping through all dates from starting until todays date.
while start_date <= todays_date:
    # Fetch repositories for start_date
    list_of_repos.extend(fetch_repo(start_date.strftime("%Y-%m-%d"), token))
    
    #Add a day to start_date
    start_date += timedelta(days=1)

# Creates a list of lists to prehibit to large messages being sent. 
# Each chunk is 100 
chunks = [list_of_repos[i:i + 100] for i in range(0, len(list_of_repos), 100)]

#Send each chunk in chunks as topics in pulsar
for repos in chunks:
    print(f"Sent {len(repos)} repos")
    send_to_pulsar(repos, False)

# Print number of tota, repos we sent through pulsar
print(f"Sent a total of {len(list_of_repos)} repos")

# Print top 10 most occuring in list_of_repo
print(num_of_languages(list_of_repos).most_common(10))

# Total time it took to run run.py
t1 = time.time()
print(f"Total of {t1-t0}s")

