"""
Test listen_for_new_tweets:
- Poll a user's timeline every N seconds
- Fire a callback when a new tweet is detected

This test runs for a short duration (3 polls) instead of looping forever.
"""
import asyncio
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.dirname(__file__))

from twitscraper import Tweet
from conftest import get_client

# User to watch (elonmusk posts frequently)
WATCH_USER_ID = "44196397"
CHECK_INTERVAL = 10   # seconds between polls (short for testing)
MAX_POLLS = 3         # stop after this many polls


def on_new_tweet(tweet: Tweet) -> None:
    print(f"  🆕 New tweet detected: [{tweet.id}] {tweet.text[:80]!r}")


async def main():
    client = await get_client()

    print(f"\n--- Listening for new tweets from user {WATCH_USER_ID} ---")
    print(f"    interval={CHECK_INTERVAL}s, max_polls={MAX_POLLS}\n")

    tweets = await client.get_user_tweets(WATCH_USER_ID, 'Tweets', count=1)
    if not tweets:
        print("  [SKIP] Could not fetch initial tweet")
        return

    before = tweets[0]
    print(f"  Latest tweet at start: [{before.id}] {before.text[:80]!r}")

    for poll in range(1, MAX_POLLS + 1):
        print(f"\n  Poll {poll}/{MAX_POLLS} — waiting {CHECK_INTERVAL}s...")
        await asyncio.sleep(CHECK_INTERVAL)

        latest_tweets = await client.get_user_tweets(WATCH_USER_ID, 'Tweets', count=1)
        if not latest_tweets:
            print("  [WARN] Empty result, skipping")
            continue

        latest = latest_tweets[0]
        if (
            latest.id != before.id
            and latest.created_at_datetime > before.created_at_datetime
        ):
            on_new_tweet(latest)
            before = latest
        else:
            print(f"  No new tweet (still [{before.id}])")

    print("\n[DONE] test_listen_tweets.py complete")


if __name__ == "__main__":
    asyncio.run(main())
