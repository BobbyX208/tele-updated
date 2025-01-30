import os
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from flask import Flask
import threading

# Initialize Flask server
app = Flask(__name__)

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))

# Telegram bot handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Request Mod", callback_data='request_mod')],
        [InlineKeyboardButton("Report Error", callback_data='report_error')],
        [InlineKeyboardButton("Suggest Feature", callback_data='suggest_feature')],
        [InlineKeyboardButton("Chat with Admin", callback_data='chat_admin')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Please choose an option:', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'request_mod':
        await query.edit_message_text(text="Please send details of the mod you want.")
        context.user_data['awaiting_mod_request'] = True
    elif query.data == 'report_error':
        await query.edit_message_text(text="Please describe the error you encountered.")
        context.user_data['awaiting_error_report'] = True
    elif query.data == 'suggest_feature':
        await query.edit_message_text(text="Please describe your feature suggestion.")
        context.user_data['awaiting_feature_suggestion'] = True
    elif query.data == 'chat_admin':
        await query.edit_message_text(text="Send your message, and the admin will respond.")
        context.user_data['chatting_with_admin'] = True

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    user_id = update.message.chat_id
    username = update.message.from_user.username or "Unknown User"

    if context.user_data.get('awaiting_mod_request'):
        await context.bot.send_message(ADMIN_CHAT_ID, f"🔹 *Mod Request* from @{username}:\n{user_message}")
        await update.message.reply_text("Your mod request has been sent to the admin.")
        context.user_data['awaiting_mod_request'] = False

    elif context.user_data.get('awaiting_error_report'):
        await context.bot.send_message(ADMIN_CHAT_ID, f"⚠ *Error Report* from @{username}:\n{user_message}")
        await update.message.reply_text("Your error report has been sent to the admin.")
        context.user_data['awaiting_error_report'] = False

    elif context.user_data.get('awaiting_feature_suggestion'):
        await context.bot.send_message(ADMIN_CHAT_ID, f"💡 *Feature Suggestion* from @{username}:\n{user_message}")
        await update.message.reply_text("Your feature suggestion has been sent to the admin.")
        context.user_data['awaiting_feature_suggestion'] = False

    elif context.user_data.get('chatting_with_admin'):
        await context.bot.send_message(ADMIN_CHAT_ID, f"📩 *Message from @{username}*:\n{user_message}")
        await update.message.reply_text("Your message has been sent to the admin.")

# Dummy Flask server to keep Koyeb happy
@app.route('/')
def health_check():
    return "Bot is running"

# Main function to run the bot and Flask server
def run():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

# Run Flask server in a separate thread
def start_flask():
    app.run(host='0.0.0.0', port=8000)

if __name__ == '__main__':
    # Start the Flask server in a separate thread
    threading.Thread(target=start_flask).start()
    # Run the Telegram bot
    run()
