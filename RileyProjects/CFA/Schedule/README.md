# 7shifts Schedule — CFA (Riley Colley)

**Last updated:** 2026-04-08
**Owner:** Riley Colley, Manager @ Chick-fil-A
**Purpose:** Source-of-truth folder for building an AI-assisted schedule workflow on top of 7shifts. This README exists so any agent (Claude, ChatGPT, Gemini, etc.) can load context on the scheduling project without Riley re-explaining it.

---

## What this project is

Riley is building an AI-assisted scheduling system for his CFA store. 7shifts is the system of record for employees, availability, and published schedules. The goal is a workflow where an AI partner can read real employee + schedule data, learn Riley's style, and help draft weekly schedules that match how Riley actually builds them — not generic scheduling-software output.

The `7shifts_planning_questionnaire.html` in this folder is a 52-question, 5-phase planning doc Riley built to scope the project. Start there if deeper project context is needed.

---

## Folder layout

```
Schedule/
├── README.md                              ← this file
├── 7shifts_planning_questionnaire.html    ← 52-question project scoping doc
├── Chick-fil-A_Schedule_2026-03-16.csv    ← example published schedule (CSV export)
├── Chick-fil-A_Schedule_2026-03-16.numbers
├── Employees/                             ← employee master data
├── Schedule Archive/                      ← published schedules (PDF, weekly)
├── 7shifts Schedule Templates/            ← Riley's recurring template schedules
└── Templates/                             ← role-level blank templates (Director / TL / TM)
```

### `Employees/`
Employee exports from 7shifts. The latest file is the source of truth for who's active.

- **`7 Shifts Employee List_2026-04-08.csv`** — latest full export (1,843 rows, **139 unique active employees**, 628 active role-rows).
- **`7shifts - Availability.pdf`** — availability windows per employee.
- **`Employee List_2026-01-24 2.pdf`** — older snapshot, kept for reference.

### `Schedule Archive/`
Weekly published schedules as exported PDFs from 7shifts. One file per week, named `schedule-YYYY-MM-DD.pdf` using the Monday of that week.

Current files:
- `schedule-2026-03-09.pdf`
- `schedule-2026-04-13.pdf` ← most recent

### `7shifts Schedule Templates/`
Riley's recurring template schedules — the long-term shift patterns he loads into 7shifts as a starting point before tweaking each week.

- `Service Mar '26.jpg / .pdf / .png` — same Service-department template in three formats.
- `Service Mar '26_2026-04-08.png` — updated snapshot captured 2026-04-08 (11.1 MB; larger than the 6.4 MB Mar 24 version, so treat as a newer revision).
- `Service Mar '26_Riley.png` — Riley-annotated version.

### `Templates/`
Blank role-level templates (Director / Team Leader / Team Member) for ad-hoc schedule building outside 7shifts.

---

## Employee data model (from the 2026-04-08 CSV)

CSV columns:
```
First name, Last name, Email, Mobile phone, Location, Department, Role,
Wage, Pay type, User type, Hire date, Termination date, Birthdate,
Employee ID, Punch ID, User status
```

Key facts to remember:

- **One row per employee-role combination**, not per employee. A single employee with multiple roles appears on multiple rows. Of 139 active employees, **137 hold more than one role** — so always dedupe by (First name, Last name) before counting headcount.
- **Status filter:** `User status` is `Active` or `Inactive`. Only 628 of 1,843 rows are Active. Always filter to Active first.
- **Location:** all rows = `CFA` (single-location store).
- **Departments:** `Service` and `Kitchen`. Active breakdown: Service ~101 unique employees, Kitchen ~79 unique employees (with overlap — employees cross-trained across both).
- **Roles seen in the Active set:**
  - `Team Member - Night`
  - `Team Member - Day`
  - `Team Member - Flex`
  - `Hospitality`
  - `Prep`
  - `Team Leader`
  - `Director`
  - `Training`
  - `MARKETING` (note ALL CAPS — formatting quirk in 7shifts, not a typo to fix)
  - A small number of rows have a blank role — those are data hygiene issues in 7shifts, not a distinct role.
- **Wage / Pay type / Hire date / Termination date / Employee ID / Punch ID** are mostly blank in exports — 7shifts does not surface these in the standard CSV. Don't treat blanks as missing data to chase down.

---

## Schedule PDF format (from `schedule-2026-04-13.pdf`)

7shifts publishes schedules as multi-page PDFs, one grid per department. Structure:

- **Header:** `April 13, 2026 - April 19, 2026 Service @ CFA` (date range + department + location).
- **Columns:** `Name | Mon 13 | Tue 14 | Wed 15 | Thu 16 | Fri 17 | Sat 18 | Sun 19`
- **Rows:** one per scheduled employee for that department that week.
- **Cell values:**
  - Shift time: `7:30am - 3pm`, `6:30pm - CL`, `11:15am - 5:30pm` — lowercase am/pm, no leading zero.
  - `CL` = close (end-of-day, no fixed time).
  - `TIME OFF` = approved time off, **not** an unfilled shift.
  - Blank cell = not scheduled that day (neutral, not time off).
- **Footer:** free-text "footnotes" area visible to all employees.

The 2026-04-13 week covers **~90 Service employees** across 3 pages. Riley himself appears in the schedule (`Riley Colley`) — he works shifts in addition to managing.

When reading schedules programmatically, parse by splitting on lines and recognizing `TIME OFF` and `CL` as special tokens distinct from regular `HH[:MM]am/pm - HH[:MM]am/pm` shift strings.

---

## Working with this data

**Before analyzing or building anything on this folder:**

1. Always use the newest CSV in `Employees/` as the source of truth for who's active.
2. Dedupe by name when counting people.
3. Only consider `User status == "Active"`.
4. Don't chase blank `Wage` / `Employee ID` fields — they're blank by design in 7shifts exports.
5. When parsing schedule PDFs, handle `TIME OFF`, `CL`, and empty cells distinctly.
6. Templates in `7shifts Schedule Templates/` reflect Riley's repeating pattern — they're *starting points*, not final schedules. The archive PDFs show what actually got published.

**Schedule naming convention going forward:**
- New weekly exports: `schedule-YYYY-MM-DD.pdf` (Monday of the week) → `Schedule Archive/`
- New employee exports: `7 Shifts Employee List_YYYY-MM-DD.csv` → `Employees/`
- New template snapshots: `<Department> <Month> '<YY>_YYYY-MM-DD.png` → `7shifts Schedule Templates/`

---

## Open questions / TODO for the project

(Not exhaustive — see `7shifts_planning_questionnaire.html` for the full 52-question scope.)

- Decide on the ingestion cadence (weekly manual drop vs. automated pull via 7shifts API).
- Define "Riley's scheduling rules" explicitly — the implicit heuristics (fairness, preferred pairings, closing coverage, Riley's own shifts) he applies when editing the template each week.
- Build a parser that turns the PDF schedule grids + CSV employee list into a structured dataset an agent can reason over.
- Decide whether templates should live as images forever or be rebuilt as structured data (CSV / JSON) so they can be diffed against actual weeks.
