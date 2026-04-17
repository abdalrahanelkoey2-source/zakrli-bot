import time
import asyncio
import random
from telethon import TelegramClient, functions, types

# --- بياناتك ---
API_ID = 34459951
API_HASH = '5a05195164987f68a284e7cf8025a9c6'
BOT_USERNAME = 'ZakrLi_ViP1_Bot'
GROUP_USERNAME = 'ZakrLi_ViP'

client = TelegramClient('zakrli_session', API_ID, API_HASH)

async def refresh():
    while True:
        try:
            # وقت انتظار عشوائي بين 23 و 26 دقيقة
            wait_time = random.randint(23 * 60, 26 * 60)
            print(f"[{time.strftime('%H:%M:%S')}] التجديد القادم بعد {wait_time // 60} دقيقة...")
            
            # 1. مغادرة المجموعة
            try: await client(functions.channels.LeaveChannelRequest(channel=GROUP_USERNAME))
            except: pass

            await asyncio.sleep(random.randint(5, 15))
            await client.send_message(BOT_USERNAME, '/start')
            
            await asyncio.sleep(random.randint(5, 10))
            messages = await client.get_messages(BOT_USERNAME, limit=1)
            if messages and messages[0].reply_markup:
                for row in messages[0].reply_markup.rows:
                    for button in row.buttons:
                        if "تجربة" in button.text:
                            await messages[0].click(button)
                            await asyncio.sleep(random.randint(5, 10))
                            break

            # 2. الانضمام بالرابط الجديد
            new_messages = await client.get_messages(BOT_USERNAME, limit=1)
            if new_messages and new_messages[0].reply_markup:
                for row in new_messages[0].reply_markup.rows:
                    for button in row.buttons:
                        if isinstance(button, types.KeyboardButtonUrl):
                            hash_link = button.url.split('/')[-1].replace('+', '')
                            await client(functions.messages.ImportChatInviteRequest(hash_link))
                            print("✅ تم التجديد بنجاح.")
                            break

            await asyncio.sleep(wait_time)
        except Exception as e:
            print(f"خطأ: {e}")
            await asyncio.sleep(60)

async def main():
    await client.start()
    print("🚀 نظام ZakrLi يعمل الآن على Koyeb...")
    await refresh()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
