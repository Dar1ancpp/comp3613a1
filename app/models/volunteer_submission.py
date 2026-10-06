"""Volunteer-hours submission table for the Submit Volunteer Hours workflow."""

from datetime import date, datetime
from decimal import Decimal

from sqlmodel import Field, SQLModel


class VolunteerSubmission(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    student_id: int = Field(
        foreign_key="user.id",
        nullable=False,
    )

    activity_name: str = Field(
        nullable=False,
    )

    organization: str = Field(
        nullable=False,
    )

    activity_date: date = Field(
        nullable=False,
    )

    hours: Decimal = Field(
        gt=0,
        nullable=False,
    )

    supporting_information: str = Field(
        nullable=False,
    )

    status: str = Field(
        default="pending",
        nullable=False,
    )

    submitted_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
    )

    reviewed_by: int | None = Field(
        default=None,
        foreign_key="user.id",
        nullable=True,
    )

    reviewed_at: datetime | None = Field(
        default=None,
        nullable=True,
    )