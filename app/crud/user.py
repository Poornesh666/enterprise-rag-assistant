from sqlalchemy.orm import Session

from app.models.users import User
from app.core.security import hash_password

def create_user(
    db: Session,
    username: str,
    password: str,
    role: str,
):

    user = User(
        username=username,
        password=hash_password(password),
        role=role,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def get_user_by_username(
    db: Session,
    username: str,
):
    """
    Retrieve a user by username.
    """

    return (
        db.query(User)
        .filter(User.username == username)
        .first()
    )
    