# -*- coding: utf-8 -*-
"""Pre-build client requirements for the Mandatory Training recording (data for build_prereq.py)."""
from build_prereq import COLS, sref

META = dict(
    title="Mandatory Training – Pre-Build Client Requirements",
    header="Mandatory Training Compliance — Pre-Build Client Requirements (Inputs & Decisions)",
    subtitle="Files, sheets, VBA, business rules and client decisions that must be supplied or confirmed before the modern Mandatory "
             "Training compliance system can be built, each with the reason it is required",
    applies="Mandatory training workflow (ESR / WFS / Provide CIC reports and contractor certificates → Training Matrix v3 → Compliance Data.xlsm → dashboard)",
    spec="Training_Compliance_Workflow_Specification.pdf",
    evidence="Teams recording 20260814_113314 (14:33); timestamps are video positions",
    why="The operator rebuilt this logic after its author left and could not explain several fields (timeframe 0.5, Issue, Missing). "
        "The monthly publish deletes and replaces every training row in the data store, requirements are typed by hand, and targets "
        "and thresholds disagree.",
    owners=["Tool owner / HR systems", "Operator", "IT", "Business owner / L&D lead", "Business owner / IG"],
    figs=[[("cdM", None)], [("ddn", None), ("ovw", None)], [("trE", 40)], [("ctt", None), ("rol", None)], [("reqA", None)]],
    decisions_intro="These decide how training is governed in the new system; several belong to Learning & Development and HR, not only to the dashboard owner.",
    blockers={"F-01", "F-02", "F-03", "S-01", "R-01", "R-02", "R-03", "D-01", "D-02", "D-04"},
)

FILES = [COLS,
    ["F-01", "<b>Training Matrix v3</b> (full copy) and confirmation of file type / any VBA", "Read every formula and hidden column directly; the extension and macros were not visible (G-11).", "Operator", "Discovery", "G-11"],
    ["F-02", "<b>Sample monthly reports</b> from ESR, Workforce Solutions and Provide CIC L&amp;D (anonymised)", "They are the main sources of training dates (00:04:26) and set the import contracts.", "HR systems / WFS / L&amp;D", "FR-T04", "G-05"],
    ["F-03", "<b>Compliance Data.xlsm</b> with the Most Recent formula and the current training rows", "Needed to confirm why Most Recent fails for training (" + sref("cdM") + ") and to migrate.", "Tool owner", "FR-T03", "G-01"],
    ["F-04", "<b>Staff identifiers</b> per source (ESR employee number, WFS worker ID)", "Matching by name fails with prefixes and spelling variants.", "HR systems", "FR-T04", "FM-03"],
    ["F-05", "<b>Dashboard measures</b> for People › Training", "The operator is unsure whether the transfer rows are used as-is (G-08).", "BI owner", "Parity", "G-08"],
]

SHEETS = [COLS,
    ["S-01", "<b>Full course list</b> with intervals, groups and supersession (Training Details) — approved", "Drives every expiry and supersession (" + sref("trd") + ").", "L&amp;D lead", "FR-T01", "BR-01"],
    ["S-02", "<b>Roles table review</b>: is Roles_Training12 the source of truth for requirements?", "Requirements are typed by hand and can disagree (" + sref("rol") + ").", "L&amp;D lead", "FR-T02", "SV-03"],
    ["S-03", "<b>Unused tabs</b>: Course Detail, Nurses, Staff Filter, Transfer from v…, Role Rules, OMcGOW, Training Intervals", "Several show #REF! or Medical Devices headers (" + sref("ddn") + "); decide what to retire.", "Operator", "Scope", "G-07"],
    ["S-04", "<b>How Expiry Date is filled</b> in Completed Training", "Typed or calculated changes the import rules.", "Operator", "FR-T06", "G-06"],
    ["S-05", "<b>Staff list value lists</b> (Status, Employer, Training System, Role2)", "Free values break filters and joins.", "Operator", "FR-T07", "G-10"],
]

VBA = [COLS,
    ["V-01", "<b>Confirm whether the matrix has any VBA</b>", "None was run on screen; needed to complete the inventory.", "IT", "Discovery", "G-11"],
]

RULES = [COLS,
    ["R-01", "<b>Validity rule</b>: interval per course, 45-day Expiring window, one-off courses", "Read from the formula (" + sref("ctE") + "); must be confirmed before automation.", "L&amp;D lead", "FR-T06", "BR-01"],
    ["R-02", "<b>Supersession rules</b> (which higher course satisfies which lower one)", "Drives Required / Not Required (BR-03).", "L&amp;D lead", "FR-T01", "BR-03"],
    ["R-03", "<b>Per-course targets</b>: one set (90%/95%?) for overview and dashboard", "Overview targets and timeframe thresholds disagree (" + sref("ctt") + ", " + sref("ovw") + ").", "Business owner", "FR-T08", "SV-04"],
    ["R-04", "<b>Meaning of 0.5 timeframe and Issue = 10</b>", "Unexplained constants copied into the store.", "Business owner", "Data model", "G-02, G-03"],
    ["R-05", "<b>Which staff are counted</b>: current only; onboarding excluded; on-hold?", "Current Staff logic depends on Status and dates (BR-05).", "Business owner", "FR-T06", "BR-05"],
    ["R-06", "<b>Moving and Handling rule</b> for roles where the course name differs", "It showed Not Required until the correct course was recorded (00:09:20).", "L&amp;D lead", "FR-T02", "G-09"],
]

DECISIONS = [COLS,
    ["D-01", "<b>Keep full training history in the new store</b> (no monthly delete-and-replace)", "The store currently loses history every month (FM-01).", "Business owner", "FR-T03", "SV-01"],
    ["D-02", "<b>Source of truth for staff</b> (ESR / HR system vs the matrix)", "Decides identifiers and who maintains the register.", "HR / business owner", "Data model", "FM-03"],
    ["D-03", "<b>Contractor evidence process</b>: certificate upload, reviewer, reminders", "Direct contractors are chased by email today (BR-07).", "Business owner", "FR-T05", "BR-07"],
    ["D-04", "<b>IG approval</b> for staff contact data and HR notes in the new system", "Emails and comments are copied widely (FM-09).", "IG lead / DPO", "Before data load", "NFR-T01"],
    ["D-05", "<b>Named approver</b> for monthly training publication", "One person edits and publishes today.", "Business owner", "Publication", "EX-04"],
]
