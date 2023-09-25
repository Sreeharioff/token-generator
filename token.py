import time
import pyshorteners
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Define your token timeout duration in seconds (e.g., 1 hour)
TOKEN_TIMEOUT_SECONDS = 3600

# Create a dictionary to store user tokens and their creation times
user_tokens = {}

# Initialize the Bitly URL shortener with your API access token
GREY_API_TOKEN = "3f52cf5744a74654e91274e16f6bb338fb3e9174"
s = pyshorteners.Shortener(api_key=GREY_API_TOKEN)

# Function to generate a new token (shortened URL) for a user
def generate_token(user_id):
    original_url = f"https://greymatterslinks.in/api?api={GREY_API_TOKEN}&url=6655395078:AAEx-YZ7NofmuTzWxqpg3YphlxVazgZDgzY"
    token = s.greymatterslinks.short(original_url)
    user_tokens[user_id] = {
        "token": token,
        "created_at": time.time()
    }
    return token

# Function to check if a token is valid and not expired
def is_valid_token(user_id):
    if user_id in user_tokens:
        token_info = user_tokens[user_id]
        created_at = token_info["created_at"]
        current_time = time.time()
        return current_time - created_at < TOKEN_TIMEOUT_SECONDS
    return False

# Command to request a new token
def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    # Check if the user already has a valid token
    if is_valid_token(user_id):
        update.message.reply_text("You already have a valid token.")
    else:
        # Generate a new token and send it to the user
        token = generate_token(user_id)
        update.message.reply_text(f"Your new token (shortened URL): {token}")

def main():
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    updater = Updater(token="6655395078:AAEx-YZ7NofmuTzWxqpg3YphlxVazgZDgzY", use_context=True)
    dispatcher = updater.dispatcher

    # Define a command handler for the /start command
    dispatcher.add_handler(CommandHandler("start", start))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
