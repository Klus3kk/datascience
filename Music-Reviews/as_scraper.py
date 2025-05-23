import requests
import pandas as pd
from time import sleep
from datetime import datetime

APP_IDS = {
    "Apple Music": "1108187390",
    "Spotify": "324684580",
    "TIDAL": "913943275",
    "SoundCloud": "336353151",
    "Deezer": "292738169",
    "Shazam": "284993459"
}

COUNTRY_CODES = [
    "us", "gb", "ca", "de", "fr", "it", "es", "pl", "nl", "se",
    "no", "fi", "au", "nz", "jp", "kr", "ru", "br", "mx", "in"
]

MAX_REVIEWS_PER_APP = 1000  
OUTPUT_FILE = "app_store_music_reviews.csv"

reviews = []

def fetch_reviews(app_id, country, app_name):
    url = f"https://itunes.apple.com/{country}/rss/customerreviews/id={app_id}/json"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        entries = data.get('feed', {}).get('entry', [])

        if isinstance(entries, dict):  # only one review
            entries = [entries]

        for entry in entries:
            if not isinstance(entry, dict): continue
            review_text = entry.get("content", {}).get("label")
            rating = entry.get("im:rating", {}).get("label")
            date = entry.get("updated", {}).get("label")
            title = entry.get("title", {}).get("label", "")
            author = entry.get("author", {}).get("name", {}).get("label", "")

            if review_text and rating:
                reviews.append({
                    "app": app_name,
                    "country": country.upper(),
                    "title": title,
                    "review": review_text,
                    "rating": int(rating),
                    "date": date,
                    "scraped_at": datetime.utcnow().isoformat()
                })

    except Exception as e:
        print(f"Error for {app_name} in {country.upper()}: {e}")

for app_name, app_id in APP_IDS.items():
    print(f"Scraping {app_name}...")
    for country in COUNTRY_CODES:
        fetch_reviews(app_id, country, app_name)
        sleep(0.3)

df = pd.DataFrame(reviews)
df.to_csv(OUTPUT_FILE, index=False)
print(f"Saved {len(df)} reviews to '{OUTPUT_FILE}'")
