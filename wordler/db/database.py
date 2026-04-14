import os
from functools import wraps

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from wordler.db.models import (
    Base,
)  # Import all models here that should be included in the db.

##########################
# --- DATABASE SETUP --- #
##########################
DATABASE_URL = f"sqlite:///{os.getenv('DATABASE_PATH')}"
engine = create_engine(DATABASE_URL)


def init_db():
    Base.metadata.create_all(engine)


# Create a session factory
SessionLocal = sessionmaker(
    bind=engine
)  # SessionLocal is a factory for creating sessions


# Decorator wrapper for dependecy injection of the session to message handlers
def provide_session(handler_func):
    @wraps(handler_func)
    async def wrapper(update, context, *args, **kwargs):
        session = SessionLocal()
        try:
            # We pass session as a keyword argument
            result = await handler_func(
                update, context, session=session, *args, **kwargs
            )
            session.commit()  # Commit here, now it is the duty of the caller to commit the changes
            return result
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    return wrapper
