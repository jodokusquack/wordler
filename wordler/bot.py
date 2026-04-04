import os
import logging
import datetime
from zoneinfo import ZoneInfo

from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

from wordler.text_handling import parse_wordle_share_text, stats_reply_message
from wordler.database import init_db, SessionLocal
from wordler.crud import save_wordle, subscribe_chat, unsubscribe_chat, get_subscribed_chats, extract_stats, check_user_exists

#################
# Env variables #
#################
api_key = os.getenv("WORDLER_API_KEY")
# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


# --- COMMAND HANDLERS ---
# command /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! Are you ready to play Wordle?"
    )


# command /stats
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE, session=None) -> None:
    """Send a stats message to the user asking for it."""
    user = update.effective_user
    # determine if unsolved wordles should be included in the stats
    include_unsolved = False
    if context.args:
        if context.args[0].lower().startswith('y'):
            include_unsolved = True

    # check if the user is already in the database
    if session is None:
        session = SessionLocal()
    user_exists = check_user_exists(session, user.id)

    if user_exists:
        stats = extract_stats(user.id, include_unsolved)

        # craft message with stats:
        await update.message.reply_html(
            rf"""Of course {user.mention_html()}! Here are the stats 📝 I have collected about you:

            Total number of Wordles: {stats['no_of_guesses']} 🆒
            Best score: {min(stats["guess_list"])} 🎯
            Average score: {stats['average_score']:.3f}
            """)
    else:
        await update.message.reply_html(
            "Sorry there are no Wordles on record for you."
            "You have to post some results before checking your stats."
        )


# command /subscribe
async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE, session=None) -> None:
    chat_id = update.message.chat_id

    if session is None:
        session = SessionLocal()
    res = subscribe_chat(session, chat_id)
    if res == "already_subscribed":
        message = "It seems like this chat is already subscribed! No need to do it again."
    elif res == "success":
        message = "Successfully subscribed. ✅"

    await update.message.reply_text(message)


# command /unsubscribe
async def unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE, session=None) -> None:
    chat_id = update.message.chat_id

    if session is None:
        session = SessionLocal()

    res = unsubscribe_chat(session, chat_id)
    if res == "not_subscribed":
        message = "You weren't subscribed at all. Use /subscribe to add this chat to the subscription list."
    else:
        message = "Succesfully unsubscribed. Sad to see you leave 😔"

    await update.message.reply_text(message)


# --- MESSAGE HANDLER ---
async def reply_wordle(update: Update, context: ContextTypes.DEFAULT_TYPE, session=None) -> None:
    """If the message contains the Wordle Share string, extract the stats from it and send them back."""
    # get the text from the received update
    text = update.effective_message.text

    # try to parse the text and extract the stats
    result = parse_wordle_share_text(text)
    if result:
        # save result to database
        user = update.effective_user
        wordle_answer = {
            'user_id': user.id,
            'username': user.username or user.first_name,
            'timestamp': update.message.date.isoformat(),
            'wordle_id': result['wordle_id'],
            'hard_mode': result['hard_mode'],
            'solved': result['solved'],
            'guesses_needed': result['guesses_needed'],
            'guesses': '\n'.join(result['guesses'])
        }

        # save the wordle to the database
        if session is None:
            session = SessionLocal()
        save_wordle(session, **wordle_answer)

        # create the answer text
        answer = stats_reply_message(result)

        # send the message
        # await update.message.reply_text(answer)


async def send_scheduled_messages(context: ContextTypes.DEFAULT_TYPE, session=None) -> None:
    message = "Good Morning! This is a test message sent at 9:30."

    if session is None:
        session = SessionLocal()

    chat_ids = get_subscribed_chats(session)
    for chat_id in chat_ids:
        print(chat_id)
        await context.bot.send_message(chat_id=chat_id, text=message)


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
    job_queue.run_daily(
        send_scheduled_messages,
        time=vienna_time
        )

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
