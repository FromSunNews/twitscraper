"""
Test Media:
- upload_media (image)
- create_tweet with media
- create_poll
- vote
"""
import asyncio
import os
import urllib.request
from conftest import get_client

TEST_IMAGE_URL = "https://www.gstatic.com/webp/gallery/1.jpg"
TEST_IMAGE_PATH = "/tmp/twikit_test_image.jpg"


async def main():
    client = await get_client()

    if not os.path.exists(TEST_IMAGE_PATH):
        print("[INFO] Downloading test image...")
        urllib.request.urlretrieve(TEST_IMAGE_URL, TEST_IMAGE_PATH)

    print("\n--- [1] upload_media ---")
    media_id = await client.upload_media(TEST_IMAGE_PATH)
    print(f"  media_id={media_id}")

    print("\n--- [2] create_tweet with media ---")
    tweet = await client.create_tweet(
        text="Test tweet with image from twitscraper 📸",
        media_ids=[media_id]
    )
    print(f"  Tweet id={tweet.id}")
    print(f"  Media: {[m.__class__.__name__ for m in tweet.media]}")

    print("\n--- [3] create_poll ---")
    poll_uri = await client.create_poll(
        choices=["Python", "JavaScript", "Go"],
        duration_minutes=60
    )
    print(f"  poll_uri={poll_uri}")
    poll_tweet = await client.create_tweet(
        text="Test poll from twitscraper 📊",
        poll_uri=poll_uri
    )
    print(f"  Poll tweet id={poll_tweet.id}")

    print("\n--- [4] vote ---")
    if poll_tweet.poll:
        updated = await client.vote("1", poll_tweet.poll.id, poll_tweet.id, poll_tweet.poll.name)
        print(f"  Voted choice 1: {updated.choices}")
    else:
        print("  [INFO] Poll not loaded yet, fetching again...")
        refreshed = await client.get_tweet_by_id(poll_tweet.id)
        if refreshed.poll:
            print(f"  Poll choices: {refreshed.poll.choices}")

    await client.delete_tweet(tweet.id)
    await client.delete_tweet(poll_tweet.id)
    print("\n  Deleted test tweets")
    print("\n[DONE] test_media.py complete")


if __name__ == "__main__":
    asyncio.run(main())
