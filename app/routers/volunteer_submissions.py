"""HTTP handlers for the Submit Volunteer Hours workflow."""

from datetime import date
from decimal import Decimal

from fastapi import Form, Request
from fastapi.responses import RedirectResponse

from app.dependencies.auth import AuthDep
from app.dependencies.session import SessionDep
from app.repositories.volunteer_submission import VolunteerSubmissionRepository
from app.services.volunteer_submission_service import VolunteerSubmissionService
from app.utilities.flash import flash
from . import router, templates


@router.get("/app/hours", name="volunteer_hours_view")
async def volunteer_hours_view(request: Request, user: AuthDep, db: SessionDep):
    repository = VolunteerSubmissionRepository(db)
    service = VolunteerSubmissionService(repository)
    return templates.TemplateResponse(
        request=request,
        name="volunteer-hours.html",
        context={"user": user, "submissions": service.list_for_student(user.id)},
    )


@router.post("/app/hours", name="submit_volunteer_hours")
async def submit_volunteer_hours(
    request: Request,
    user: AuthDep,
    db: SessionDep,
    activity_name: str = Form(...),
    organization: str = Form(...),
    hours: Decimal = Form(...),
    activity_date: date = Form(...),
    supporting_information: str = Form(""),
):
    repository = VolunteerSubmissionRepository(db)
    service = VolunteerSubmissionService(repository)

    try:
        service.submit(
            student_id=user.id,
            activity_name=activity_name,
            organization=organization,
            hours=hours,
            activity_date=activity_date,
            supporting_information=supporting_information,
        )
        flash(request, "Volunteer hours submitted for review.", "success")
    except ValueError as exc:
        flash(request, str(exc), "danger")

    return RedirectResponse(
        url=request.url_for("volunteer_hours_view"),
        status_code=303,
    )
