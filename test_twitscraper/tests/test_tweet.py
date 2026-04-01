"""
Test Tweet:
- search_tweet
- get_tweet_by_id
- create_tweet / delete_tweet
- favorite / unfavorite
- retweet / delete_retweet
- bookmark / delete_bookmark
- reply
- get_retweeters
"""
import asyncio
from conftest import get_client

SEARCH_QUERY = "python programming"
SAMPLE_TWEET_ID = "20"


async def main():
    client = await get_client()

    print("\n--- [1] search_tweet: Latest ---")
    results = await client.search_tweet(SEARCH_QUERY, 'Latest', count=5)
    for t in results:
        print(f"  @{t.user.screen_name}: {t.text[:70]!r}")

    print("\n--- [2] search_tweet: Top ---")
    top = await client.search_tweet(SEARCH_QUERY, 'Top', count=3)
    for t in top:
        print(f"  [{t.id}] fav={t.favorite_count} rt={t.retweet_count}")

    print(f"\n--- [3] get_tweet_by_id: {SAMPLE_TWEET_ID} ---")
    try:
        tweet = await client.get_tweet_by_id(SAMPLE_TWEET_ID)
        print(f"  text={tweet.text!r}")
    except Exception as e:
        print(f"  [SKIP] {e}")

    print("\n--- [4] create_tweet ---")
    new_tweet = await client.create_tweet(text="Test tweet from twitscraper 🐍 #test")
    print(f"  Created tweet id={new_tweet.id}")

    print("\n--- [5] reply ---")
    reply = await new_tweet.reply("Reply from twitscraper 👋")
    print(f"  Reply id={reply.id}, in_reply_to={reply.in_reply_to}")

    print("\n--- [6] favorite / unfavorite ---")
    await new_tweet.favorite()
    print(f"  Favorited {new_tweet.id}")
    await new_tweet.unfavorite()
    print(f"  Unfavorited {new_tweet.id}")

    print("\n--- [7] retweet / delete_retweet ---")
    await new_tweet.retweet()
    print(f"  Retweeted {new_tweet.id}")
    await new_tweet.delete_retweet()
    print(f"  Deleted retweet {new_tweet.id}")

    print("\n--- [8] bookmark / delete_bookmark ---")
    await new_tweet.bookmark()
    print(f"  Bookmarked {new_tweet.id}")
    await new_tweet.delete_bookmark()
    print(f"  Deleted bookmark {new_tweet.id}")

    print("\n--- [9] get_retweeters ---")
    try:
        retweeters = await client.get_retweeters(new_tweet.id, count=5)
        print(f"  {len(retweeters)} retweeters")
    except Exception as e:
        print(f"  [INFO] {e}")

    print("\n--- [10] delete_tweet ---")
    await client.delete_tweet(reply.id)
    print(f"  Deleted reply {reply.id}")
    await client.delete_tweet(new_tweet.id)
    print(f"  Deleted tweet {new_tweet.id}")

    print("\n[DONE] test_tweet.py complete")


if __name__ == "__main__":
    asyncio.run(main())
