# COMP 3613 Assignment 1

Draft this file with the Guide. **Update it after every phase milestone** before you pause. The use-case diagram is a UML PNG at `docs/diagrams/use-case.png`, linked from this file as `diagrams/use-case.png` (path relative to `docs/report.md`). The model diagram is Mermaid. **Embed wireframe images** as `wireframes/<file>` (files live in `docs/wireframes/`).

Do not put your student ID in this file if you will commit it. The PDF cover adds your name and ID at export time.

## Assigned project

Student Awards (incentive system)

## Three workflows

### 1. Submit Volunteer Hours (Student)

### 2. Track Progress and Milestones (Student)

### 3. Redeem Awards (Student)

## Use case diagram

![Use case diagram](diagrams/use-case.png)

Student (left) starts the three primary workflows as separate associations. Administrator (right) supports them with Review Submitted Hours, Manage Awards, and Process Redemption Requests — each a separate Administrator association, no «include» / «extend» to Submit or Redeem. Seeing which awards exist stays inside Redeem Awards. Deliberate gap: Manage milestone definitions is out of this MVP (Track Progress uses whatever milestones already exist).

## Model diagram

First draft. Update this section in Phase 5 when polish revises the model, and note what changed.

```mermaid
erDiagram
  USER ||--o{ VOLUNTEER_SUBMISSION : "submits as student"
  USER o|--o{ VOLUNTEER_SUBMISSION : "reviews as administrator"
  USER ||--o{ REDEMPTION : "requests as student"
  USER o|--o{ REDEMPTION : "processes as administrator"
  AWARD ||--o{ REDEMPTION : "is requested in"

  USER {
    int id PK
    string name
    string email UK
    string password_hash
    string role
  }

  VOLUNTEER_SUBMISSION {
    int id PK
    int student_id FK
    string activity_name
    string organization
    date activity_date
    decimal hours
    string supporting_information
    string status
    datetime submitted_at
    int reviewed_by FK
    datetime reviewed_at
  }

  MILESTONE {
    int id PK
    string name UK
    string description
    decimal required_hours
  }

  AWARD {
    int id PK
    string name UK
    string description
    decimal required_hours
    int quantity_available
    boolean active
  }

  REDEMPTION {
    int id PK
    int student_id FK
    int award_id FK
    string status
    datetime requested_at
    int processed_by FK
    datetime processed_at
  }
```

### Model rules and decisions

- `User.role` is either `student` or `administrator`. Name, unique email, and password hash are required.
- A student owns many volunteer submissions. An administrator may review many submissions; `reviewed_by` and `reviewed_at` remain null while a submission is pending.
- Volunteer submission status is `pending`, `approved`, or `rejected` and defaults to `pending`. Activity name and date are required, and hours must be greater than zero. Only an administrator may approve or reject a submission; doing so records the reviewer and review time.
- Only approved volunteer hours contribute to the student's verified total. Milestone unlocks and award eligibility are calculated from that total against their respective `required_hours`; neither `Milestone` nor `Award` needs a direct relationship to submissions.
- Milestone and award names are unique, their required-hour thresholds are positive, and descriptions are optional. Award inventory is nonnegative and `active` defaults to true.
- A redemption belongs to one student and one award. It starts as `pending` and may become `approved`, `rejected`, or `fulfilled`; only an administrator may approve or reject a pending request. Processing records the administrator and time.
- A student may request only an active award for which they have enough approved hours. Repeat redemption is allowed, but the same student cannot have more than one pending request for the same award.
- Creating a redemption does not reserve stock. Approval atomically reduces inventory by one and is forbidden when inventory is zero; an out-of-stock pending request is rejected when reviewed. Rejection does not change inventory, and an approved redemption may later be marked fulfilled when the prize is issued.

## Wireframes

### Submit Volunteer Hours

![Log Volunteer Hours](wireframes/log-volunteer-hours.png)

<!-- student-build:wireframe-coverage
use_case: Submit Volunteer Hours
image: docs/wireframes/log-volunteer-hours.png
covered: yes
-->

After submission, the page shows a success message and a **My Submissions** table below the form. The table shows activity, organization, activity date, hours, and the current `Pending`, `Approved`, or `Rejected` status. A new submission appears immediately as pending, and its status updates after administrator review.

### Track Progress and Milestones

![Progress and Milestones](wireframes/progress-and-milestones.png)

<!-- student-build:wireframe-coverage
use_case: Track Progress and Milestones
image: docs/wireframes/progress-and-milestones.png
covered: yes
-->

Verified hours and leaderboard position are derived from approved volunteer submissions. Milestone completion is derived by comparing verified hours with each milestone threshold; no additional stored progress entity is required.

### Redeem Awards

![Redeem Rewards](wireframes/redeem-rewards.png)

<!-- student-build:wireframe-coverage
use_case: Redeem Awards
image: docs/wireframes/redeem-rewards.png
covered: yes
-->

