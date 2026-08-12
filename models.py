from sqlalchemy import Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from datetime import datetime

class Document(Base):
    __tablename__ = "documents"
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    raw_text : Mapped[str] = mapped_column(Text, nullable=False)
    title : Mapped[str] = mapped_column(String(50), nullable = False)
    created_at : Mapped[datetime] = mapped_column(DateTime, default = datetime.now, nullable = False)
    source_type : Mapped[str] = mapped_column(String(10), nullable = False)
    user_id : Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable = False)


class User(Base):
    __tablename__ = "users"
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    username : Mapped[str] = mapped_column(String(50), nullable = False, unique = True)
    email : Mapped[str] = mapped_column(String(50), nullable = False, unique = True)
    hashed_password : Mapped[str] = mapped_column(String(5000), nullable = False)
    created_at : Mapped[datetime] = mapped_column(DateTime, default = datetime.now, nullable = False)