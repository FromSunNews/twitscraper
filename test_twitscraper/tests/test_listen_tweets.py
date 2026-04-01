"""
Test listen_for_new_tweets:
- Poll a user's timeline every N seconds
- Fire callback khi có tweet mới
"""
import asyncio
from twitscraper import Tweet
from conftest import get_client

WATCH_USER_ID = "44196397"  # elonmusk
CHECK_INTERVAL = 10
MAX_POLLS = 3


def on_new_tweet(tweet: Tweet) -> None:
    print(f"  🆕 New tweet: [{tweet.id}] {tweet.text[:80]!r}")


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
        if latest.id != before.id and latest.created_at_datetime > before.created_at_datetime:
            on_new_tweet(latest)
            before = latest
        else:
            print(f"  No new tweet (still [{before.id}])")

    print("\n[DONE] test_listen_tweets.py complete")


if __name__ == "__main__":
    asyncio.run(main())