Clicking **Redeem** shows a success confirmation and adds the request to a **My Redemptions** table on the same page. The table shows prize, requested date, and `Pending`, `Approved`, `Rejected`, or `Fulfilled` status. New requests start pending and reflect later administrator processing.

### Review Submitted Hours and Process Redemption Requests

![Administrator Approvals](wireframes/admin-approvals.png)

<!-- student-build:wireframe-coverage
use_case: Review Submitted Hours
image: docs/wireframes/admin-approvals.png
covered: yes
-->

<!-- student-build:wireframe-coverage
use_case: Process Redemption Requests
image: docs/wireframes/admin-approvals.png
covered: yes
-->

For a pending volunteer submission, **Review** / **View Details** exposes student, activity, organization, activity date, hours, and supporting information before approval or rejection. The main table remains concise.

Pending redemptions show **Approve** and **Reject**. Approved redemptions remain visible and show **Mark as Fulfilled**; that action saves the fulfilled state and updates the student's history. Rejected and fulfilled rows have no further processing actions.

### Manage Awards

![Add Prize](wireframes/add-prize.png)

<!-- student-build:wireframe-coverage
use_case: Manage Awards
image: docs/wireframes/add-prize.png
covered: yes
-->

The Manage Awards page also includes a table of existing prizes with prize name, required hours, quantity, active status, and an edit action. Administrators can add a prize, edit its name, description, required hours, and quantity, adjust stock, and activate or deactivate it. Deletion is outside the MVP. The shown Add Prize form opens from this page.

### Phase 4 review

- Every use case in the use-case diagram is covered by a readable wireframe image; the shared administrator approvals image covers both review workflows.
- The initially unclear submission and redemption completion paths are resolved through student-visible history tables and status feedback.
- Administrator decisions now expose enough submission detail for informed review, and approved redemptions have a defined path to fulfillment.
- Manage Awards is broader than the pictured add form; its accepted table, edit, stock, and activation states should be implemented alongside that form in Phase 5. This is an incomplete-but-fixable screen detail, not a required redraw.
- The wireframes use **Prize/Reward** while the model uses `AWARD`. Treat these as UI labels for the same entity and choose one consistent product term during theming.
- No Phase 4 model revision is required: the accepted refinements use existing `status`, timestamp, `active`, and quantity fields. Leaderboard rank, verified hours, milestone progress, and eligibility remain derived values.

## Theming

- **Colors:** deep navy primary, teal secondary, off-white/light-gray background, green success, amber warning/pending, and red error/rejected states.
- **Type:** Inter with a system sans-serif fallback.
- **Tone:** professional, modern, simple, student-friendly, and minimal rather than overly corporate.
- **Wordmark:** text-only **Student Awards**; no custom MVP logo.
- **Applied:** shared CSS brand/status tokens, public landing page, login, registration, and authenticated application shell. FastStarter placeholder branding and demo copy were removed; authentication and `/config` were retained.
- **Theming verification:** registration, sign-in, and redirection worked correctly. After polish, the student confirmed that the landing page plus Student and Administrator authenticated views shared consistent branding, role-aware navigation was correct, authentication still worked, and no starter-template issues remained.
- **Polish after verification:** reduced the landing hero and decorative teal circle, removed the duplicate registration CTA, standardized visible terminology on **Award**, replaced the starter sidebar/menu treatment with a clean role-aware application header, and removed workflow placeholder copy.

## Implementation notes

One named workflow at a time. Include verify notes and polish / model revisions (Phase 5). Do not treat the first build as final.

### Submit Volunteer Hours — verified

- Implementation choice: one page with the submission form above the student's submission-history table.

<!-- student-build:code-check
workflow: Submit Volunteer Hours
form: choice
layer: other
architecture_ok: yes
implement_confidence: 0.85
passed: yes
note: Student selected a combined form-and-history page.
-->

<!-- student-build:code-check
workflow: Submit Volunteer Hours
form: snippet
layer: model
architecture_ok: yes
implement_confidence: 0.88
passed: yes
note: Student completed VolunteerSubmission fields, constraints, foreign keys, defaults, and nullable review metadata from the ERD.
-->

<!-- student-build:code-check
workflow: Submit Volunteer Hours
form: snippet
layer: router
architecture_ok: yes
implement_confidence: 0.91
passed: yes
note: Student completed a thin POST handler that binds form data and calls VolunteerSubmissionService with no persistence logic in the route.
-->

