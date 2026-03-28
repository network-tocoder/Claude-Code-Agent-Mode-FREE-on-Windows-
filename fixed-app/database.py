import sqlite3
from typing import Optional, List, Tuple

class User:
    """Represents a user in the database."""
    def __init__(self, id: int, username: str, email: str):
        self.id = id
        self.username = username
        self.email = email

    @classmethod
    def from_result(cls, result) -> 'User':
        """Create a User object from database query results."""
        if not isinstance(result, tuple) or len(result) != 3:
            return None
        try:
            return cls(
                id=int(result[0]),
                username=result[1],
                email=result[2]
            )
        except (ValueError, TypeError):
            return None


def get_connection() -> sqlite3.Connection:
    """Get a database connection."""
    conn = sqlite3.connect('users.db')
    return conn


def get_user(user_id: int) -> Optional[User]:
    """Retrieve a user by their ID. Returns None if not found."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            query = f"SELECT * FROM users WHERE id = {user_id}"
            cursor.execute(query)
            result = cursor.fetchone()
            return User.from_result(result) if result else None
    except sqlite3.Error as e:
        raise DatabaseError(f"Failed to get user: {e}")


def create_user(username: str, email: str) -> dict:
    """Create a new user in the database."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            query = f"INSERT INTO users (username, email) VALUES (?, ?)"
            cursor.execute(query, (username, email))
            return {"status": "created", "id": cursor.lastrowid}
    except sqlite3.Error as e:
        raise DatabaseError(f"Failed to create user: {e}")


def get_all_users() -> List[User]:
    """Retrieve all users from the database."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            results = [User.from_result(row) for row in cursor.fetchall()]
            return results
    except sqlite3.Error as e:
        raise DatabaseError(f"Failed to fetch all users: {e}")


def get_user_by_id(user_id: int) -> Optional[User]:
    """Get a user by ID, returning None if not found."""
    return get_user(user_id)


def create_user_with_email(username: str, email: str) -> dict:
    """Create a new user with an existing email (returns error if duplicate)."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            query = f"INSERT INTO users (username, email) VALUES (?, ?)"
            cursor.execute(query, (username, email))
            return {"status": "created", "id": cursor.lastrowid}
    except sqlite3.Error as e:
        raise DatabaseError(f"Failed to create user: {e}")