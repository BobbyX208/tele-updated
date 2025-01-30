import os
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Load environment variables from .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Request Mod", callback_data='request_mod')],
        [InlineKeyboardButton("Report Error", callback_data='report_error')],
        [InlineKeyboardButton("Suggest Feature", callback_data='suggest_feature')],
        [InlineKeyboardButton("Chat with Admin", callback_data='chat_admin')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Please choose an option:', reply_markup=reply_markup)

# Handle button clicks
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

# Handle user messages
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

# Main function
def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == '__main__':
    main()
