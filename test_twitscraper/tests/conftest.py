"""
conftest.py - Load cookies cho test_twitscraper.
Ưu tiên: cookies.json > TWIKIT_COOKIES > TWIKIT_COOKIE_STR > TWIKIT_COOKIE_EXPORT
"""
import asyncio
import json
import os

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

from twitscraper import (
    create_client,
    create_client_from_file,
    create_client_from_string,
    create_client_from_browser_export,
)

_DEFAULT_COOKIES_FILE = os.path.join(os.path.dirname(__file__), '..', 'cookies.json')


async def get_client():
    if os.path.exists(_DEFAULT_COOKIES_FILE):
        print("[cookies] Loading from cookies.json")
        return await create_client_from_file(_DEFAULT_COOKIES_FILE)

    env_file = os.environ.get('TWIKIT_COOKIES')
    if env_file and os.path.exists(env_file):
        print(f"[cookies] Loading from file: {env_file}")
        return await create_client_from_file(env_file)

    env_str = os.environ.get('TWIKIT_COOKIE_STR')
    if env_str:
        print("[cookies] Loading from TWIKIT_COOKIE_STR")
        return await create_client_from_string(env_str)

    env_export = os.environ.get('TWIKIT_COOKIE_EXPORT')
    if env_export:
        print("[cookies] Loading from TWIKIT_COOKIE_EXPORT")
        return await create_client_from_browser_export(env_export)

    raise RuntimeError(
        "No cookies found. Provide one of:\n"
        "  1. cookies.json\n"
        "  2. TWIKIT_COOKIES=/path/to/cookies.json\n"
        "  3. TWIKIT_COOKIE_STR='auth_token=...; ct0=...'\n"
        "  4. TWIKIT_COOKIE_EXPORT='[{\"name\":\"auth_token\",...}]'"
    )


async def _test_all_methods():
    if not os.path.exists(_DEFAULT_COOKIES_FILE):
        print("[SKIP] cookies.json not found")
        return

    with open(_DEFAULT_COOKIES_FILE) as f:
        cookies_dict = json.load(f)

    results = {}

    try:
        c = await create_client(cookies_dict)
        me = await c.user()
        results['create_client(dict)'] = f"OK - @{me.screen_name}"
    except Exception as e:
        results['create_client(dict)'] = f"FAIL - {e}"

    try:
        c = await create_client_from_file(_DEFAULT_COOKIES_FILE)
        me = await c.user()
        results['create_client_from_file'] = f"OK - @{me.screen_name}"
    except Exception as e:
        results['create_client_from_file'] = f"FAIL - {e}"

    try:
        raw = '; '.join(f"{k}={v}" for k, v in cookies_dict.items())
        c = await create_client_from_string(raw)
        me = await c.user()
        results['create_client_from_string'] = f"OK - @{me.screen_name}"
    except Exception as e:
        results['create_client_from_string'] = f"FAIL - {e}"

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
