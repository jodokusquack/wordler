from telegram import Update
from telegram.ext import ContextTypes

from wordler.db.crud import create_user, create_wordle, get_user_by_telegram_id
from wordler.db.database import provide_session
from wordler.utilities.text_handling import parse_wordle_share_text


# --- MESSAGE HANDLER ---
@provide_session
async def reply_wordle(
    update: Update, context: ContextTypes.DEFAULT_TYPE, session
) -> None:
    """If the message contains the Wordle Share string, extract the stats from it and send them back."""
    # get the info from the update
    text = update.effective_message.text
    user_id = update.effective_user.id

    # try to get the user and create a new user if it doesn't exist
    user = get_user_by_telegram_id(session=session, telegram_user_id=user_id)
    if not user:
        telegram_username = (
            update.effective_user.username or update.effective_user.first_name
        )  # sometimes telegram doesn't share a users username so we might need to use the firstname
        user = create_user(
            session=session, username=telegram_username, telegram_user_id=user_id
        )

    # try to parse the text and extract the stats
    result = parse_wordle_share_text(text)
    if result:
        wordle_info = {
            "timestamp": update.message.date,
            "wordle_id": result["wordle_id"],
            "hard_mode": result["hard_mode"],
            "solved": result["solved"],
            "guesses_needed": result["guesses_needed"],
            "guesses": "\n".join(result["guesses"]),
            "user_id": user.id,
        }

        try:
            wordle = create_wordle(session=session, **wordle_info)
            msg = f"Succesfully registered a Worlde result. {wordle.guesses_needed}/6 guesses. Not bad!"
        except ValueError:
            # this means there is already a wordle for the user for the day
            msg = f"It looks like {update.effective_user.mention_html()} already has a Wordle registered for today. Only one Worlde per day allowed."

    else:
        msg = "Cool story bro!"
    await update.message.reply_html(msg, do_quote=False)
