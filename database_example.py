import sqlite3
from datetime import datetime
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

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


def save_message(user_id, username, content):
    conn = sqlite3.connect("bot_history.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (user_id, username, content, timestamp) VALUES (?, ?, ?, ?)",
        (user_id, username, content, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


# --- BOT HANDLERS  ---
async def track_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # 1. Extract data from the update
    user = update.effective_user
    text = update.message.text
    current_chat_id = update.effective_chat.id

    # 2. Save to SQLite
    save_message(user.id, user.username, text)

    # 3. Optional: Confirm to the user
    print(f"Saved message from {user.username}: {text}")
    await update.message.reply_text(f"✅ Message received and saved, {user.first_name}!", do_quote=False)
    await context.bot.send_message(
        chat_id=current_chat_id,
        text="I've recorded this message in my logs."
    )


# --- MAIN ENGINE ---
def main():
    init_db()  # Ensure the table exists before starting

    app = Application.builder().token(api_key).build()

    # use a MessageHandler to catch all text that isn't a command
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, track_message))

    app.run_polling()


if __name__ == '__main__':
    main()
