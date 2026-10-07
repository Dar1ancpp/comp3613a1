"""Persistence operations for Awards and redemption requests."""

from decimal import Decimal

from sqlalchemy import func
from sqlmodel import Session, select

from app.models.award import Award
from app.models.redemption import Redemption
from app.models.user import User
from app.models.volunteer_submission import VolunteerSubmission


class AwardRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_active(self) -> list[Award]:
        statement = select(Award).where(Award.active == True).order_by(Award.required_hours.asc())  # noqa: E712
        return list(self.db.exec(statement).all())

    def list_all(self) -> list[Award]:
        statement = select(Award).order_by(Award.name.asc())
        return list(self.db.exec(statement).all())

    def get_award(self, award_id: int) -> Award | None:
        return self.db.get(Award, award_id)

    def get_by_name(self, name: str) -> Award | None:
        statement = select(Award).where(Award.name == name)
        return self.db.exec(statement).first()

    def save_award(self, award: Award) -> Award:
        self.db.add(award)
        self.db.commit()
        self.db.refresh(award)
        return award

    def verified_hours(self, student_id: int) -> Decimal:
        statement = select(func.coalesce(func.sum(VolunteerSubmission.hours), 0)).where(
            VolunteerSubmission.student_id == student_id,
            VolunteerSubmission.status == "approved",
        )
        return Decimal(str(self.db.exec(statement).one()))

    def has_pending(self, student_id: int, award_id: int) -> bool:
        statement = select(Redemption.id).where(
            Redemption.student_id == student_id,
            Redemption.award_id == award_id,
            Redemption.status == "pending",
        )
        return self.db.exec(statement).first() is not None

    def create_redemption(self, redemption: Redemption) -> Redemption:
        self.db.add(redemption)
        self.db.commit()
        self.db.refresh(redemption)
        return redemption

    def list_student_redemptions(self, student_id: int):
        statement = (
            select(Redemption, Award)
            .join(Award, Award.id == Redemption.award_id)
            .where(Redemption.student_id == student_id)
            .order_by(Redemption.requested_at.desc())
        )
        return list(self.db.exec(statement).all())

    def list_actionable_redemptions(self):
        statement = (
            select(Redemption, User, Award)
            .join(User, User.id == Redemption.student_id)
            .join(Award, Award.id == Redemption.award_id)
            .where(Redemption.status.in_(["pending", "approved"]))
            .order_by(Redemption.requested_at.asc())
        )
        return list(self.db.exec(statement).all())

    def get_redemption(self, redemption_id: int) -> Redemption | None:
        return self.db.get(Redemption, redemption_id)

    def save_processing(self, redemption: Redemption, award: Award | None = None) -> Redemption:
        if award is not None:
            self.db.add(award)
        self.db.add(redemption)
        self.db.commit()
        self.db.refresh(redemption)
        return redemption

    def count_pending_redemptions_for_student(self, student_id: int) -> int:
        statement = select(func.count(Redemption.id)).where(
            Redemption.student_id == student_id,
            Redemption.status == "pending",
        )
        return int(self.db.exec(statement).one())

    def count_pending_redemptions(self) -> int:
        statement = select(func.count(Redemption.id)).where(Redemption.status == "pending")
        return int(self.db.exec(statement).one())

    def count_active_awards(self) -> int:
        statement = select(func.count(Award.id)).where(Award.active == True)  # noqa: E712
        return int(self.db.exec(statement).one())

    def list_low_stock_awards(self, threshold: int = 3) -> list[Award]:
        statement = (
            select(Award)
            .where(Award.active == True, Award.quantity_available <= threshold)  # noqa: E712
            .order_by(Award.quantity_available.asc(), Award.name.asc())
        )
        return list(self.db.exec(statement).all())
