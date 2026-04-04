from sqlalchemy import Integer, Boolean
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)


class Base(DeclarativeBase):
    pass


# --- MODEL DEFINITION ---
class Wordle(Base):
    __tablename__ = "wordles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int]
    username: Mapped[str]
    timestamp: Mapped[str]
    wordle_id: Mapped[int]
    hard_mode: Mapped[bool]
    solved: Mapped[bool]
    guesses_needed: Mapped[int]
    guesses: Mapped[str]


class SubscribedChat(Base):
    __tablename__ = 'subscribed_chats'
    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(Integer, unique=True)
    subscribed: Mapped[bool] = mapped_column(Boolean, default=True)  # default = True actually uses 'True' as the default value for this row
