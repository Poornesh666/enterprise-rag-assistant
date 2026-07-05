"""
Initialize the SQLite database.
"""

from app.core.database import Base, engine

# Import all models
from app.models.users import User


def init_db():
    """
    Create all database tables.
    """
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully.")


if __name__ == "__main__":
    init_db()