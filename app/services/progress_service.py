"""Derived progress and dense-ranking rules."""

from app.repositories.progress import ProgressRepository


class ProgressService:
    def __init__(self, repository: ProgressRepository):
        self.repository = repository

    def get_student_progress(self, student_id: int) -> dict:
        ranked_students = []
        previous_total = None
        dense_rank = 0
        for user_id, username, verified_hours in self.repository.leaderboard_totals():
            if previous_total is None or verified_hours != previous_total:
                dense_rank += 1
                previous_total = verified_hours
            ranked_students.append(
                {
                    "student_id": user_id,
                    "username": username,
                    "verified_hours": verified_hours,
                    "rank": dense_rank,
                    "is_current": user_id == student_id,
                }
            )

        current = next(
            (entry for entry in ranked_students if entry["student_id"] == student_id),
            {"verified_hours": 0, "rank": None},
        )
        verified_hours = current["verified_hours"]
        milestones = []
        for milestone in self.repository.list_milestones():
            completed = verified_hours >= milestone.required_hours
            percentage = min(100, float((verified_hours / milestone.required_hours) * 100))
            milestones.append(
                {
                    "name": milestone.name,
                    "description": milestone.description,
                    "required_hours": milestone.required_hours,
                    "completed": completed,
                    "percentage": round(percentage, 1),
                }
            )

        return {
            "verified_hours": verified_hours,
            "rank": current["rank"],
            "milestones": milestones,
            "leaderboard": ranked_students,
        }
