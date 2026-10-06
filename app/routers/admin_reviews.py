"""Administrator review handlers for volunteer submissions."""

from fastapi import Form, Request
from fastapi.responses import RedirectResponse

from app.dependencies.auth import AdminDep
from app.dependencies.session import SessionDep
from app.repositories.volunteer_submission import VolunteerSubmissionRepository
from app.services.volunteer_submission_service import VolunteerSubmissionService
from app.utilities.flash import flash
from . import router, templates


@router.get("/admin/approvals", name="admin_approvals_view")
async def admin_approvals_view(request: Request, user: AdminDep, db: SessionDep):
    service = VolunteerSubmissionService(VolunteerSubmissionRepository(db))
    return templates.TemplateResponse(
        request=request,
        name="admin-approvals.html",
        context={"user": user, "pending_submissions": service.list_pending_with_students()},
    )


@router.post("/admin/submissions/{submission_id}/review", name="review_volunteer_submission")
async def review_volunteer_submission(
    request: Request,
    submission_id: int,
    user: AdminDep,
    db: SessionDep,
    decision: str = Form(...),
):
    service = VolunteerSubmissionService(VolunteerSubmissionRepository(db))
    try:
        service.review(
            submission_id=submission_id,
            reviewer_id=user.id,
            decision=decision,
        )
        flash(request, f"Submission {decision}.", "success")
    except ValueError as exc:
        flash(request, str(exc), "danger")
    return RedirectResponse(url=request.url_for("admin_approvals_view"), status_code=303)
