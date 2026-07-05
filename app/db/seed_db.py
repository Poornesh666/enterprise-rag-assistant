"""
Seed the database with initial users.
"""

from app.core.database import SessionLocal
from app.models.users import User
from app.core.security import hash_password


def seed_users():
    db = SessionLocal()

    existing_user = db.query(User).first()

    if existing_user:
         print("Database is already seeded.")
         db.close()
         return

    users = [
        User(
            username="Tony",
            password=hash_password("password123"),
            role="engineering",
        ),
        User(
            username="Bruce",
            password=hash_password("securepass"),
            role="marketing",
        ),
        User(
            username="Sam",
            password=hash_password("financepass"),
            role="finance",
        ),
        User(
            username="Peter",
            password=hash_password("pete123"),
            role="engineering",
        ),
        User(
            username="Sid",
            password=hash_password("sidpass123"),
            role="marketing",
        ),
        User(
            username="Natasha",
            password=hash_password("hrpass123"),
            role="hr",
        ),
        User(
            username="Alice",
            password=hash_password("ceopass"),
            role="c-levelexecutives",
        ),
        User(
            username="Bob",
            password=hash_password("employeepass"),
            role="employee",
        ),
    ]

    db.add_all(users)
    db.commit()
    db.close()

    print("Users inserted successfully.")


if __name__ == "__main__":
    seed_users()