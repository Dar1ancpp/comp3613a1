"""Redeemable awards for the Redeem Awards workflow."""

from decimal import Decimal

from sqlmodel import Field, SQLModel


class Award(SQLModel, table=True):
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

    quantity_available: int = Field(
        default=0,
        ge=0,
        nullable=False,
    )

    active: bool = Field(
        default=True,
        nullable=False,
    )