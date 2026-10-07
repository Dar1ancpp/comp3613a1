"""Eligibility and processing rules for Award redemptions."""

from datetime import datetime
from decimal import Decimal

from app.models.award import Award
from app.models.redemption import Redemption
from app.repositories.award import AwardRepository


class AwardService:
    def __init__(self, repository: AwardRepository):
        self.repository = repository

    def get_student_awards(self, student_id: int) -> dict:
        verified_hours = self.repository.verified_hours(student_id)
        awards = []
        for award in self.repository.list_active():
            awards.append(
                {
                    "award": award,
                    "eligible": verified_hours >= award.required_hours,
                    "pending": self.repository.has_pending(student_id, award.id),
                }
            )
        return {
            "verified_hours": verified_hours,
            "awards": awards,
            "redemptions": self.repository.list_student_redemptions(student_id),
        }

    def request_redemption(self, *, student_id: int, award_id: int) -> Redemption:
        award = self.repository.get_award(award_id)
        if award is None or not award.active:
            raise ValueError("This Award is not available.")
        if self.repository.verified_hours(student_id) < award.required_hours:
            raise ValueError("You have not earned enough verified hours for this Award.")
        if self.repository.has_pending(student_id, award_id):
            raise ValueError("You already have a pending request for this Award.")
        return self.repository.create_redemption(Redemption(student_id=student_id, award_id=award_id))

    def list_actionable_redemptions(self):
        return self.repository.list_actionable_redemptions()

    def list_all_awards(self) -> list[Award]:
        return self.repository.list_all()

    def create_award(
        self,
        *,
        name: str,
        description: str,
        required_hours: Decimal,
        quantity_available: int,
        active: bool,
    ) -> Award:
        name = name.strip()
        if not name:
            raise ValueError("Award name is required.")
        if self.repository.get_by_name(name):
            raise ValueError("An Award with that name already exists.")
        self._validate_award_values(required_hours, quantity_available)
        return self.repository.save_award(
            Award(
                name=name,
                description=description.strip() or None,
                required_hours=required_hours,
                quantity_available=quantity_available,
                active=active,
            )
        )

    def update_award(
        self,
        *,
        award_id: int,
        name: str,
        description: str,
        required_hours: Decimal,
        quantity_available: int,
        active: bool,
    ) -> Award:
        award = self.repository.get_award(award_id)
        if award is None:
            raise ValueError("Award was not found.")
        name = name.strip()
        if not name:
            raise ValueError("Award name is required.")
        duplicate = self.repository.get_by_name(name)
        if duplicate and duplicate.id != award_id:
            raise ValueError("An Award with that name already exists.")
        self._validate_award_values(required_hours, quantity_available)
        award.name = name
        award.description = description.strip() or None
        award.required_hours = required_hours
        award.quantity_available = quantity_available
        award.active = active
        return self.repository.save_award(award)

    @staticmethod
    def _validate_award_values(required_hours: Decimal, quantity_available: int) -> None:
        if required_hours <= 0:
            raise ValueError("Required hours must be greater than zero.")
        if quantity_available < 0:
            raise ValueError("Quantity cannot be negative.")

    def process_redemption(self, *, redemption_id: int, administrator_id: int, decision: str) -> str:
        redemption = self.repository.get_redemption(redemption_id)
        if redemption is None:
            raise ValueError("Redemption request was not found.")
        award = self.repository.get_award(redemption.award_id)
        if award is None:
            raise ValueError("The requested Award was not found.")

        decision = decision.strip().lower()
        if redemption.status == "pending" and decision in {"approved", "rejected"}:
            if decision == "approved" and award.quantity_available <= 0:
                redemption.status = "rejected"
                message = "Request rejected because the Award is out of stock."
            else:
                redemption.status = decision
                message = f"Redemption {decision}."
                if decision == "approved":
                    award.quantity_available -= 1
            redemption.processed_by = administrator_id
            redemption.processed_at = datetime.utcnow()
            self.repository.save_processing(redemption, award)
            return message

        if redemption.status == "approved" and decision == "fulfilled":
            redemption.status = "fulfilled"
            redemption.processed_by = administrator_id
            redemption.processed_at = datetime.utcnow()
            self.repository.save_processing(redemption)
            return "Redemption marked as fulfilled."

        raise ValueError("That processing action is not valid for the current status.")
