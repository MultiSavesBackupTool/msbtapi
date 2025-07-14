from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
from app import config

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Pyrogram client
bot = Client(
    "msbtapibot",
    api_hash=config.tg_api_hash,
    api_id=config.tg_api_id,
    bot_token=config.bot_token
)

async def send_moderation_request(request_id: str, request_type: str, request_data: dict):
    message_text = f"New {request_type} request (ID: {request_id}):\n```json\n{request_data}\n```"
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Approve", callback_data=f"moderate_approve_{request_id}"),
                InlineKeyboardButton("Deny", callback_data=f"moderate_deny_{request_id}")
            ]
        ]
    )
    try:
        await bot.send_message(chat_id=config.telegram_moderation_group_id, text=message_text, reply_markup=keyboard)
        logger.info(f"Sent moderation request {request_id} to Telegram.")
    except Exception as e:
        logger.error(f"Error sending moderation request to Telegram: {e}")

@bot.on_callback_query(filters.regex(r"moderate_(approve|deny)_.+"))
async def moderation_callback(client, callback_query):
    action, request_id = callback_query.data.replace("moderate_", "").split("_", 1)

    if callback_query.from_user.id != config.telegram_admin_user_id:
        await callback_query.answer("You are not authorized to perform this action.", show_alert=True)
        return

    # Import here to avoid circular dependency
    from app.main import process_moderation_action

    approved = True if action == "approve" else False
    success = await process_moderation_action(request_id, approved)

    if success:
        status = "Approved" if approved else "Denied"
        await callback_query.edit_message_text(
            f"{callback_query.message.text.split('```')[0]}```json\n{callback_query.message.text.split('```')[1]}\n```\n\n**Request {status} by {callback_query.from_user.first_name}**"
        )
        await callback_query.answer(f"Request {status}!")
    else:
        await callback_query.answer("Failed to process request.", show_alert=True)

async def start_bot():
    await bot.start()
    logger.info("Telegram Bot started.")

async def stop_bot():
    await bot.stop()
    logger.info("Telegram Bot stopped.") 