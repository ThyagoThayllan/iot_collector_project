from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from iot_collector.models.mixins import Base


DATABASE_URL = 'sqlite:///db/db.db'


class Database:
    def __init__(self) -> None:
        self.engine = create_engine(
            DATABASE_URL, connect_args={'check_same_thread': False}, echo=False
        )

        self._init_db()

        self.SessionLocal = sessionmaker(bind=self.engine)

    def _init_db(self) -> None:
        Base.metadata.create_all(self.engine)

    def get_session(self) -> Session:
        return self.SessionLocal()
