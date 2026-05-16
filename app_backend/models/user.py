import uuid
from datetime import datetime
from sqlalchemy import String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    full_name: Mapped[str] = mapped_column(String(50), nullable=True)
    bio: Mapped[str] = mapped_column(String(200), nullable= True)
    profile_picture: Mapped[str] = mapped_column(String(200), nullable=True)

    posts: Mapped[list["Posts"]] = relationship("Posts", back_populates="author")