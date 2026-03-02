import os
from sqlalchemy import create_engine, Integer, String, Boolean, select  # func, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

# --- DATABASE SETUP ---
DATABASE_URL = f"sqlite:///{os.getenv('DATABASE_PATH')}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


# --- MODEL DEFINITION ---
class Wordle(Base):
    __tablename__ = "wordles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer)
    username: Mapped[str] = mapped_column(String)
    timestamp: Mapped[str] = mapped_column(String)
    wordle_id: Mapped[int] = mapped_column(Integer)
    hard_mode: Mapped[bool] = mapped_column(Boolean)
    solved: Mapped[bool] = mapped_column(Boolean)
    guesses_needed: Mapped[int] = mapped_column(Integer)
    guesses: Mapped[str] = mapped_column(String)


def init_db():
    """Create tables if they don't exist."""
    Base.metadata.create_all(engine)


# --- CRUD OPERATIONS ---

def save_wordle(**kwargs) -> None:
    """Save a result to the wordles table."""
    with SessionLocal() as session:
        new_wordle = Wordle(**kwargs)
        session.add(new_wordle)
        session.commit()


def extract_stats(user_id: int, include_unsolved: bool) -> dict:
    """Extract stats for a user."""
    with SessionLocal() as session:
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


def check_user_exists(user_id: int) -> bool:
    """Check if a specific user already has an entry in the database."""
    with SessionLocal() as session:
        stmt = select(Wordle.id).where(Wordle.user_id == user_id).limit(1)
        result = session.execute(stmt).first()
    return result is not None
