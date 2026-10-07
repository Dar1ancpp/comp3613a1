"""Persistence operations for volunteer-hour submissions."""

from decimal import Decimal

from sqlalchemy import func
from sqlmodel import Session, select

from app.models.volunteer_submission import VolunteerSubmission
from app.models.user import User


class VolunteerSubmissionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, submission: VolunteerSubmission) -> VolunteerSubmission:
        self.db.add(submission)
        self.db.commit()
        self.db.refresh(submission)
        return submission

    def list_for_student(self, student_id: int) -> list[VolunteerSubmission]:
        statement = (
            select(VolunteerSubmission)
            .where(VolunteerSubmission.student_id == student_id)
            .order_by(VolunteerSubmission.submitted_at.desc())
        )
        return list(self.db.exec(statement).all())

    def list_pending_with_students(self) -> list[tuple[VolunteerSubmission, User]]:
        statement = (
            select(VolunteerSubmission, User)
            .join(User, User.id == VolunteerSubmission.student_id)
            .where(VolunteerSubmission.status == "pending")
            .order_by(VolunteerSubmission.submitted_at.asc())
        )
        return list(self.db.exec(statement).all())

    def get_by_id(self, submission_id: int) -> VolunteerSubmission | None:
        return self.db.get(VolunteerSubmission, submission_id)

    def save(self, submission: VolunteerSubmission) -> VolunteerSubmission:
        self.db.add(submission)
        self.db.commit()
        self.db.refresh(submission)
        return submission

    def approved_hours_total(self, student_id: int) -> Decimal:
        statement = select(
            func.coalesce(func.sum(VolunteerSubmission.hours), 0)
        ).where(
            VolunteerSubmission.student_id == student_id,
            VolunteerSubmission.status == "approved",
        )
        return Decimal(str(self.db.exec(statement).one()))

    def count_pending_for_student(self, student_id: int) -> int:
        statement = select(func.count(VolunteerSubmission.id)).where(
            VolunteerSubmission.student_id == student_id,
            VolunteerSubmission.status == "pending",
        )
        return int(self.db.exec(statement).one())

    def count_pending(self) -> int:
        statement = select(func.count(VolunteerSubmission.id)).where(
            VolunteerSubmission.status == "pending"
        )
        return int(self.db.exec(statement).one())
