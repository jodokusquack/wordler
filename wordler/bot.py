import datetime
import logging
import os
from zoneinfo import ZoneInfo

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from wordler.db.crud import get_all_subscribed_chats
from wordler.db.database import SessionLocal, init_db
from wordler.handlers.command_handlers import start, stats, subscribe, unsubscribe
from wordler.handlers.message_handlers import reply_wordle

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


async def send_scheduled_messages(
    context: ContextTypes.DEFAULT_TYPE, session=None
) -> None:
    message = "Good Morning! This is a test message sent at 9:30."

    if session is None:
        session = SessionLocal()

    chat_ids = get_all_subscribed_chats(session)
    for chat_id in chat_ids:
        print(chat_id)
        await context.bot.send_message(chat_id=chat_id, text=message)


#################
# Env variables #
#################
api_key = os.getenv("WORDLER_API_KEY")


def main() -> None:
    """Start the Bot."""
    init_db()

    app = Application.builder().token(api_key).build()
    job_queue = app.job_queue

    # Command Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("subscribe", subscribe))
    app.add_handler(CommandHandler("unsubscribe", unsubscribe))

    # Message Handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_wordle))

    # schedule regular messages
    vienna_time = datetime.time(hour=9, minute=30, tzinfo=ZoneInfo("Europe/Vienna"))
    job_queue.run_daily(send_scheduled_messages, time=vienna_time)

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
