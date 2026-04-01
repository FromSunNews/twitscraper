"""
Test Timeline:
- get_timeline (Home)
- get_latest_timeline
- get_trends
"""
import asyncio
from conftest import get_client


async def main():
    client = await get_client()

    print("\n--- [1] get_timeline (Home) ---")
    try:
        timeline = await client.get_timeline(count=5)
        for t in timeline:
            print(f"  @{t.user.screen_name}: {t.text[:70]!r}")
    except Exception as e:
        print(f"  [WARN] {e}")

    print("\n--- [2] get_latest_timeline ---")
    try:
        latest = await client.get_latest_timeline(count=5)
        for t in latest:
            print(f"  @{t.user.screen_name}: {t.text[:70]!r}")
    except Exception as e:
        print(f"  [WARN] {e}")

    print("\n--- [3] get_trends: trending ---")
    try:
        trends = await client.get_trends('trending', retry=False,
                                         additional_request_params={'candidate_source': 'trends'})
        for trend in trends[:10]:
            print(f"  {trend.name}")
    except Exception as e:
        print(f"  [WARN] {e}")

    print("\n--- [4] get_trends: news ---")
    try:
        news = await client.get_trends('news', retry=False)
        for trend in news[:5]:
            print(f"  {trend.name}")
    except Exception as e:
        print(f"  [WARN] {e}")

    print("\n[DONE] test_timeline.py complete")


if __name__ == "__main__":
    asyncio.run(main())
