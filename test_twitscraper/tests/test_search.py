"""
Test Search:
- search_tweet (Latest / Top / Media)
- search_user
- pagination
"""
import asyncio
from conftest import get_client

QUERY = "AI"


async def main():
    client = await get_client()

    print(f"\n--- [1] search_tweet '{QUERY}' Latest (count=5) ---")
    latest = await client.search_tweet(QUERY, 'Latest', count=5)
    for t in latest:
        print(f"  @{t.user.screen_name}: {t.text[:60]!r}")

    print("\n--- [2] Pagination: next() ---")
    more = await latest.next()
    print(f"  Next page: {len(more)} tweets")
    for t in more[:3]:
        print(f"  @{t.user.screen_name}: {t.text[:60]!r}")

    print(f"\n--- [3] search_tweet '{QUERY}' Top ---")
    top = await client.search_tweet(QUERY, 'Top', count=5)
    for t in top:
        print(f"  [{t.id}] fav={t.favorite_count}")

    print(f"\n--- [4] search_tweet '{QUERY}' Media ---")
    media = await client.search_tweet(QUERY, 'Media', count=3)
    for t in media:
        print(f"  [{t.id}] media_count={len(t.media)}")

    print(f"\n--- [5] search_user '{QUERY}' ---")
    users = await client.search_user(QUERY, count=5)
    for u in users:
        print(f"  @{u.screen_name} - {u.name} ({u.followers_count} followers)")

    print("\n--- [6] search_user next() ---")
    more_users = await users.next()
    print(f"  Next page: {len(more_users)} users")

    print("\n[DONE] test_search.py complete")


if __name__ == "__main__":
    asyncio.run(main())
