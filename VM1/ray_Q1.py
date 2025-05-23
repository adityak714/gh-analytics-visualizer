# Kör Q1 med VM1 som head node. Har satt IPn statiskt

import os
import requests
from datetime import datetime, timedelta
from collections import Counter
import time


import ray
# replace 192.168.2.32 with the value from `hostname -I`
ray.init(address="192.168.2.32:6379", _node_ip_address="192.168.2.32")

# GitHub token from environment variable
token = os.getenv("GITHUB_TOKEN")
if not token:
    raise ValueError("❌ Set your GitHub token in the GITHUB_TOKEN environment variable.")

headers = {"Authorization": f"token {token}"}
base_url = "https://api.github.com/search/repositories"
per_page = 100  # max per page
page = 1        # only 1 page per day

# Date range: past year, every 2nd day
end_date = datetime.utcnow().date()
start_date = end_date - timedelta(days=365)
date_ranges = [start_date + timedelta(days=i) for i in range(0, 365, 1)]  

@ray.remote
def fetch_day(day):
    start_str = day.strftime("%Y-%m-%d")
    end_str = (day + timedelta(days=1)).strftime("%Y-%m-%d")
    created_range = f"{start_str}..{end_str}"

    params = {
        "q": f"created:{created_range} archived:false",
        "per_page": per_page,
        "page": page,
    }

    while True:
        try:
            response = requests.get(base_url, headers=headers, params=params)

            if response.status_code == 403:
                reset_ts = int(response.headers.get("X-RateLimit-Reset", time.time() + 60))
                now_ts = int(time.time())
                sleep_seconds = max(0, reset_ts - now_ts + 5)
                reset_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(reset_ts))
                print(f"⛔ 403 Rate limit hit for {created_range}. Sleeping until {reset_time}...")
                time.sleep(sleep_seconds)
                continue

            if response.status_code != 200:
                print(f"❌ Failed for {created_range}, status {response.status_code}")
                return []

            items = response.json().get("items", [])
            print(f"✅ {created_range}: {len(items)} repos")
            return items

        except Exception as e:
            print(f"❌ Exception during fetch for {created_range}: {e}")
            time.sleep(5)  # back off and retry

# Dispatch tasks to Ray
futures = [fetch_day.remote(day) for day in date_ranges]
results = ray.get(futures)

# Flatten results
all_repos = [repo for day_repos in results for repo in day_repos]
print(f"\n✅ Done. Total repositories fetched: {len(all_repos)}")

# Language analysis
def num_of_languages(items):
    langs = [repo["language"] for repo in items if repo["language"]]
    return Counter(langs)

print("\n📊 Top 10 languages:")
for lang, count in num_of_languages(all_repos).most_common(10):
    print(f"{lang}: {count}")
