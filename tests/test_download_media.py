"""
Test download_tweet_media:
- Find a tweet with media (photo / video / gif)
- Download each media type to /tmp/
"""
import asyncio
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.dirname(__file__))

from conftest import get_client

OUTPUT_DIR = "/tmp/twikit_media_test"


async def main():
    client = await get_client()
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Search for tweets with media to get real tweet IDs
    print("\n--- [1] Find tweets with media ---")
    results = await client.search_tweet("python", 'Media', count=5)
    media_tweets = [t for t in results if t.media]
    if not media_tweets:
        print("  [SKIP] No media tweets found in search results")
        return
    print(f"  Found {len(media_tweets)} tweets with media")

    # Download media from the first tweet that has it
    for tweet in media_tweets[:2]:
        print(f"\n--- [2] Downloading media from tweet {tweet.id} ---")
        for i, media in enumerate(tweet.media):
            print(f"  media[{i}] type={media.type}")
            try:
                if media.type == 'photo':
                    path = os.path.join(OUTPUT_DIR, f"photo_{tweet.id}_{i}.jpg")
                    await media.download(path)
                    size = os.path.getsize(path)
                    print(f"  Downloaded photo → {path} ({size} bytes)")

                elif media.type == 'animated_gif':
                    if media.streams:
                        path = os.path.join(OUTPUT_DIR, f"gif_{tweet.id}_{i}.mp4")
                        await media.streams[-1].download(path)
                        size = os.path.getsize(path)
                        print(f"  Downloaded gif → {path} ({size} bytes)")
                    else:
                        print("  [SKIP] No streams for gif")

                elif media.type == 'video':
                    if media.streams:
                        path = os.path.join(OUTPUT_DIR, f"video_{tweet.id}_{i}.mp4")
                        await media.streams[-1].download(path)
                        size = os.path.getsize(path)
                        print(f"  Downloaded video → {path} ({size} bytes)")
                    else:
                        print("  [SKIP] No streams for video")

            except Exception as e:
                print(f"  [WARN] {e}")

    print(f"\n  Output dir: {OUTPUT_DIR}")
    print("\n[DONE] test_download_media.py complete")


if __name__ == "__main__":
    asyncio.run(main())
