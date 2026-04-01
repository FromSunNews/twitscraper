"""
Test Direct Messages:
- send_dm
- get_dm_history
"""
import asyncio
from conftest import get_client

# None = self DM
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
