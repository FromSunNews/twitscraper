"""
Run all tests in order.
"""
import asyncio
import importlib
import os
import sys
import traceback
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.dirname(__file__))

TESTS = [
    ("test_user",       "User info, followers, following"),
    ("test_search",     "Search tweets & users"),
    ("test_timeline",   "Timeline & Trends"),
    ("test_tweet",      "Create/delete/favorite/retweet"),
    ("test_bookmarks",  "Bookmarks"),
    ("test_media",      "Upload media & Poll"),
    ("test_dm",         "Direct Messages"),
]


async def run_test(module_name: str, description: str) -> bool:
    print(f"\n{'='*60}")
    print(f"  {module_name}: {description}")
    print(f"{'='*60}")
    try:
        mod = importlib.import_module(module_name)
        await mod.main()
        print(f"\n  ✅ {module_name} PASSED")
        return True
    except Exception as e:
        print(f"\n  ❌ {module_name} FAILED: {e}")
        traceback.print_exc()
        return False


async def main():
    # First verify all cookie loading methods
    from conftest import _test_all_methods
    await _test_all_methods()

    results = {}
    for module_name, description in TESTS:
        results[module_name] = await run_test(module_name, description)

    print(f"\n{'='*60}")
    print("  RESULTS")
    print(f"{'='*60}")
    for name, ok in results.items():
        print(f"  {'✅ PASS' if ok else '❌ FAIL'}  {name}")

    passed = sum(results.values())
    print(f"\n  {passed}/{len(results)} tests passed")


if __name__ == "__main__":
    asyncio.run(main())
