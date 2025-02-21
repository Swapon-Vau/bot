import logging
import os
import subprocess
import sys

# Function to install missing packages
def install_package(package: str):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Attempt to import the google.generativeai module, install if not available
try:
    import google.generativeai as genai
except ModuleNotFoundError:
    print("google.generativeai not found, installing...")
    install_package("google-generativeai")
    import google.generativeai as genai

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
TELEGRAM_BOT_TOKEN = "7908149234:AAHDOFkFjA4yDJGl9IWH2d5GDLoK1IVt19E"
GEMINI_API_KEY = "AIzaSyDDi2gNzOcPrcHe4i_FpZvCQiRpHUpiUOI"

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
    
    logger.info("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
