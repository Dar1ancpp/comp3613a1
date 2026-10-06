"""HTTP handlers for Track Progress and Milestones."""

from fastapi import Request

from app.dependencies.auth import AuthDep
from app.dependencies.session import SessionDep
from app.repositories.progress import ProgressRepository
from app.services.progress_service import ProgressService
from . import router, templates


@router.get("/app/progress", name="progress_view")
async def progress_view(
    request: Request,
    user: AuthDep,
    db: SessionDep,
):
    repository = ProgressRepository(db)
    service = ProgressService(repository)

    progress = service.get_student_progress(user.id)

    return templates.TemplateResponse(
        request=request,
        name="progress.html",
        context={
            "user": user,
            "progress": progress,
        },
    )