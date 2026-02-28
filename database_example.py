import sqlite3
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("JS_TUT_BOT_API_KEY")


# ---- DATABASE SETUP ----
def init_db():
    conn = sqlite3.connect("bot_history.db")
    cursor = conn.cursor()
    cursor.execute('''
          CREATE TABLE IF NOT EXISTS messages (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_id INTEGER,
                   username TEXT,
                   content TEXT,
                   timestamp TEXT
                   )
                   ''')
    conn.commit()
    conn.close()


def save_message(user_id, username, content, timestamp):
    conn = sqlite3.connect("bot_history.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (user_id, username, content, timestamp) VALUES (?, ?, ?, ?)",
        (user_id, username, content, timestamp)
    )
    conn.commit()
    conn.close()


# --- BOT HANDLERS  ---
async def track_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # 1. Extract data from the update
    user = update.effective_user
    display_name = user.username or user.first_name
    text = update.message.text
    # current_chat_id = update.effective_chat.id
    message_time = update.message.date
    timestamp_str = message_time.isoformat()

    # 2. Save to SQLite
    save_message(user.id, display_name, text, timestamp_str)

    # 3. Optional: Confirm to the user
    print(f"Saved message from {display_name}: {text}")
    await update.message.reply_text(f"✅ Message received and saved, {user.first_name}!", do_quote=False)


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id

    with sqlite3.connect("bot_history.db") as conn:
        cursor = conn.cursor()

        # Count messages for specific user
        cursor.execute("SELECT COUNT(*) FROM messages WHERE user_id = ?", (user_id,))
        total = cursor.fetchone()[0]

    await update.message.reply_text(f"📊 You have recorded {total} messages in my database.")


# --- MAIN ENGINE ---
def main():
    init_db()  # Ensure the table exists before starting

    app = Application.builder().token(api_key).build()

    app.add_handler(CommandHandler('stats', stats))
    # use a MessageHandler to catch all text that isn't a command
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, track_message))

    app.run_polling()


if __name__ == '__main__':
    main()
