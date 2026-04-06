from telegram import Update
from telegram.ext import ContextTypes

from wordler.db.crud import create_wordle
from wordler.db.database import SessionLocal
from wordler.utilities.text_handling import parse_wordle_share_text


# --- MESSAGE HANDLER ---
async def reply_wordle(
    update: Update, context: ContextTypes.DEFAULT_TYPE, session=None
) -> None:
    """If the message contains the Wordle Share string, extract the stats from it and send them back."""
    # get the text from the received update
    text = update.effective_message.text

    # try to parse the text and extract the stats
    result = parse_wordle_share_text(text)
    if result:
        # save result to database
        user = update.effective_user
        wordle_answer = {
            "timestamp": update.message.date.isoformat(),
            "wordle_id": result["wordle_id"],
            "hard_mode": result["hard_mode"],
            "solved": result["solved"],
            "guesses_needed": result["guesses_needed"],
            "guesses": "\n".join(result["guesses"]),
            "user_id": user.id,
        }

        # save the wordle to the database
        if session is None:
            session = SessionLocal()
        create_wordle(session, **wordle_answer)

        # create the answer text
        # answer = stats_reply_message(result)

        # send the message
        # await update.message.reply_text(answer)
