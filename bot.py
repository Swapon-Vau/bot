import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import google.generativeai as genai

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hello! I am your DMart bot. Send me a message, and I will respond using Gemini AI!")

def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    try:
        response = model.generate_content(user_message)
        bot_reply = response.text if hasattr(response, 'text') else "Sorry, I couldn't understand that."
    except Exception as e:
        bot_reply = "Error processing your request. Please try again later."
        logger.error(f"Error: {e}")
    
    update.message.reply_text(bot_reply)

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
