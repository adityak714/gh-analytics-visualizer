import os
import requests
from datetime import datetime, timedelta
from collections import Counter
import time

# Start timer
start_time = time.time()

# GitHub token from environment variable
token = os.getenv("GITHUB_TOKEN")
if not token:
    raise ValueError("Set your GitHub token in the GITHUB_TOKEN environment variable.")

headers = {"Authorization": f"token {token}"}
base_url = "https://api.github.com/search/repositories"
per_page = 100  # max per page
page = 1        # just 1 page per interval

# Date range: past year, stepping every 2nd day
end_date = datetime.utcnow().date()
start_date = end_date - timedelta(days=365)
date_ranges = [start_date + timedelta(days=i) for i in range(0, 365, 2)]

all_repos = []
total_fetched = 0

# Fetch 100 repos every other day
for day in date_ranges:
    start_str = day.strftime("%Y-%m-%d")
    end_str = (day + timedelta(days=1)).strftime("%Y-%m-%d")
    created_range = f"{start_str}..{end_str}"

    params = {
        "q": f"created:{created_range} archived:false",
        "per_page": per_page,
        "page": page,
    }

    response = requests.get(base_url, headers=headers, params=params)

    # Rate‐limit handling
    if response.status_code == 403:
        reset_ts = int(response.headers.get("X-RateLimit-Reset", time.time() + 60))
        sleep_seconds = max(0, reset_ts - time.time() + 5)
        reset_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(reset_ts))
        print(f"⛔ 403 Rate limit hit. Sleeping until {reset_time} ({int(sleep_seconds)}s)...")
        time.sleep(sleep_seconds)
        response = requests.get(base_url, headers=headers, params=params)  # retry once

    if response.status_code != 200:
        print(f"❌ Failed for {created_range}, status {response.status_code}")
        continue

    items = response.json().get("items", [])
    all_repos.extend(items)
    total_fetched += len(items)

    print(f"✅ {created_range}: {len(items)} repos (total so far: {total_fetched})")

# End timer
elapsed = time.time() - start_time
print(f"\n⏱️  Total execution time: {elapsed:.2f} seconds")

# Language stats
def num_of_languages(items):
    langs = [repo["language"] for repo in items if repo["language"]]
    return Counter(langs)

print("\n📊 Top 10 languages:")
for lang, count in num_of_languages(all_repos).most_common(10):
    print(f"{lang}: {count}")
