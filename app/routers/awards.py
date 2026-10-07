"""HTTP handlers for the Redeem Awards workflow."""

from fastapi import Request
from fastapi.responses import RedirectResponse

from app.dependencies.auth import AuthDep
from app.dependencies.session import SessionDep
from app.repositories.award import AwardRepository
from app.services.award_service import AwardService
from app.utilities.flash import flash
from . import router, templates


@router.get("/app/awards", name="awards_view")
async def awards_view(request: Request, user: AuthDep, db: SessionDep):
    service = AwardService(AwardRepository(db))
    return templates.TemplateResponse(
        request=request,
        name="awards.html",
        context={"user": user, "catalogue": service.get_student_awards(user.id)},
    )


@router.post("/app/awards/{award_id}/redeem", name="redeem_award")
async def redeem_award(
    request: Request,
    award_id: int,
    user: AuthDep,
    db: SessionDep,
):
    repository = AwardRepository(db)
    service = AwardService(repository)

    try:
        service.request_redemption(student_id=user.id, award_id=award_id)
        flash(request, "Award redemption requested.", "success")
    except ValueError as exc:
        flash(request, str(exc), "danger")

    return RedirectResponse(
        url=request.url_for("awards_view"),
        status_code=303,
    )
