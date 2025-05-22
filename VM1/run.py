from datetime import datetime, timedelta, date
from producer import send_to_pulsar
from Github_API_fetch import fetch_repo

# Set dates where we want to fetch repositories
start_date = datetime.strptime("2025-05-16", "%Y-%m-%d")
todays_date = datetime.strptime(date.today().strftime("%Y-%m-%d"), "%Y-%m-%d")


list_of_repos = []

# Looping through all dates from starting until todays date.
while start_date <= todays_date:
        
    list_of_repos.extend(fetch_repo(start_date.strftime("%Y-%m-%d")))
    start_date += timedelta(days=1)

chunks = [list_of_repos[i:i + 100] for i in range(0, len(list_of_repos), 100)]


for repos in chunks:
    print(f"Sent{len(repos)} repos")
    send_to_pulsar(repos)


print(f"Sent a total of {len(list_of_repos)} repos")
# Send the list of repositories to pulsar using send_to_pulsar()
