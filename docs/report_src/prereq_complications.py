# -*- coding: utf-8 -*-
"""Pre-build client requirements for the Complications recording (data for build_prereq.py)."""
from build_prereq import COLS, sref

META = dict(
    title="Complications – Pre-Build Client Requirements",
    header="Complications Compliance — Pre-Build Client Requirements (Inputs & Decisions)",
    subtitle="Files, sheets, VBA, business rules and client decisions that must be supplied or confirmed before the modern Complications "
             "compliance system can be built, each with the reason it is required",
    applies="Complications compliance workflow (appointments store + SystmOne → Complications Report.xlsm → Compliance Data.xlsm → dashboard)",
    spec="Complications_Compliance_Workflow_Specification.pdf",
    evidence="Teams recording 20260814_120551 (7:58); timestamps are video positions",
    why="The recording is a walkthrough: the monthly upload, counting, pasting and refresh are described but not performed, and the "
        "operator could not explain several parts. The spec found typed counts, fixed “Within benchmark” output rows, a result dated "
        "09/04/26, two conflicting sets of standards and patient-identifiable data in the workbook.",
    owners=["Tool owner / IT", "Operator", "IT", "Clinical lead / business owner", "Business owner / Caldicott / IG"],
    figs=[[("pq", 80), ("sys1", None)], [("cr1", None)], [("vbe", None)], [("cr2", None), ("bench", None)], [("cdt", None)]],
    decisions_intro="These need clinical-governance and information-governance decisions, not only dashboard decisions.",
    blockers={"F-01", "F-02", "F-03", "S-01", "R-01", "R-02", "R-03", "R-04", "D-01", "D-02", "D-03"},
)

FILES = [COLS,
    ["F-01", "<b>Complications Report.xlsm</b> (full copy) with the <b>All_Appts Power Query (M) code</b>",
     "The query source and filters of the appointments extract were not shown (" + sref("pq") + "). They decide which appointments are counted.",
     "Tool owner", "Ingestion design", "G-03"],
    ["F-02", "<b>SystmOne report definition</b> and an anonymised sample export",
     "The complications export is pasted by hand (" + sref("sys1") + "); the report’s filters and columns set the ingestion contract.",
     "Operator / SystmOne admin", "FR-C01", "EX-01"],
    ["F-03", "<b>Appointments data store access</b> (location, owner, schema)", "Needed to replace the on-open query with a governed feed.", "IT", "FR-C01", "G-03"],
    ["F-04", "<b>The “other document”</b> holding the original automated requirements and timeframes",
     "The data store pulls Complications requirements and timeframes from it (00:07:15–00:07:41).", "Tool owner", "Reference data", "G-11"],
    ["F-05", "<b>Compliance Data.xlsm link list</b> and query definitions", "It shows “UNABLE TO REFRESH – linked workbook” (" + sref("req") + "). Shared with specs 01 and 02.", "Tool owner", "Migration", "G-12"],
    ["F-06", "<b>Dashboard measures</b> for Complications", "Whether rates or only the 8 rows are shown decides the mart.", "BI owner", "Parity", "G-14"],
]

SHEETS = [COLS,
    ["S-01", "<b>How the monthly counts (Compliance Report rows 22–30) are produced</b>", "They are typed (" + sref("cr1") + "); we need the exact source and filters to compute them automatically.", "Operator", "FR-C04", "G-05"],
    ["S-02", "<b>Complications Details log rules</b>: what is copied, how Op Date and clinician are found, what Include in Statistics means", "The log is curated by hand; its rules become the attribution and review rules.", "Operator", "FR-C03", "G-02"],
    ["S-03", "<b>Monthly status columns</b> (Mar-25…Jun-26) and the “at 09/04/26” result block", "The result looks four months stale (" + sref("cr2") + ").", "Operator", "FR-C06", "G-06"],
    ["S-04", "<b>Sheet1, Post-Op Reported Pain Rate, Comps Reported Pivot</b>", "Not opened; may hold rules or outputs.", "Operator", "Discovery", "G-10"],
    ["S-05", "<b>Clinician name list</b> with all variants", "Name variants split figures (" + sref("vfp") + ").", "Operator", "FR-C07", "FM-06"],
]

VBA = [COLS,
    ["V-01", "<b>Export the VBA project</b> (all modules), or confirm there is none", "Only ThisWorkbook was opened and was empty (" + sref("vbe") + "); the operator was unsure.", "IT", "Discovery", "G-01"],
]

RULES = [COLS,
    ["R-01", "<b>Read-code list per complication type</b>", "Five infection codes are tested; others in the export may be missed (FD-03).", "Clinical lead", "FR-C02", "G-04"],
    ["R-02", "<b>Attribution rule</b>: which appointment a complication belongs to; time limit after surgery", "Today: same NHS number, after the appointment, before the next one (spec BR-01).", "Clinical lead", "FR-C03", "BR-01"],
    ["R-03", "<b>Standards</b>: one authoritative set of limits per type and service", "Compliance Report and Benchmarks disagree (" + sref("bench") + ").", "Clinical lead", "FR-C05", "G-08"],
    ["R-04", "<b>Rate definitions</b>: denominators, the 12-month lag for VAS failure, 3/6/12-month windows, spike = max monthly rate", "Read from the sheet but never explained.", "Clinical lead", "FR-C04", "BR-03"],
    ["R-05", "<b>Dehiscence and Sperm Granuloma</b>: how they are measured", "Published but not calculated (SV-04).", "Clinical lead", "FR-C06", "G-09"],
    ["R-06", "<b>Issue, Weighting and Due Date</b> values in the published rows", "Meaning of Issue = 10, Weighting = 1, due + 4 weeks unknown (" + sref("cdt") + ").", "Business owner", "FR-C06", "G-07"],
    ["R-07", "<b>Exclusions</b> (e.g. Dr Saad in one overall rate)", "Rules for excluding clinicians or cases must be explicit.", "Clinical lead", "FR-C04", "G-13"],
]

DECISIONS = [COLS,
    ["D-01", "<b>Lawful basis, DPIA and Caldicott approval</b> for processing patient-level data", "NHS numbers and clinical notes are processed (FM-01).", "Caldicott Guardian / DPO", "Before any data load", "NFR-C02"],
    ["D-02", "<b>What the dashboard may show</b>: aggregates only, small-number rules, clinician-level visibility", "Clinician rates are sensitive; patient data must not reach the dashboard.", "Business owner + IG", "Mart design", "NFR-C01"],
    ["D-03", "<b>Clinical reviewer role</b> for complication attribution", "Replaces the hand-kept log with an accountable review.", "Clinical lead", "FR-C03", "S-02"],
    ["D-04", "<b>Scope</b>: services included (vasectomy, carpal tunnel, minor skin …)", "Services differ in benchmarks (" + sref("bench") + ").", "Business owner", "Data model", "G-08"],
    ["D-05", "<b>Publication cadence and as-of month</b>", "Today the published result date is unclear (09/04/26).", "Business owner", "FR-C06", "FM-04"],
]
