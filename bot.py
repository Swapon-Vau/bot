import logging
import subprocess
import sys
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Function to install missing packages
def install_package(package: str):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Try importing google.generativeai, and install google package if not found
try:
    import google.generativeai as genai
except ModuleNotFoundError:
    print("google.generativeai module not found. Installing google and google-generativeai...")
    install_package("google")
    install_package("google-generativeai")
    import google.generativeai as genai

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Command to start the bot
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hello! I am your DMart bot. Send me a message, and I will respond using Gemini AI!")

# Handle user messages and generate response
def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    try:
        # Generate a response from Gemini
        response = model.generate_content(user_message)
        bot_reply = response.text if hasattr(response, 'text') else "Sorry, I couldn't understand that."
    except Exception as e:
        bot_reply = "Error processing your request. Please try again later."
        logger.error(f"Error: {e}")
    
    update.message.reply_text(bot_reply)

# Main function to set up the bot and handlers
def main():
    # Initialize the Telegram bot application
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers for start command and messages
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot
    logger.info("Bot is running...")
    app.run_polling()

# Run the bot
if __name__ == "__main__":
    main()
