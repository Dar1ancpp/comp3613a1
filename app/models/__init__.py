"""Database table models.

Import every table model here so ``SQLModel.metadata.create_all`` sees them.
"""

from app.models.user import User
from app.models.volunteer_submission import VolunteerSubmission
from app.models.milestone import Milestone

__all__ = ["User", "VolunteerSubmission", "Milestone"]
