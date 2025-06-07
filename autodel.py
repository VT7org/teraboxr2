import asyncio
from telethon import TelegramClient, events
from motor.motor_asyncio import AsyncIOMotorClient
from config import API_ID, API_HASH, BOT_TOKEN, MONGO_DB_URL, DB_NAME  # Updated import
import time

# Initialize MongoDB client
mongo_client = AsyncIOMotorClient(MONGO_DB_URL)
bc = mongo_client[DB_NAME]
settings_collection = bc["settings"]
message_deletion_collection = bc["message_deletion"]

# Initialize Telegram client
bot = TelegramClient('bot_autodel', api_id=API_ID, api_hash=API_HASH).start(bot_token=BOT_TOKEN)  # Updated

# Default deletion time (5 minutes in seconds)
DEFAULT_DELETION_TIME = 5 * 60

# Store deletion times for users
async def get_deletion_time(user_id):
    setting = await settings_collection.find_one({"_id": f"deletion_time_{user_id}"})
    return setting["deletion_time"] if setting else DEFAULT_DELETION_TIME

async def set_deletion_time(user_id, minutes):
    seconds = minutes * 60
    await settings_collection.update_one(
        {"_id": f"deletion_time_{user_id}"},
        {"$set": {"deletion_time": seconds}},
        upsert=True
    )

# Command to set deletion time
@bot.on(events.NewMessage(pattern='/setdel (\d+)', incoming=True))
async def setdel_command(event):
    user_id = event.sender_id
    minutes = int(event.pattern_match.group(1))
    if minutes < 1:
        await event.reply("Deletion time must be at least 1 minute.")
        return
    await set_deletion_time(user_id, minutes)
    await event.reply(f"Deletion time set to {minutes} minutes.")

# Function to schedule message deletion
async def schedule_message_deletion(chat_id, message_id, user_id):
    deletion_time = await get_deletion_time(user_id)
    await message_deletion_collection.insert_one({
        "chat_id": chat_id,
        "message_id": message_id,
        "user_id": user_id,
        "delete_at": int(time.time()) + deletion_time
    })

# Background task to check and delete messages
async def delete_expired_messages():
    while True:
        current_time = int(time.time())
        expired_messages = message_deletion_collection.find({"delete_at": {"$lte": current_time}})
        async for msg in expired_messages:
            try:
                await bot.delete_messages(msg["chat_id"], [msg["message_id"]])
                await message_deletion_collection.delete_one({"_id": msg["_id"]})
            except Exception as e:
                print(f"Error deleting message {msg['message_id']}: {e}")
        await asyncio.sleep(60)  # Check every minute

# Start the deletion task
async def main():
    await bot.start(bot_token=BOT_TOKEN)
    print("Auto-deletion bot started successfully.")
    asyncio.create_task(delete_expired_messages())
    await bot.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
