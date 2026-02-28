import os
import logging
from dotenv import load_dotenv

from telegram import Update, ForceReply
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

from wordler.text_handling import parse_wordle_share_text, stats_reply_message


# Env variables
load_dotenv()
api_key = os.getenv("WORDLER_BOT_API_KEY")
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


# --- COMMAND HANDLERS ---
# command /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! Are you ready to play Wordle?",
        reply_markup=ForceReply(selective=True),
    )


# --- MESSAGE HANDLER ---
async def reply_wordle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """If the message contains the Wordle Share string, extract the stats from it and send them back."""
    text = update.effective_message.text
    parse_result = parse_wordle_share_text(text)
    if parse_result:
        answer = stats_reply_message(parse_result)
        await update.message.reply_text(answer)


def main() -> None:
    """Start the Bot."""
    app = Application.builder().token(api_key).build()

    # Command Handlers
    app.add_handler(CommandHandler("start", start))

    # Message Handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_wordle))

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
