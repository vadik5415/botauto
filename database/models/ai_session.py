from sqlalchemy import BigInteger, Integer
from sqlalchemy.orm import Mapped, mapped_column
from database.models.base import Base


class AISession(Base):
    __tablename__ = "ai_sessions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, index=True)
    prompt_tokens: Mapped[int] = mapped_column(Integer, default=0)
    completion_tokens: Mapped[int] = mapped_column(Integer, default=0)
