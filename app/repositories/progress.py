"""Read models for student progress, milestones, and leaderboard data."""

from decimal import Decimal

from sqlalchemy import and_, func
from sqlmodel import Session, select

from app.models.milestone import Milestone
from app.models.user import User
from app.models.volunteer_submission import VolunteerSubmission


class ProgressRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_milestones(self) -> list[Milestone]:
        statement = select(Milestone).order_by(Milestone.required_hours.asc())
        return list(self.db.exec(statement).all())

    def leaderboard_totals(self) -> list[tuple[int, str, Decimal]]:
        approved_join = and_(
            VolunteerSubmission.student_id == User.id,
            VolunteerSubmission.status == "approved",
        )
        total = func.coalesce(func.sum(VolunteerSubmission.hours), 0)
        statement = (
            select(User.id, User.username, total.label("verified_hours"))
            .outerjoin(VolunteerSubmission, approved_join)
            .where(User.role != "admin")
            .group_by(User.id, User.username)
            .order_by(total.desc(), User.username.asc())
        )
        return [
            (int(user_id), username, Decimal(str(hours)))
            for user_id, username, hours in self.db.exec(statement).all()
        ]
