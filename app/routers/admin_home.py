from fastapi import Request
from fastapi.responses import HTMLResponse
from app.dependencies.session import SessionDep
from app.dependencies.auth import AdminDep
from app.repositories.award import AwardRepository
from app.repositories.progress import ProgressRepository
from app.repositories.volunteer_submission import VolunteerSubmissionRepository
from app.services.dashboard_service import DashboardService
from . import router, templates


@router.get("/admin", response_class=HTMLResponse)
async def admin_home_view(
    request: Request,
    user: AdminDep,
    db:SessionDep
):
    service = DashboardService(
        ProgressRepository(db),
        VolunteerSubmissionRepository(db),
        AwardRepository(db),
    )
    return templates.TemplateResponse(
        request=request, 
        name="admin.html",
        context={
            "user": user,
            "summary": service.administrator_summary(low_stock_threshold=3),
        }
    )
