import os
import logging

from telegram import Update, ForceReply
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

from text_handling import parse_wordle_share_text, stats_reply_message
from database_connection import init_db, save_wordle, extract_stats, check_user_exists


# Env variables
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
        rf"Hi {user.mention_html()}! Are you ready to play Wordle?",
        reply_markup=ForceReply(selective=True),
    )


# command /stats
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a stats message to the user asking for it."""
    user = update.effective_user
    # determine if unsolved wordles should be included in the stats
    include_unsolved = False
    if context.args:
        if context.args[0].lower().startswith('y'):
            include_unsolved = True

    # check if the user is already in the database
    user_exists = check_user_exists(user.id)
    
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
            "Sorry there are no Wordles on record for you." \
            "You have to post some results before checking your stats."
        )


# --- MESSAGE HANDLER ---
async def reply_wordle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """If the message contains the Wordle Share string, extract the stats from it and send them back."""
    # get the text from the received update
    text = update.effective_message.text

    # try to parse the text and extract the stats
    result = parse_wordle_share_text(text)
    if result:
        # save result to database
        user = update.effective_user
        user_id = user.id
        username = user.username or user.first_name
        timestamp = update.message.date.isoformat()
        wordle_id = result['wordle_id']
        hard_mode = result['hard_mode']
        solved = result['solved']
        guesses_needed = result['guesses_needed']
        guesses = '\n'.join(result['guesses'])

        save_wordle(user_id, username, timestamp, wordle_id, hard_mode, solved, guesses_needed, guesses)

        answer = stats_reply_message(result)
        await update.message.reply_text(answer)


def main() -> None:
    """Start the Bot."""
    init_db()

    app = Application.builder().token(api_key).build()

    # Command Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))

    # Message Handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_wordle))

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
