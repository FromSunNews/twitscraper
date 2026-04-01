# Protecting your account

Since twitscrape uses unofficial APIs, improper usage can lead to account suspension. Follow these guidelines:

## 1. Respect rate limits

Avoid hitting rate limits documented in [ratelimits.md](ratelimits.md). Add delays between requests:

```python
import asyncio

for user_id in user_ids:
    tweets = await client.get_user_tweets(user_id, "Tweets")
    # Process tweets...
    await asyncio.sleep(2)  # 2 second delay
```

## 2. Reuse cookies — don't login repeatedly

Logging in frequently triggers Twitter's anti-bot detection. Instead:

1. Get cookies once (from browser or via `client.login()`)
2. Save them: `client.save_cookies("cookies.json")`
3. Reuse them: `client = await create_client_from_file("cookies.json")`

## 3. Limit DMs and follows

Twitter monitors these actions closely:
- DMs: Keep under 50/day for new accounts
- Follows: Keep under 100/day

## 4. Avoid sensitive content

Don't tweet content that violates Twitter's ToS:
- Hate speech
- Violence
- Sexual content
- Spam

## 5. Use realistic delays

Mimic human behavior — don't send requests instantly back-to-back. Add random delays:

```python
import random

await asyncio.sleep(random.uniform(1, 3))
```

## 6. Rotate accounts for high-volume scraping

If scraping thousands of tweets, use multiple accounts and rotate between them to distribute load.

---

Use twitscrape responsibly!
