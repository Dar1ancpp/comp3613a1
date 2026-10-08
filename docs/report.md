<!-- student-build:skill-integrity
status: pass
root: e84cd692d0b85eefe546385661958c27d07e8be6c5176a82012f68ccff5c8beb
expected_root: e84cd692d0b85eefe546385661958c27d07e8be6c5176a82012f68ccff5c8beb
mismatches: none
-->

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

### Cross-workflow dashboard polish — verified

- Student dashboard: verified hours, leaderboard rank, next-milestone progress, pending hour submissions, pending redemptions, and quick links to the three named workflows.
- Administrator dashboard: pending hour approvals, pending redemptions, active Award count, active Awards with quantity `3` or fewer, and quick links to Approvals and Awards.
- Dashboards are read-only landing summaries using existing workflow services/routes; they do not duplicate actions or introduce new workflows.
- **Final verification:** testing with both student accounts and the Administrator confirmed all submission and redemption states, approved-only hour totals, milestone and dense-rank updates, Award eligibility, duplicate-pending prevention, inventory decrement on approval, Award management and validation, accurate dashboards, consistent navigation/terminology/status styling/feedback/spacing, and correct empty and populated states.
- **Final model review:** no Phase 5 model revision was required. `Milestone` progress and leaderboard rank remain derived; redemption inventory changes occur on approval; dashboard values are read-only aggregates over the accepted entities.
- **Polish outcome:** no further UI, workflow, or model refinements were requested after the final cross-workflow pass.

## Deployed app

Phase 6. Public Render URL (not localhost). Markers open this to mark the three workflows.

https://faststarter-1ygs.onrender.com

The public health endpoint returns `{"ok":true}`.

## GitHub repository

https://github.com/Dar1ancpp/comp3613a1.git

## Logins

Every account a marker needs, including extra users you added. Starter accounts:

- `bob` / `bobpass` — `regular_user` (student)
- `admin` / `adminpass` — `admin` (administrator)

## YouTube video

https://youtu.be/ViRlo6-w-xI

## Final implementation summary

- Project: Student Awards, an incentive system for verified volunteer hours, milestone progress, and prize redemption.
- Named workflows: Submit Volunteer Hours, Track Progress and Milestones, Redeem Awards, plus administrator review and award management.
- Architecture: FastStarter routes remain thin; application rules live in services; persistence and queries live in repositories; SQLModel tables define the data model.
- Theme: deep navy, teal, off-white, status colors, Inter typography, and a consistent Student Awards wordmark across landing, authentication, and authenticated pages.
- Data lifecycle: volunteer submissions begin as `pending`; only approved submissions contribute to verified hours; milestones and award eligibility are derived from approved totals; redemption requests begin as `pending` and inventory changes occur only on approval.
- Admin workflows: review submissions, process redemptions, create and edit awards, adjust stock, and activate or deactivate awards.
- Verified polish: role-aware navigation, consistent Award terminology, clean hour formatting, confirmation flows, validation feedback, empty/populated states, and dashboard summaries for both student and administrator roles.

## Final deployment summary

- Render web service: `faststarter-1ygs.onrender.com`
- Database: Render Postgres configured for the web service; the database password and internal connection string are not included in the report.
- Health check: `GET /health` returned `{"ok":true}`.
- Deployment command used: `python manage.py init --no-drop && python manage.py run --host 0.0.0.0 --port $PORT`
- Render startup and configuration secrets were not committed; app usernames, passwords, and roles are listed above under Logins.

## Session transcripts

Filled when the Guide builds the report: the agent writes chat markdown into `docs/transcripts/`; `python manage.py report` packages them.

Guide packaged **2** chat(s) in `docs/transcripts/` (and `docs/transcripts.zip`).

Index: [docs/transcripts/INDEX.md](transcripts/INDEX.md)

- [`render-connected`](transcripts/render-connected.md)
- [`render-deploy-verification`](transcripts/render-deploy-verification.md)

## Competency (student-judge)

Filled by Guide from the student-judge run when this report was built.

**Judged at:** 2026-10-08T00:00:00Z
**Evidence pass:** re-read current project artefacts plus available Guide deployment transcripts; prior judge records ignored

# student-judge competency report

**Student / session:** Student (project session evidence available only through current artefacts and two Guide deployment chats)
**Artifact:** current `docs/report.md`, `docs/diagrams/`, `docs/wireframes/`, and guide transcript records in `docs/transcripts/`
**Phases in evidence:** 1–6 (COMP 3613; Phase 5 polish, Phase 6 deploy; never generic 0–5)

### Totals

