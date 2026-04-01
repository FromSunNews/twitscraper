# twitscraper - Test Suite

Integration tests for the `twitscraper` package using real Twitter/X cookies.

## Setup

**1. Install dependencies**
```bash
pip install -r requirements.txt
```

**2. Add your cookies**

Option A — `cookies.json` (recommended):
```bash
cp .env.example .env
# or create cookies.json directly
```

`cookies.json` format:
```json
{
  "auth_token": "your_auth_token",
  "ct0": "your_ct0",
  "twid": "u%3Dyour_user_id"
}
```

Option B — `.env` file:
```env
# Path to a cookies JSON file
TWIKIT_COOKIES=/path/to/cookies.json

# Or raw cookie string from browser DevTools (Network → Cookie header)
TWIKIT_COOKIE_STR=auth_token=abc; ct0=xyz; twid=u%3D123

# Or browser extension export (EditThisCookie / Cookie-Editor JSON array)
TWIKIT_COOKIE_EXPORT=[{"name":"auth_token","value":"...","domain":".x.com"}]
```

## Getting your cookies

1. Open [x.com](https://x.com) and log in
2. DevTools (F12) → Application → Cookies → `https://x.com`
3. Copy `auth_token`, `ct0`, and `twid`

Or use [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie) / [Cookie-Editor](https://cookie-editor.com) to export all cookies as JSON.

## Run tests

**Run a single test:**
```bash
cd tests
python test_search.py
python test_user.py
python test_tweet.py
```

**Run all tests:**
```bash
cd tests
python run_all.py
```

## Test files

| File | Description |
|------|-------------|
| `test_basic.py` | Smoke test — login + search |
| `test_user.py` | User info, followers, following |
| `test_search.py` | Search tweets & users, pagination |
| `test_timeline.py` | Home timeline & trends |
| `test_tweet.py` | Create/delete/favorite/retweet/reply |
| `test_bookmarks.py` | Bookmarks CRUD |
| `test_media.py` | Upload image, create poll, vote |
| `test_download_media.py` | Download photo/video/gif |
| `test_listen_tweets.py` | Poll for new tweets |
| `test_dm.py` | Send & read DMs |

## Notes

- `cookies.json` and `.env` are gitignored — never commit credentials
- Tests make real API calls and may create/delete tweets on your account
- `test_listen_tweets.py` runs for ~30s (3 polls × 10s interval)
- `test_dm.py` defaults to self-DM; set `DM_TARGET_USER_ID` to test with another user
