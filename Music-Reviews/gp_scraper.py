from google_play_scraper import Sort, reviews
import pandas as pd
import time

APP_PACKAGES = [
    "com.spotify.music",
    "com.apple.android.music",
    "com.soundcloud.android",
    "com.aspiro.tidal",
    "deezer.android.app",
    "com.shazam.android",
    "com.google.android.music"
]

REVIEWS_PER_APP = 15000  
BATCH_SIZE = 200  
OUTPUT_FILE = "google_play_music_reviews.csv"

reviews = []

for app in APP_PACKAGES:
    print(f"Fetching reviews for: {app}")
    count = 0
    continuation_token = None

    while count < REVIEWS_PER_APP:
        try:
            result, continuation_token = reviews(
                app,
                lang="en",
                country="us",
                sort=Sort.NEWEST,
                count=BATCH_SIZE,
                continuation_token=continuation_token
            )
            for r in result:
                reviews.append({
                    "app": app,
                    "review": r.get("content"),
                    "rating": r.get("score"),
                    "thumbs_up": r.get("thumbsUpCount"),
                    "version": r.get("reviewCreatedVersion"),
                    "date": r.get("at"),
                    "device": r.get("device")
                })
            count += len(result)
            print(f"{count} reviews collected so far.")
            if continuation_token is None:
                break
            time.sleep(0.1)
        except Exception as e:
            print(f"Error fetching for {app}: {e}")
            break
        
df = pd.DataFrame(reviews)
df.to_csv(OUTPUT_FILE, index=False)
print(f"Saved {len(df)} reviews to '{OUTPUT_FILE}'")
