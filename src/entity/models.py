from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Date
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Contact(Base):
    __tablename__ = 'contacts'
    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str] = mapped_column(String(50))
    lastname: Mapped[str] = mapped_column(String(50), index=True)
    e_mail: Mapped[str] = mapped_column(String(120), index=True, unique=True)
    birthday: Mapped[datetime] = mapped_column(Date())
    add_data: Mapped[Optional[str]] = mapped_column(String(250))