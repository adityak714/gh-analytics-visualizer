from datetime import datetime, timedelta, date
import ray
from Github_API_fetch import fetch_repo
from producer import send_to_pulsar

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
    # Parallell hämtning med Ray
    futures = [fetch_and_return.remote(date_str) for date_str in dates]
    results = ray.get(futures)

    # Platta till listan
    list_of_repos = [repo for sublist in results for repo in sublist]
    print(f"\nTotal repositories fetched: {len(list_of_repos)}")

    # Skicka i chunkar om 100
    chunk_size = 100
    chunks = [list_of_repos[i:i + 100] for i in range(0, len(list_of_repos), 100)]

    for i, chunk in enumerate(chunks):
        print(f"Sent{len(chunk)} repos")
        send_to_pulsar(chunk)


    print(f"Sent a total of {len(list_of_repos)} repos")

if __name__ == "__main__":
    main()