| | Count / value |
|--|--|
| Metrics on rubric | 12 (M1–M12) |
| N/A (excluded) | 0 |
| Metrics scored | 12 |
| Scoreable max | 48 |
| Awarded total | 40 / 48 |
| **Overall (avg of scored)** | **3.3 / 4** |
| Impression mark | 17 / 20 |

## Scorecard

| ID | Metric | Score / 4 | In avg | Evidence |
|----|--------|----------:|:------:|----------|
| M1 | Phase discipline | 4 | yes | The report records the designed workflow sequence, Phase 5 polish, and staged Phase 6 deployment. The app was deployed only after local workflow verification. |
| M2 | Problem framing | 3 | yes | Three named workflows were defined and the report documents include/extend use-case relationships, shared administrator support, and an explicit MVP gap. The report is evidence of ownership of the project framing. |
| M3 | Decision ownership | 3 | yes | The student selected the workflow and relationship decisions in the report, including the one-page form/history layout, dense ranking, and confirmation modal choices. |
| M4 | Artefact-before-code | 4 | yes | The implementation was aligned with the ERD and wireframes, and later model revisions and workflow refinements were recorded in the report. |
| M5 | Verification habit | 4 | yes | The report records per-workflow verification and a final cross-workflow pass with student-observed outcomes. |
| M6 | Assignment fit | 3 | yes | The app uses the FastStarter layers and the report describes thin routes, services, repositories, and models; no route-level persistence appears in the reported architecture checks. |
| M7 | Slice explanation | 3 | yes | The report includes workflow-level architecture checks, layer choices, and own-words explanations of the model and route boundaries. |
| M8 | Prompt quality | 3 | yes | The Phase 5 workflow checks use concrete feature prompts and verified mismatches. The project report is concise and phase-tagged. |
| M9 | Response to pushback | 3 | yes | The report documents mismatch handling, UI refinement, and final model review after verification. |
| M10 | Integrity | 4 | yes | No evidence of edited skills or a failed skill-integrity check. No external-LLM laundering indicators were found in the current record. |
| M11 | Provenance continuity | 3 | yes | The implementation decisions and refinements match the report’s named workflows, ERD, and wireframes. |
| M12 | Sincerity trajectory | 3 | yes | No suspicion spiral was found in the available records; the available deployment transcript is direct and consistent. |

## Strengths

- The project clearly defines three student workflows and separate administrator support workflows in the report.
- The model, wireframe coverage, and final implementation are consistently aligned around approved hours, milestones, awards, redemptions, and administrator review.
- The report documents per-workflow verification, final cross-workflow checking, and explicit UI/model polish decisions.
- The deployment record includes a live Render URL and a successful `/health` response.
- The skill-integrity check passed, so protected course skills remain unchanged.

## Gaps (priority order)

1. **Earlier native Phase 1–5 build transcripts are not present in the workspace.** The current session stores only two Render deployment turns. The judge uses those transcripts and current project artefacts, but this limits the evidence available for the full implementation conversation.
2. The student identity and student ID are not supplied, so the PDF export cannot be executed with a complete cover identity yet.

## Phase gate status

| Phase | Status | Note |
|-------|--------|------|
| 1 | met | Three named workflows are stated and the project is identified as Student Awards. |
| 2 | met | The use-case diagram is generated and relationships are recorded in the report. |
| 3 | met | The ERD and model rules document the required entities, fields, and lifecycle decisions. |
| 4 | met | All named workflows are covered by readable wireframe images and coverage markers are recorded. |
| 5 | met | Theme, implementation, verification, and final polish are documented; the report records cross-workflow validation. |
| 6 | met | The app is deployed at https://faststarter-1ygs.onrender.com and `/health` returns `{"ok":true}`. Marker credentials are reported without exposing database credentials. |

## Recommended next practice

- Provide the student’s full name and student ID, then run the final export command once to produce the PDF cover and packaged transcript appendix.

## Integrity note

- Clean
- No edited skills, failed integrity checks, or suspicion flags were found in the available records.

## Provenance flags

- None found in the available evidence.

## Sincerity log summary

- Blocks found: 0
- max round: 0
- min/mean/final confidence: not recorded
- trend: not applicable
- cleared: no suspicion spiral found

## Skips

- Skips: 0/3 used (from the available Guide records)

## Skill integrity

Course skills are hashed at export and compared to `.agents/skills.lock.json`. Do not edit `.agents/skills/`, `.cursor/skills/`, or `AGENTS.md`.

- Status: **pass**
- Root: `e84cd692d0b85eefe546385661958c27d07e8be6c5176a82012f68ccff5c8beb`
- none
