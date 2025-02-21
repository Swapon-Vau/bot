import logging
import subprocess
import sys

# Function to install missing package using pip
def install_package(package: str):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Try importing google.generativeai, and install if not found
try:
    import google.generativeai as genai
except ModuleNotFoundError:
    print("google.generativeai module not found. Installing...")
    install_package("google-generativeai")
    import google.generativeai as genai

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables (make sure to replace with actual values)
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"

# Configure Gemini AI
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Telegram bot functions
def start(update, context):
    update.message.reply_text("Hello! I am your DMart bot. Send me a message, and I will respond using Gemini AI!")

def handle_message(update, context):
    user_message = update.message.text
    try:
        response = model.generate_content(user_message)
        bot_reply = response.text if hasattr(response, 'text') else "Sorry, I couldn't understand that."
    except Exception as e:
        bot_reply = "Error processing your request. Please try again later."
        logger.error(f"Error: {e}")
    
    update.message.reply_text(bot_reply)

# Main function to set up the bot
def main():
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
    
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
