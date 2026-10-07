"""Read-only summaries for role-specific landing dashboards."""

from app.repositories.award import AwardRepository
from app.repositories.progress import ProgressRepository
from app.repositories.volunteer_submission import VolunteerSubmissionRepository
from app.services.progress_service import ProgressService


class DashboardService:
    def __init__(
        self,
        progress_repository: ProgressRepository,
        volunteer_repository: VolunteerSubmissionRepository,
        award_repository: AwardRepository,
    ):
        self.progress_repository = progress_repository
        self.volunteer_repository = volunteer_repository
        self.award_repository = award_repository

    def student_summary(self, student_id: int) -> dict:
        progress = ProgressService(self.progress_repository).get_student_progress(student_id)
        next_milestone = next(
            (milestone for milestone in progress["milestones"] if not milestone["completed"]),
            None,
        )
        return {
            "verified_hours": progress["verified_hours"],
            "rank": progress["rank"],
            "next_milestone": next_milestone,
            "pending_submissions": self.volunteer_repository.count_pending_for_student(student_id),
            "pending_redemptions": self.award_repository.count_pending_redemptions_for_student(student_id),
        }

    def administrator_summary(self, low_stock_threshold: int = 3) -> dict:
        low_stock_awards = self.award_repository.list_low_stock_awards(low_stock_threshold)
        return {
            "pending_submissions": self.volunteer_repository.count_pending(),
            "pending_redemptions": self.award_repository.count_pending_redemptions(),
            "active_awards": self.award_repository.count_active_awards(),
            "low_stock_awards": low_stock_awards,
            "low_stock_threshold": low_stock_threshold,
        }
