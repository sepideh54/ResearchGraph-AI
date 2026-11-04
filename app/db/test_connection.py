
from sqlalchemy import text

from app.db.session import engine


def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Database connection successful:", result.scalar())

    except Exception as error:
        print("Database connection failed:", error)
        raise


if __name__ == "__main__":
    test_connection()
