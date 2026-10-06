"""Milestone thresholds for the Track Progress and Milestones workflow."""

from decimal import Decimal

from sqlmodel import Field, SQLModel


class Milestone(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    name: str = Field(
        nullable=False,
        unique=True,
    )

    description: str | None = Field(
        default=None,
        nullable=True,
    )

    required_hours: Decimal = Field(
        gt=0,
        nullable=False,
    )