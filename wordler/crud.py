from wordler.models import Wordle, SubscribedChat, User
from sqlalchemy.orm import Session
from sqlalchemy import select


def save_wordle(session: Session, **kwargs) -> None:
    """Save a result to the wordles table."""
    with session:
        new_wordle = Wordle(**kwargs)
        session.add(new_wordle)
        session.commit()


def subscribe_chat(session: Session, chat_id: int) -> str:
    """Save a chat to the subscribed chats table."""
    with session:
        # check if already subsribed
        if session.query(SubscribedChat).filter_by(chat_id=chat_id).first():
            return 'already_subscribed'
        else:
            # add to database
            session.add(SubscribedChat(chat_id=chat_id))
            session.commit()
            return "success"


def unsubscribe_chat(session: Session, chat_id: int) -> str:
    """Delete a chat from the subscribed chats table."""
    with session:
        # check if chat is subsribed at all.
        if session.query(SubscribedChat).filter_by(chat_id=chat_id).first():
            session.query(SubscribedChat).filter_by(chat_id=chat_id).delete()
            session.commit()
            return "success"
        else:
            return "not_subscribed"


def get_subscribed_chats(session: Session) -> list[int]:
    """Get a list of all the subscribed chats."""
    with session:
        return [chat_id[0] for chat_id in session.query(SubscribedChat.chat_id).distinct()]


def extract_stats(session: Session, user_id: int, include_unsolved: bool) -> dict:
    """Extract stats for a user."""
    with session:
        stmt = select(Wordle.guesses_needed).where(Wordle.user_id == user_id)

        if not include_unsolved:
            # stmt = stmt.where(Wordle.solved == True)
            stmt = stmt.where(Wordle.solved)

        results = session.execute(stmt).scalars().all()

    if not results:
        return {'guess_list': [], 'no_of_guesses': 0, 'total_number_of_guesses': 0, 'average_score': 0}

    return {
        'guess_list': list(results),
        'no_of_guesses': len(results),
        'total_number_of_guesses': sum(results),
        'average_score': sum(results) / len(results)
    }


def check_user_exists(session: Session, user_id: int) -> bool:
    """Check if a specific user already has an entry in the database."""
    with session:
        stmt = select(Wordle.id).where(Wordle.user_id == user_id).limit(1)
        result = session.execute(stmt).first()
    return result is not None


# User functions
def create_user(session: Session, username: str, telegram_user_id: int):
    user = User(username=username, telegram_user_id=telegram_user_id)
    session.add(user)
    session.commit()
    session.refresh(user)  # refreshes the object to ensure all attributes are up-to-date
    return user


def get_user_by_telegram_id(session: Session, telegram_user_id: int):
    return session.query(User).filter(User.telegram_user_id == telegram_user_id).first()


def delete_user(session: Session, telegram_user_id: int):
    user = get_user_by_telegram_id(session=session, telegram_user_id=telegram_user_id)
    if user:
        session.delete(user)
        session.commit()
        return True
    return False
