import asyncio
import logging
import os
from collections import deque
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from openai import AsyncOpenAI

# Load environment variables from .env file
load_dotenv()

# Load API keys and tokens from environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Define GPT CHAT Params
GPTCHAT_MODEL = 'gpt-4o-mini'
MESSAGE_HISTORY_LIMIT = 50  # Number of previous messages to include

# Load text files
def load_text_file(filename):
    with open(filename, 'r') as file:
        return file.read().strip()

# Load bot instructions and command texts
BOT_INSTRUCTIONS = load_text_file('bot_instructions.txt')
START_TEXT = load_text_file('com_start.txt')
HELP_TEXT = load_text_file('com_help.txt')
INFO_TEXT = load_text_file('com_info.txt')

# Set up your OpenAI API client
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Dictionary to store user message history
user_histories = {}

# Function to handle the start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Received /start command from {update.effective_user.first_name}")
    user_histories[update.effective_user.id] = deque(maxlen=MESSAGE_HISTORY_LIMIT)  # Initialize message history for the user
    await update.message.reply_text(START_TEXT)

# Function to handle the help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Received /help command from {update.effective_user.first_name}")
    await update.message.reply_text(HELP_TEXT)

# Function to handle the info command
async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Received /info command from {update.effective_user.first_name}")
    await update.message.reply_text(INFO_TEXT)

# Function to handle text messages
async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text
    logger.info(f"Received message: {user_message} from {update.effective_user.first_name}")

    # Append the new message to the user's history
    if user_id not in user_histories:
        user_histories[user_id] = deque(maxlen=MESSAGE_HISTORY_LIMIT)
    user_histories[user_id].append({"role": "user", "content": user_message})

    # Get the response from GPT-4
    response = await get_gpt_response(user_id)
    logger.info(f"Sending response: {response}")
    await update.message.reply_text(response)

# Function to get response from GPT-4
async def get_gpt_response(user_id):
    try:
        history = list(user_histories[user_id])
        response = await client.chat.completions.create(
            model=GPTCHAT_MODEL,
            messages=[
                {"role": "system", "content": BOT_INSTRUCTIONS},
                *history
            ]
        )
        # Append the assistant's response to the history
        user_histories[user_id].append({"role": "assistant", "content": response.choices[0].message.content.strip()})
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error while getting response from GPT-4: {e}")
        return f"Oops! Something went wrong: {e}"

# Main function to set up the bot
async def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("info", info_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))

    await application.initialize()
    logger.info("Bot initialized and starting...")

    # Start polling and use idle to keep the bot running
    await application.start()
    logger.info("Bot is now polling for updates...")
    await application.updater.start_polling()
    await application.updater.idle()

# For environments with an already running event loop
def run_bot():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    loop.create_task(main())
    logger.info('Bot running in an existing event loop')

    if not loop.is_running():
        loop.run_forever()

if __name__ == '__main__':
    run_bot()
