from sqlalchemy import BigInteger, JSON
from sqlalchemy.orm import Mapped, mapped_column
from database.models.base import Base


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, index=True)
    readiness_score: Mapped[int] = mapped_column()
    preferences: Mapped[dict] = mapped_column(JSON)
