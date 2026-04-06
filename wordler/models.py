from datetime import datetime
from typing import List

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


# --- MODEL DEFINITION ---
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str]
    telegram_user_id: Mapped[int] = mapped_column(
        Integer, unique=True, index=True, nullable=False
    )

    # Relationship to Wordle: 'cascade' ensures Wordles are deleted with the User
    wordles: Mapped[List["Wordle"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class SubscribedChat(Base):
    __tablename__ = "subscribed_chats"
    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_chat_id: Mapped[int] = mapped_column(
        Integer, unique=True, index=True, nullable=False
    )
    subscribed: Mapped[bool] = mapped_column(
        Boolean, default=True
    )  # default = True actually uses 'True' as the default value for this row


class Wordle(Base):
    __tablename__ = "wordles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    wordle_id: Mapped[int]
    hard_mode: Mapped[bool]
    solved: Mapped[bool]
    guesses_needed: Mapped[int]
    guesses: Mapped[str]

    # Foreign Key linking to the User table
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    # Back-reference to the User object
    user: Mapped["User"] = relationship(back_populates="wordles")

    # enforce uniqueness of wordle_id and user_id together at the DB level
    __table_args__ = (UniqueConstraint("wordle_id", "user_id", name="uq_user_wordle"),)
