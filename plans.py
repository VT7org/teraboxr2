# plans.py
from telethon import events
from config import ADMINS

async def plans_command(m):
    user_id = m.sender_id
    user = await m.client.get_entity(user_id)

    if user_id in ADMINS:
        # Premium user
        reply_text = f"You are already a premium user, {user.first_name}! ðŸŒŸ"
    else:
        # Free user
        full_name = user.first_name + (f" {user.last_name}" if user.last_name else "")
        reply_text = f"User ID: {user_id}\nName: {full_name}\n\nðŸ’  Premium\n\n  âœ“ Download Upto 2.0 GB\n  âœ“ Task Limit: NO LIMIT\n  âœ“ Time Gap: NO\n  âœ“ No Anti-Spam Timer\n  âœ“ Validity: 1 MONTH\n\n  Amount: 60 INR â‚¹\n\nBUY NOW FROM : @x_ifeelram or @Trashxd"

    await m.reply(reply_text, parse_mode="markdown")


COOKIE = """browserid=YNi1qZmU9YcaF5yXArpUtpMe9sEVRbb7vUsf8kY2t-oeJtrUBxm2GsTFA1y9W-E7SKYW_KSJPN-6wDly; lang=en; TSID=BIVYynQUydq0LDhvQPLHG8IWe6wIJwdG; ndus=YfsAzKyteHuiK1MczOwlvnKVfIJmUO9C5_qB0j9j; csrfToken=Z9e1PR18XQs-m3HZ7i7khyfN; __bid_n=18f3031a7a6941cc4c4207; __stripe_mid=5eeb8285-c1a9-4dac-be34-58e9f3ecaa39d7df03; __stripe_sid=63d257f4-02c9-47ce-a099-a8b3876f9fd9237dfb; ndut_fmt=1C7BF505462B582A202CDE68F8435AC1B144A46B0022AC64A9EA30434A124ED0"""
