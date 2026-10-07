"""Administrator review handlers for volunteer submissions."""

from fastapi import Form, Request
from fastapi.responses import RedirectResponse

from app.dependencies.auth import AdminDep
from app.dependencies.session import SessionDep
from app.repositories.volunteer_submission import VolunteerSubmissionRepository
from app.services.volunteer_submission_service import VolunteerSubmissionService
from app.repositories.award import AwardRepository
from app.services.award_service import AwardService
from app.utilities.flash import flash
from . import router, templates


@router.get("/admin/approvals", name="admin_approvals_view")
async def admin_approvals_view(request: Request, user: AdminDep, db: SessionDep):
    service = VolunteerSubmissionService(VolunteerSubmissionRepository(db))
    award_service = AwardService(AwardRepository(db))
    return templates.TemplateResponse(
        request=request,
        name="admin-approvals.html",
        context={
            "user": user,
            "pending_submissions": service.list_pending_with_students(),
            "redemptions": award_service.list_actionable_redemptions(),
        },
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


@router.post("/admin/redemptions/{redemption_id}/process", name="process_redemption")
async def process_redemption(
    request: Request,
    redemption_id: int,
    user: AdminDep,
    db: SessionDep,
    decision: str = Form(...),
):
    service = AwardService(AwardRepository(db))
    try:
        message = service.process_redemption(
            redemption_id=redemption_id,
            administrator_id=user.id,
            decision=decision,
        )
        flash(request, message, "success")
    except ValueError as exc:
        flash(request, str(exc), "danger")
    return RedirectResponse(url=request.url_for("admin_approvals_view"), status_code=303)
