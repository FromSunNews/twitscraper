# twitscraper

A Python library for interacting with Twitter/X — no API key required.

Uses cookie-based authentication and browser-level HTTP fingerprinting (`curl_cffi`) to bypass connection issues that affect standard `httpx` clients.

## Features

- No API key required
- Cookie-based auth — paste cookies from your browser, no login flow needed
- Supports 4 cookie input formats
- Async API built on `twikit` internals

## Install

```bash
pip install twitscraper
```

## Getting your cookies

1. Open [x.com](https://x.com) and log in
2. Open DevTools → Application → Cookies → `https://x.com`
3. Copy `auth_token` and `ct0` (minimum required)

Or use a browser extension like [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie) or [Cookie-Editor](https://cookie-editor.com) to export all cookies at once.

## Quick start

### From a dict

```python
import asyncio
from twitscraper import create_client

async def main():
    client = await create_client({
        "auth_token": "your_auth_token",
        "ct0": "your_ct0",
        "twid": "u%3D123456789",
    })

    me = await client.user()
    print(me.screen_name)

asyncio.run(main())
```

### From a JSON file

```python
from twitscraper import create_client_from_file

client = await create_client_from_file("cookies.json")
```

`cookies.json`:
```json
{
  "auth_token": "...",
  "ct0": "...",
  "twid": "u%3D123456789"
}
```

### From a raw cookie string (Network tab)

```python
from twitscraper import create_client_from_string

raw = "auth_token=abc123; ct0=xyz789; twid=u%3D123456789"
client = await create_client_from_string(raw)
```

### From a browser extension export

```python
from twitscraper import create_client_from_browser_export

# Paste the JSON array copied from EditThisCookie / Cookie-Editor
raw_json = '[{"name": "auth_token", "value": "...", "domain": ".x.com"}, ...]'
client = await create_client_from_browser_export(raw_json)
```

## Examples

**Search tweets**
```python
tweets = await client.search_tweet("python", "Latest")
for tweet in tweets:
    print(tweet.user.screen_name, tweet.text)
```

**Create a tweet**
```python
tweet = await client.create_tweet("Hello from twitscraper!")
```

**Upload media**
```python
media_id = await client.upload_media("image.jpg")
await client.create_tweet("Tweet with image", media_ids=[media_id])
```

**Send a DM**
```python
await client.send_dm("123456789", "Hello!")
```

**Get trends**
```python
trends = await client.get_trends("trending")
for t in trends:
    print(t.name)
```

**Download tweet media**
```python
tweet = await client.get_tweet_by_id("tweet_id")
for i, media in enumerate(tweet.media):
    if media.type == "photo":
        await media.download(f"photo_{i}.jpg")
    elif media.type == "video":
        await media.streams[-1].download(f"video_{i}.mp4")
```

**Listen for new tweets**
```python
import asyncio
from twitscraper import Tweet

async def on_new_tweet(tweet: Tweet):
    print(f"New tweet: {tweet.text}")

USER_ID = "44196397"
before = (await client.get_user_tweets(USER_ID, "Tweets", count=1))[0]

while True:
    await asyncio.sleep(60)
    latest = (await client.get_user_tweets(USER_ID, "Tweets", count=1))[0]
    if latest.id != before.id:
        await on_new_tweet(latest)
        before = latest
```

## Rate limits

See [ratelimits.md](ratelimits.md) for per-endpoint limits (reset every 15 minutes).

## License

MIT