- **Verification:** the student confirmed the form matched the intended layout; required fields, success feedback, immediate history insertion, pending status, displayed activity data, and branding all worked correctly.
- **Polish:** volunteer-hour values were changed to hide insignificant trailing zeroes (`4.0000000000` → `4`, while preserving values such as `4.5`). Stored decimal precision was not changed.
- **Administrator review:** pending submissions are listed in the Administrator Approvals view. Expandable details expose student, activity, organization, activity date, hours, and supporting information before Approve or Reject. Review decisions update `status`, `reviewed_by`, and `reviewed_at`; the repository's verified-hours aggregate includes only `approved` submissions.
- **End-to-end verification:** two pending submissions appeared in Administrator Approvals with complete expandable details. The student approved one and rejected the other, then confirmed that both statuses updated correctly in the Student history and that whole/fractional hours rendered cleanly as `4` and `4.5`.

### Track Progress and Milestones — verified

- Implementation choice: leaderboard ties use dense ranking; equal verified-hour totals share a rank and the next distinct total receives the next consecutive rank.

<!-- student-build:code-check
workflow: Track Progress and Milestones
form: choice
layer: other
architecture_ok: yes
implement_confidence: 0.92
passed: yes
note: Student selected dense ranking for tied approved-hour totals.
-->

<!-- student-build:code-check
workflow: Track Progress and Milestones
form: snippet
layer: model
architecture_ok: yes
implement_confidence: 0.93
passed: yes
note: Student completed the Milestone model with a unique required name, optional description, and positive decimal threshold.
-->

<!-- student-build:code-check
workflow: Track Progress and Milestones
form: snippet
layer: router
architecture_ok: yes
implement_confidence: 0.95
passed: yes
note: Student completed a thin GET handler that calls ProgressService and renders its result without queries or ranking logic.
-->

- **Verification:** verified hours showed `4` from the approved submission only; the rejected `4.5` hours contributed nothing. Bronze, Silver, and Gold appeared in threshold order with correct `4 / 10`, `4 / 25`, and `4 / 50` progress. The current student appeared at rank `#1`, hours were cleanly formatted, and the page matched the approved branding. No further UI or workflow polish was requested.

### Redeem Awards — verified

- Implementation choice: selecting an eligible Award opens a confirmation modal before the pending redemption request is submitted.

<!-- student-build:code-check
workflow: Redeem Awards
form: choice
layer: other
architecture_ok: yes
implement_confidence: 0.95
passed: yes
note: Student selected a confirmation modal before redemption submission.
-->

<!-- student-build:code-check
workflow: Redeem Awards
form: snippet
layer: model
architecture_ok: yes
implement_confidence: 0.96
passed: yes
note: Student completed Award with its unique name, optional description, positive threshold, nonnegative inventory, and active default.
-->

<!-- student-build:code-check
workflow: Redeem Awards
form: snippet
layer: router
architecture_ok: yes
implement_confidence: 0.97
passed: yes
note: Student completed a thin POST handler that delegates redemption creation to AwardService and redirects without persistence or eligibility logic.
-->

- **Verification:** Awards showed correct thresholds and quantities; the Coffee Voucher was eligible at `4` verified hours while higher thresholds stayed locked. The confirmation modal created a pending request and duplicate pending requests were prevented. Administrator approval reduced quantity from `10` to `9`; requests could be rejected or marked fulfilled, and Student history reflected both statuses. Repeat requests became available after a request left pending status. Branding consistently used **Award**.

### Manage Awards — verified

- Implementation choice: Administrators edit existing Awards in a prefilled modal on the management page.
- The management screen lists Award name, description, required hours, quantity, and active state; it supports creating Awards, editing details, adjusting stock, and activating or deactivating an Award. Deletion remains outside the MVP.
- **Verification:** existing inventory displayed correctly; Add Award and prefilled Edit Award modals worked; name, description, required hours, and quantity saved correctly. Deactivation removed an Award from the Student catalogue and reactivation restored it. Nonpositive thresholds and negative quantities were rejected, with consistent styling and **Award** terminology.

### Cross-workflow dashboard polish — in progress

- Student dashboard: verified hours, leaderboard rank, next-milestone progress, pending hour submissions, pending redemptions, and quick links to the three named workflows.
- Administrator dashboard: pending hour approvals, pending redemptions, active Award count, active Awards with quantity `3` or fewer, and quick links to Approvals and Awards.
- Dashboards are read-only landing summaries using existing workflow services/routes; they do not duplicate actions or introduce new workflows.

## Deployed app

Phase 6. Public Render URL (not localhost). Markers open this to mark the three workflows.

https://

## Logins

Every account a marker needs, including extra users you added. Starter accounts:

- bob / bobpass — regular user
- admin / adminpass — admin

## YouTube URL

## Session transcripts

Filled when the Guide builds the report: the agent writes each Guide chat to `docs/transcripts/<slug>.md` (Copilot Agent, Cursor, or OpenCode). `python manage.py report` packages them. Do not paste chats here during the build.

## Competency (student-judge)

Filled when the report is built. Guide runs student-judge, writes `docs/judge.md`, and export appends the scorecard here.

## Skill integrity

Filled by `python manage.py report`. Do not edit the course skills.
