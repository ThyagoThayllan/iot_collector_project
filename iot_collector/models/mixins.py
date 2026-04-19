from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


class ReadingBase(Base):
    __abstract__ = True

    collected_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    device_id: Mapped[int] = mapped_column(ForeignKey('device.id'), nullable=False)
