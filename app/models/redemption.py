"""Student Award redemption requests."""

from datetime import datetime

from sqlmodel import Field, SQLModel


class Redemption(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="user.id", nullable=False)
    award_id: int = Field(foreign_key="award.id", nullable=False)
    status: str = Field(default="pending", nullable=False)
    requested_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    processed_by: int | None = Field(default=None, foreign_key="user.id", nullable=True)
    processed_at: datetime | None = Field(default=None, nullable=True)
