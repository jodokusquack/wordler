from telegram import Update
from telegram.ext import ContextTypes

from wordler.db.crud import (
    extract_stats,
    get_user_by_telegram_id,
    subscribe_chat,
    unsubscribe_chat,
)
from wordler.db.database import SessionLocal


# COMMAND: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! Are you ready to play Wordle?",
        do_quote=False,
    )


# COMMAND: /stats
async def stats(
    update: Update, context: ContextTypes.DEFAULT_TYPE, session=None
) -> None:
    """Send a stats message to the user asking for it."""
    user = update.effective_user
    # determine if unsolved wordles should be included in the stats
    include_unsolved = False
    if context.args:
        if context.args[0].lower().startswith("y"):
            include_unsolved = True

    # check if the user is already in the database
    if session is None:
        session = SessionLocal()
    user_exists = get_user_by_telegram_id(session, user.id)

    if user_exists:
        stats = extract_stats(user.id, include_unsolved)

        # craft message with stats:
        await update.message.reply_html(
            rf"""Of course {user.mention_html()}! Here are the stats 📝 I have collected about you:

            Total number of Wordles: {stats['no_of_guesses']} 🆒
            Best score: {min(stats["guess_list"])} 🎯
            Average score: {stats['average_score']:.3f}
            """
        )
    else:
        await update.message.reply_html(
            "Sorry there are no Wordles on record for you."
            "You have to post some results before checking your stats."
        )


# COMMAND: /subscribe
async def subscribe(
    update: Update, context: ContextTypes.DEFAULT_TYPE, session=None
) -> None:
    chat_id = update.message.chat_id

    if session is None:
        session = SessionLocal()
    res = subscribe_chat(session, chat_id)
    if res == "already_subscribed":
        message = (
            "It seems like this chat is already subscribed! No need to do it again."
        )
    elif res == "success":
        message = "Successfully subscribed. ✅"

    await update.message.reply_text(message)


# COMMAND: /unsubscribe
async def unsubscribe(
    update: Update, context: ContextTypes.DEFAULT_TYPE, session=None
) -> None:
    chat_id = update.message.chat_id

    if session is None:
        session = SessionLocal()

    res = unsubscribe_chat(session, chat_id)
    if res == "not_subscribed":
        message = "You weren't subscribed at all. Use /subscribe to add this chat to the subscription list."
    else:
        message = "Succesfully unsubscribed. Sad to see you leave 😔"

    await update.message.reply_text(message)
