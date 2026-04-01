"""
Test cơ bản - pip install twitscraper
"""
import asyncio
import json
import os

from dotenv import load_dotenv
load_dotenv()

COOKIES_FILE = os.path.join(os.path.dirname(__file__), 'cookies.json')


async def main():
    from twitscraper import create_client, create_client_from_file, create_client_from_string

    print("=" * 50)
    print("twitscraper - Basic Test")
    print("=" * 50)

    # Load client theo thứ tự ưu tiên
    if os.path.exists(COOKIES_FILE):
        print(f"\n[cookies] From cookies.json")
        client = await create_client_from_file(COOKIES_FILE)
    elif os.environ.get('TWIKIT_COOKIE_STR'):
        print(f"\n[cookies] From TWIKIT_COOKIE_STR env")
        client = await create_client_from_string(os.environ['TWIKIT_COOKIE_STR'])
    else:
        raise RuntimeError("Cần cookies.json hoặc TWIKIT_COOKIE_STR trong .env")

    # Test 1: user hiện tại
    print("\n[1] Get current user...")
    me = await client.user()
    print(f"    ✅ @{me.screen_name} ({me.name})")
    print(f"       followers={me.followers_count}, following={me.following_count}")

    # Test 2: search tweets
    print("\n[2] Search tweets: 'python'...")
    results = await client.search_tweet('python', product='Top')
    tweets = list(results)[:3]
    for i, t in enumerate(tweets, 1):
        print(f"    [{i}] @{t.user.screen_name}: {t.text[:80]}")

    print("\n✅ All tests passed!")


if __name__ == "__main__":
    asyncio.run(main())
