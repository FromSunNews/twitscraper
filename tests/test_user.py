"""
Test User:
- user() (authenticated)
- get_user_by_screen_name / get_user_by_id
- get_user_tweets (Tweets / Media)
- get_user_followers / get_user_following
"""
import asyncio
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.dirname(__file__))

from conftest import get_client

TARGET_USER = "elonmusk"


async def main():
    client = await get_client()

    print("\n--- [1] Authenticated user ---")
    me = await client.user()
    print(f"  id={me.id}, name={me.name}, screen_name={me.screen_name}")
    print(f"  followers={me.followers_count}, following={me.following_count}")

    print(f"\n--- [2] get_user_by_screen_name: @{TARGET_USER} ---")
    user = await client.get_user_by_screen_name(TARGET_USER)
    print(f"  id={user.id}, name={user.name}")
    print(f"  followers={user.followers_count}, tweets={user.statuses_count}")
    print(f"  blue_verified={user.is_blue_verified}")

    print(f"\n--- [3] get_user_by_id: {user.id} ---")
    user2 = await client.get_user_by_id(user.id)
    print(f"  name={user2.name}, screen_name={user2.screen_name}")

    print(f"\n--- [4] get_user_tweets: Tweets ---")
    tweets = await client.get_user_tweets(user.id, 'Tweets', count=5)
    for t in tweets:
        print(f"  [{t.id}] {t.text[:80]!r}")

    print(f"\n--- [5] get_user_tweets: Media ---")
    media_tweets = await client.get_user_tweets(user.id, 'Media', count=3)
    for t in media_tweets:
        print(f"  [{t.id}] media={[m.__class__.__name__ for m in t.media]}")

    print(f"\n--- [6] get_user_followers (count=5) ---")
    try:
        followers = await client.get_user_followers(user.id, count=5)
        for u in followers:
            print(f"  @{u.screen_name} ({u.followers_count} followers)")
    except Exception as e:
        print(f"  [WARN] {e}")

    print(f"\n--- [7] get_user_following (count=5) ---")
    following = await client.get_user_following(user.id, count=5)
    for u in following:
        print(f"  @{u.screen_name}")

    print("\n[DONE] test_user.py complete")


if __name__ == "__main__":
    asyncio.run(main())
