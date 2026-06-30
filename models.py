from sqlalchemy import Integer, String, Text, DateTime
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