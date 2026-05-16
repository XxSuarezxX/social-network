import uuid
from datetime import datetime
from sqlalchemy import String, Uuid, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

class Posts(Base):
    __tablename__ = "posts"

    id: Mapped[uuid.UUID]= mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id : Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    content : Mapped[String] = mapped_column(String(500), nullable=True)
    created_at : Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    author: Mapped["User"] = relationship("User", back_populates="posts")
