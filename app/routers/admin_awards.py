"""Administrator Award catalogue management."""

from decimal import Decimal

from fastapi import Form, Request
from fastapi.responses import RedirectResponse

from app.dependencies.auth import AdminDep
from app.dependencies.session import SessionDep
from app.repositories.award import AwardRepository
from app.services.award_service import AwardService
from app.utilities.flash import flash
from . import router, templates


@router.get("/admin/awards", name="admin_awards_view")
async def admin_awards_view(request: Request, user: AdminDep, db: SessionDep):
    service = AwardService(AwardRepository(db))
    return templates.TemplateResponse(
        request=request,
        name="admin-awards.html",
        context={"user": user, "awards": service.list_all_awards()},
    )


@router.post("/admin/awards", name="create_award")
async def create_award(
    request: Request,
    user: AdminDep,
    db: SessionDep,
    name: str = Form(...),
    description: str = Form(""),
    required_hours: Decimal = Form(...),
    quantity_available: int = Form(...),
    active: str | None = Form(None),
):
    service = AwardService(AwardRepository(db))
    try:
        service.create_award(
            name=name,
            description=description,
            required_hours=required_hours,
            quantity_available=quantity_available,
            active=active is not None,
        )
        flash(request, "Award created.", "success")
    except ValueError as exc:
        flash(request, str(exc), "danger")
    return RedirectResponse(url=request.url_for("admin_awards_view"), status_code=303)


@router.post("/admin/awards/{award_id}", name="update_award")
async def update_award(
    request: Request,
    award_id: int,
    user: AdminDep,
    db: SessionDep,
    name: str = Form(...),
    description: str = Form(""),
    required_hours: Decimal = Form(...),
    quantity_available: int = Form(...),
    active: str | None = Form(None),
):
    service = AwardService(AwardRepository(db))
    try:
        service.update_award(
            award_id=award_id,
            name=name,
            description=description,
            required_hours=required_hours,
            quantity_available=quantity_available,
            active=active is not None,
        )
        flash(request, "Award updated.", "success")
    except ValueError as exc:
        flash(request, str(exc), "danger")
    return RedirectResponse(url=request.url_for("admin_awards_view"), status_code=303)
