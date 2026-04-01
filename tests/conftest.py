"""
conftest.py - Tests all 4 cookie loading methods from twitscraper.factory.

Place your cookies in one of these locations (checked in order):
  1. tests/cookies.json       - JSON dict  {"auth_token": ..., "ct0": ...}
  2. TWIKIT_COOKIES env var   - path to a JSON file
  3. TWIKIT_COOKIE_STR env var - raw cookie string "auth_token=...; ct0=..."
  4. TWIKIT_COOKIE_EXPORT env var - browser extension JSON array export

Run:
    cd ref/twikit
    python tests/conftest.py
"""
import asyncio
import json
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from twitscraper import (
    create_client,
    create_client_from_file,
    create_client_from_string,
    create_client_from_browser_export,
)

_DEFAULT_COOKIES_FILE = os.path.join(os.path.dirname(__file__), 'cookies.json')


async def get_client():
    """
    Try all 4 loading methods in order and return the first that works.
    """

    # --- Method 1: tests/cookies.json (dict format) ---
    if os.path.exists(_DEFAULT_COOKIES_FILE):
        print("[cookies] Loading from tests/cookies.json (dict)")
        return await create_client_from_file(_DEFAULT_COOKIES_FILE)

    # --- Method 2: TWIKIT_COOKIES env var (path to JSON file) ---
    env_file = os.environ.get('TWIKIT_COOKIES')
    if env_file and os.path.exists(env_file):
        print(f"[cookies] Loading from file: {env_file}")
        return await create_client_from_file(env_file)

    # --- Method 3: TWIKIT_COOKIE_STR env var (raw cookie string) ---
    env_str = os.environ.get('TWIKIT_COOKIE_STR')
    if env_str:
        print("[cookies] Loading from TWIKIT_COOKIE_STR (raw string)")
        return await create_client_from_string(env_str)

    # --- Method 4: TWIKIT_COOKIE_EXPORT env var (browser extension JSON export) ---
    env_export = os.environ.get('TWIKIT_COOKIE_EXPORT')
    if env_export:
        print("[cookies] Loading from TWIKIT_COOKIE_EXPORT (browser export)")
        return await create_client_from_browser_export(env_export)

    raise RuntimeError(
        "No cookies found. Provide one of:\n"
        "  1. tests/cookies.json\n"
        "  2. TWIKIT_COOKIES=/path/to/cookies.json\n"
        "  3. TWIKIT_COOKIE_STR='auth_token=...; ct0=...'\n"
        "  4. TWIKIT_COOKIE_EXPORT='[{\"name\":\"auth_token\",...}]'"
    )


async def _test_all_methods():
    """Verify all 4 loading methods work with the available cookies."""

    if not os.path.exists(_DEFAULT_COOKIES_FILE):
        print("[SKIP] tests/cookies.json not found, skipping method tests")
        return

    with open(_DEFAULT_COOKIES_FILE) as f:
        cookies_dict = json.load(f)

    results = {}

    # Method 1: dict
    try:
        c = await create_client(cookies_dict)
        me = await c.user()
        results['create_client(dict)'] = f"OK - @{me.screen_name}"
    except Exception as e:
        results['create_client(dict)'] = f"FAIL - {e}"

    # Method 2: file
    try:
        c = await create_client_from_file(_DEFAULT_COOKIES_FILE)
        me = await c.user()
        results['create_client_from_file'] = f"OK - @{me.screen_name}"
    except Exception as e:
        results['create_client_from_file'] = f"FAIL - {e}"

    # Method 3: raw string
    try:
        raw = '; '.join(f"{k}={v}" for k, v in cookies_dict.items())
        c = await create_client_from_string(raw)
        me = await c.user()
        results['create_client_from_string'] = f"OK - @{me.screen_name}"
    except Exception as e:
        results['create_client_from_string'] = f"FAIL - {e}"

    # Method 4: browser export format
    try:
        export = [{"name": k, "value": v, "domain": ".x.com"} for k, v in cookies_dict.items()]
        c = await create_client_from_browser_export(export)
        me = await c.user()
        results['create_client_from_browser_export'] = f"OK - @{me.screen_name}"
    except Exception as e:
        results['create_client_from_browser_export'] = f"FAIL - {e}"

    print("\n=== Cookie loading methods ===")
    for method, result in results.items():
        status = "✅" if result.startswith("OK") else "❌"
        print(f"  {status} {method}: {result}")


if __name__ == "__main__":
    asyncio.run(_test_all_methods())
