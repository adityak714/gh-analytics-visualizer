from datetime import datetime, timedelta, date
from producent_VM3 import send_to_pulsar
from Github_API_fetch import fetch_repo

# Set dates where we want to fetch repositories
start_date = datetime.strptime("2025-05-10", "%Y-%m-%d")
todays_date = datetime.strptime(date.today().strftime("%Y-%m-%d"), "%Y-%m-%d")

repo_list = []

# Looping through all dates from starting until todays date.
while start_date <= todays_date:
    repo_list.extend(fetch_repo(start_date.strftime("%Y-%m-%d")))
    start_date += timedelta(days=1)

# Send the list of repositories to pulsar using send_to_pulsar()
send_to_pulsar(repo_list)
