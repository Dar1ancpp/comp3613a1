from fastapi import Request
from fastapi.responses import HTMLResponse
from app.dependencies.session import SessionDep
from app.dependencies.auth import AuthDep
from app.repositories.award import AwardRepository
from app.repositories.progress import ProgressRepository
from app.repositories.volunteer_submission import VolunteerSubmissionRepository
from app.services.dashboard_service import DashboardService
from . import router, templates


@router.get("/app", response_class=HTMLResponse)
async def user_home_view(
    request: Request,
    user: AuthDep,
    db:SessionDep
):
    service = DashboardService(
        ProgressRepository(db),
        VolunteerSubmissionRepository(db),
        AwardRepository(db),
    )
    return templates.TemplateResponse(
        request=request, 
        name="app.html",
        context={
            "user": user,
            "summary": service.student_summary(user.id),
        }
    )
