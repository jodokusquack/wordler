import os
import logging
import sqlite3
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


# --- DATABASE SETUP ---
def init_db():
    with sqlite3.connect("wordle_stats.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
    CREATE TABLE IF NOT EXISTS wordles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    username TEXT,
                    timestamp TEXT,
                    wordle_id INTEGER,
                    hard_mode BOOLEAN,
                    solved BOOLEAN,
                    guesses_needed INTEGER,
                    guesses TEXT
                    )
                    ''')
        conn.commit()


def save_wordle(
        user_id: int,
        username: str,
        timestamp: str,
        wordle_id: int,
        hard_mode: bool,
        solved: bool,
        guesses_needed: int,
        guesses: str) -> None:
    """Save a result to the wordles table."""
    with sqlite3.connect('wordle_stats.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO wordles (user_id, username, timestamp, wordle_id, hard_mode, solved, guesses_needed, guesses) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (user_id, username, timestamp, wordle_id, hard_mode, solved, guesses_needed, guesses)
        )
        conn.commit()


def extract_stats(user_id: int, include_unsolved: bool) -> dict:
    """Extract some stats for a user."""
    with sqlite3.connect('wordles_stats.db') as conn:
        cursor = conn.cursor()

        # define query with ? to prevent sql injection
        if include_unsolved:
            query = "SELECT guesses_needed FROM wordles WHERE user_id = ?"
        else:
            query = "SELECT guesses_needed FROM wordles WHERE user_id = ? AND solved = 1"
        cursor.execute(query, (user_id,))
        results = cursor.fetchall()

        guess_list = [row[0] for row in results]

    stats = {
        'guess_list': guess_list,
        'no_of_guesses': len(guess_list),
        'total_number_of_guesses': sum(guess_list),
        'average_score': sum(guess_list) / len(guess_list)
    }

    return stats


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

    # Message Handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_wordle))

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
