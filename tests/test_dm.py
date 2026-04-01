"""
Test Direct Messages:
- send_dm
- get_dm_history
"""
import asyncio
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.dirname(__file__))

from conftest import get_client

# Set a target user_id, or leave None to use self DM
DM_TARGET_USER_ID = None


async def main():
    client = await get_client()

    if DM_TARGET_USER_ID is None:
        me = await client.user()
        target_id = me.id
        print(f"[INFO] Using self DM, id={target_id}")
    else:
        target_id = DM_TARGET_USER_ID

    print(f"\n--- [1] send_dm to {target_id} ---")
    msg = await client.send_dm(target_id, "Test DM from twitscraper 🤖")
    print(f"  Message id={msg.id}, text={msg.text!r}")

    print(f"\n--- [2] get_dm_history ---")
    history = await client.get_dm_history(target_id)
    for m in list(history)[:5]:
        print(f"  [{m.id}] {m.text!r}")

    print("\n[DONE] test_dm.py complete")


if __name__ == "__main__":
    asyncio.run(main())
