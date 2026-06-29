from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy.orm import Session

from app.database.connection import SessionLocal


class DatabaseService:
    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

