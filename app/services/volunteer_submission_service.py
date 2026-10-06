"""Application rules for volunteer-hour submissions."""

from datetime import date, datetime
from decimal import Decimal

from app.models.volunteer_submission import VolunteerSubmission
from app.repositories.volunteer_submission import VolunteerSubmissionRepository


class VolunteerSubmissionService:
    def __init__(self, repository: VolunteerSubmissionRepository):
        self.repository = repository

    def submit(
        self,
        *,
        student_id: int,
        activity_name: str,
        organization: str,
        hours: Decimal,
        activity_date: date,
        supporting_information: str,
    ) -> VolunteerSubmission:
        activity_name = activity_name.strip()
        organization = organization.strip()
        supporting_information = supporting_information.strip()
        if not activity_name or not organization:
            raise ValueError("Activity name and organization are required.")
        if hours <= 0:
            raise ValueError("Hours must be greater than zero.")

        return self.repository.create(
            VolunteerSubmission(
                student_id=student_id,
                activity_name=activity_name,
                organization=organization,
                activity_date=activity_date,
                hours=hours,
                supporting_information=supporting_information,
            )
        )

    def list_for_student(self, student_id: int) -> list[VolunteerSubmission]:
        return self.repository.list_for_student(student_id)

    def list_pending_with_students(self):
        return self.repository.list_pending_with_students()

    def review(
        self,
        *,
        submission_id: int,
        reviewer_id: int,
        decision: str,
    ) -> VolunteerSubmission:
        decision = decision.strip().lower()
        if decision not in {"approved", "rejected"}:
            raise ValueError("Review decision must be approved or rejected.")

        submission = self.repository.get_by_id(submission_id)
        if submission is None:
            raise ValueError("Volunteer submission was not found.")
        if submission.status != "pending":
            raise ValueError("Only pending submissions can be reviewed.")

        submission.status = decision
        submission.reviewed_by = reviewer_id
        submission.reviewed_at = datetime.utcnow()
        return self.repository.save(submission)

    def verified_hours(self, student_id: int) -> Decimal:
        """Only approved submissions contribute to verified hours."""
        return self.repository.approved_hours_total(student_id)
