import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from wordler.models import (  # Import all models here that should be included in the db.
    Base,
)

##########################
# --- DATABASE SETUP --- #
##########################
DATABASE_URL = f"sqlite:///{os.getenv('DATABASE_PATH')}"
engine = create_engine(DATABASE_URL)


def init_db():
    Base.metadata.create_all(engine)


# Create a session factory
SessionLocal = sessionmaker(bind=engine)  # SessionLocal is a factory for creating sessions
