from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from wordler.models import SubscribedChat, User, Wordle


#########
# Users #
#########
def create_user(session: Session, username: str, telegram_user_id: int):
    """
    Create a new user in the database.

    Args:
        session: SQLAlchemy database session.
        username: Username of the user.
        telegram_user_id: Telegram user ID.

    Returns:
        User: The newly created user object.

    Raises:
        ValueError: If a user with the same telegram_user_id already exists.
    """
    try:
        user = User(username=username, telegram_user_id=telegram_user_id)
        session.add(user)
        session.commit()
        session.refresh(
            user
        )  # refreshes the object to ensure all attributes are up-to-date
        return user
    except IntegrityError:
        session.rollback()
        raise ValueError(
            f"A User with the telegram_user_id {telegram_user_id} already exists."
        )


def get_user_by_telegram_id(session: Session, telegram_user_id: int):
    return session.query(User).filter(User.telegram_user_id == telegram_user_id).first()


def delete_user(session: Session, telegram_user_id: int):
    user = get_user_by_telegram_id(session=session, telegram_user_id=telegram_user_id)
    if user:
        session.delete(user)
        session.commit()
        return True
    return False


####################
# Subscribed Chats #
####################
def subscribe_chat(session: Session, telegram_chat_id: int) -> SubscribedChat:
    """
    Create a SubscribedChat in the database.

    Args:
        session: SQLAlchemy database session.
        telegram_chat_id: Telegram chat ID.

    Returns:
        SubscribedChat: The newly created chat object.

    Raises:
        ValueError: If a chat with the same telegram_chat_id already exists.
    """
    try:
        chat = SubscribedChat(telegram_chat_id=telegram_chat_id)
        session.add(chat)
        session.commit()
        session.refresh(chat)
        return chat
    except IntegrityError:
        session.rollback()
        raise ValueError(
            f"A Chat with the telegram_chat_id {telegram_chat_id} already exists."
        )


def get_subscribed_chat(session: Session, telegram_chat_id: int) -> int:
    stmt = (
        select(SubscribedChat)
        .where(SubscribedChat.telegram_chat_id == telegram_chat_id)
        .limit(1)
    )
    chat = session.scalar(stmt)
    return chat


def unsubscribe_chat(session: Session, telegram_chat_id: int) -> str:
    """Delete a chat from the subscribed chats table."""
    chat = get_subscribed_chat(session=session, telegram_chat_id=telegram_chat_id)
    if chat:
        session.delete(chat)
        session.commit()
        return True
    return False


def get_all_subscribed_chats(session: Session) -> list[int]:
    """Get a list of all the subscribed chats."""
    stmt = select(SubscribedChat)
    return session.scalars(stmt).all()


###########
# Wordles #
###########
def create_wordle(
    session: Session,
    timestamp: Optional[datetime],
    wordle_id: int,
    hard_mode: bool,
    solved: bool,
    guesses_needed: int,
    guesses: str,
    user_id: int,
) -> Wordle:
    """
    Save a Wordle in the database.

    Args:
        session: SQLAlchemy database session.
        timestamp: Optional datetime when the wordle was posted.
        wordle_id: Id of the Wordle.
        hard_mode: Boolean if the Wordle was tried in hard mode or not.
        solved: Boolean if the Wordle was succesfully solved or not.
        guesses_needed: How many guessses were needed, 7 indicates unsuccesful solve.
        guesses: The emoji string containing the green, yellow and grey positions for each guess.

    Returns:
        Wordle: The newly created Wordle.

    Raises:
        ValueError: If a Wordle with the same wordle_id and user_id already exists.
    """
    try:
        wordle = Wordle(
            timestamp=timestamp,
            wordle_id=wordle_id,
            hard_mode=hard_mode,
            solved=solved,
            guesses_needed=guesses_needed,
            guesses=guesses,
            user_id=user_id,
        )
        session.add(wordle)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise ValueError(
            f"The user with ID {user_id} already has a Wordle with ID {wordle_id}. Only one Wordle per user per day is allowed."
        )


#########
# Other #
#########
def extract_stats(session: Session, user_id: int, include_unsolved: bool) -> dict:
    """Extract stats for a user."""
    with session:
        stmt = select(Wordle.guesses_needed).where(Wordle.user_id == user_id)

        if not include_unsolved:
            # stmt = stmt.where(Wordle.solved == True)
            stmt = stmt.where(Wordle.solved)

        results = session.execute(stmt).scalars().all()

    if not results:
        return {
            "guess_list": [],
            "no_of_guesses": 0,
            "total_number_of_guesses": 0,
            "average_score": 0,
        }

    return {
        "guess_list": list(results),
        "no_of_guesses": len(results),
        "total_number_of_guesses": sum(results),
        "average_score": sum(results) / len(results),
    }
