"""
Test Bookmarks:
- get_bookmarks
- bookmark_tweet / delete_bookmark
- get_bookmark_folders
"""
import asyncio
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.dirname(__file__))

from conftest import get_client


async def main():
    client = await get_client()

    print("\n--- [1] get_bookmarks ---")
    bookmarks = await client.get_bookmarks(count=5)
    print(f"  Found {len(bookmarks)} bookmarks")
    for t in bookmarks:
        print(f"  [{t.id}] {t.text[:60]!r}")

    print("\n--- [2] bookmark_tweet ---")
    tweet = await client.create_tweet("Test bookmark tweet 🔖")
    await client.bookmark_tweet(tweet.id)
    print(f"  Bookmarked tweet {tweet.id}")

    print("\n--- [3] delete_bookmark ---")
    await client.delete_bookmark(tweet.id)
    print(f"  Deleted bookmark {tweet.id}")

    print("\n--- [4] get_bookmark_folders ---")
    try:
        folders = await client.get_bookmark_folders()
        print(f"  {len(folders)} folders")
        for f in folders:
            print(f"  - {f.name}")
    except Exception as e:
        print(f"  [INFO] {e}")

    await client.delete_tweet(tweet.id)
    print(f"\n  Deleted test tweet {tweet.id}")
    print("\n[DONE] test_bookmarks.py complete")


if __name__ == "__main__":
    asyncio.run(main())
