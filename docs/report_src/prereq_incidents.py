# -*- coding: utf-8 -*-
"""Pre-build client requirements for the Incidents recording (data for build_prereq.py)."""
from build_prereq import COLS, sref

META = dict(
    title="Incident Management – Pre-Build Client Requirements",
    header="Incident Management Compliance — Pre-Build Client Requirements (Inputs & Decisions)",
    subtitle="Files, sheets, VBA, business rules and client decisions that must be supplied or confirmed before the modern Incident "
             "Management compliance system can be built, each with the reason it is required",
    applies="Incidents compliance workflow (Datix export → Incident Management.xlsm → Compliance Data.xlsm → dashboard)",
    spec="Incident_Management_Compliance_Workflow_Specification.pdf",
    evidence="Teams recording 20260811_135933 (7:16); timestamps are video positions",
    why="The recording covers only the first half of the update: the Datix export happened off the shared screen and the video stops at "
        "00:07:01, before the #REF! error is fixed and before any refresh or publish. The spec found a broken timeliness formula, a "
        "query-vs-paste contradiction, unmapped categories and 14 open gaps that cannot be guessed safely.",
    owners=["Tool owner / IT", "Operator", "IT", "Business owner", "Business owner / IG lead"],
    figs=[[("dx3", None), ("end", None)], [("tabs", None), ("cat2", None)], [("ctI", 50)], [("dxT", None), ("refz", 80)], [("dxN", None)]],
    decisions_intro="These are policy and governance choices only the business can make. Several depend on incident-governance and "
                    "information-governance leads, not only on the dashboard owner.",
    blockers={"F-01", "F-02", "F-03", "F-04", "S-01", "R-01", "R-02", "R-03", "R-05", "D-01", "D-02", "D-06"},
)

FILES = [COLS,
    ["F-01", "<b>Recording or written steps for the rest of the update</b> (fix #REF!, save, refresh, update data store, publish)",
     "The video stops at 00:07:01 (" + sref("end") + "). Everything after the paste check is unknown, including how the error is fixed and how the data reaches the dashboard.",
     "Operator", "Phase 0 exit; whole publish design", "G-01, P-01"],
    ["F-02", "<b>Datix export definition and an anonymised sample export</b> (report/dashboard used, filters, date range, file type, all columns)",
     "The export was done off the shared screen (00:05:14–00:06:17, " + sref("dx3") + "). The sample sets the ingestion contract and the header checks.",
     "Operator / Datix admin", "FR-I01 ingestion", "G-02, P-02"],
    ["F-03", "<b>Incident Management.xlsm</b> (full copy) with its <b>Power Query (M) code</b>",
     "The Datix table shows a Query ribbon tab, so it is loaded by Power Query, yet the operator describes copy-paste (" + sref("dx1") + "). Only the query shows where pasted data really lands.",
     "Tool owner", "Schema, migration", "G-03, P-03"],
    ["F-04", "<b>File history of the Datix tab</b> (a previous version from before #REF! appeared)",
     "The In set timeframe formula tests a deleted column for “Yes” (" + sref("dxT") + "). We need to know which column it was to restore the rule.",
     "Tool owner", "FR-I04", "G-06"],
    ["F-05", "<b>Compliance Data.xlsm</b> queries that read this tool", "Its Requirements table has 7 columns while Staff Management’s has 10, so the consolidation query must handle both (G-09). Shared with the Staff Management ask.",
     "Tool owner", "Data-store design", "G-09"],
    ["F-06", "<b>Dashboard measures</b> for the incidents dial", "How the percentage per type is computed was not shown (G-13); needed for the parity test.", "BI owner", "T-I04 parity", "G-13"],
    ["F-07", "<b>Datix API / reporting documentation and access</b>", "Needed to decide between an automated pull and a scheduled export (D-01).", "IT / Datix admin", "FR-I01", "P-07"],
]

SHEETS = [COLS,
    ["S-01", "<b>Manage Compliance</b> tab and any macros", "It is the first tab but was never opened; the operator says this tool “doesn’t work in the same way”. It may hold the update logic.", "Operator / IT", "Phase 0 exit", "G-07"],
    ["S-02", "<b>Estates, Health and Safety, Safeguarding, IG, Clinical, SPC, Miscellaneous</b> tabs", "Named after the groupings and SPC types but not opened (" + sref("tabs") + "). They may be the per-group views the dashboard reads.", "Operator", "FR-I07", "G-08"],
    ["S-03", "<b>Groupings Pivot and Harm Pivot</b>", "Likely the summary counts per group and per harm level; the target views must reproduce them.", "Operator", "FR-I07, parity", "G-08"],
    ["S-04", "<b>Notes tabs</b> (All, Clinical, IG, Health and Safety, Estates, Sa… and any further tabs)", "Who writes them, when, and whether the dashboard shows them (" + sref("cat2") + ").", "Operator", "FR-I08", "G-08"],
    ["S-05", "<b>“In last 7 months” formula</b> (Datix column S)", "Not shown; it is a reporting-window rule the dashboard probably depends on (" + sref("refz") + ").", "Tool owner", "FR-I05", "G-05"],
    ["S-06", "<b>Full Datix Category table</b> plus the list of categories present in Datix", "“Administrative Process (excluding documentation)” is in the data but not in the 25-row map (" + sref("dxN") + "), so it drops out of every group.", "Operator", "FR-I03", "G-11"],
    ["S-07", "<b>Missing column</b> on Compliance Timeframes: keep, fix or drop", "It looks in its own table and is TRUE for every row (" + sref("ctI") + ").", "Operator", "Reference load", "SV-04"],
]

VBA = [COLS,
    ["V-01", "<b>Does the workbook contain VBA?</b> If so, export all modules", "The file is .xlsm and has a Manage Compliance tab cloned from the Staff tool, which there runs macros.", "IT", "Phase 0", "G-07"],
    ["V-02", "<b>Any macro or query step that loads, clears or appends Datix rows</b>", "Decides whether each import replaces or appends rows (FM-05), which drives the merge design.", "IT", "FR-I02", "FM-05"],
    ["V-03", "<b>Any macro that writes the Notes tabs or the per-group tabs</b>", "These outputs must be reproduced or retired.", "IT", "FR-I07, FR-I08", "G-08"],
]

RULES = [COLS,
    ["R-01", "<b>Allowed days per harm level</b> (No/Low/Moderate 42, Severe 90, Fatal 365?) and the default", "Read from the formula (" + sref("dxT") + "), but the formula is broken, so the numbers must be confirmed before they are automated.", "Incident governance lead", "FR-I04", "BR-03"],
    ["R-02", "<b>Which date starts the clock</b>: Reported or Incident date; and which date stops it (closure date?)", "The formula uses TODAY() − Reported, so results change daily and closure timing is ignored (FD-03).", "Incident governance lead", "FR-I04, FR-I05", "G-04"],
    ["R-03", "<b>Meaning of “in set timeframe”</b>: closed within the limit, or not yet overdue?", "As written, every open incident counts as in timeframe even when overdue, and closed ones fail once they are old (FD-04).", "Incident governance lead", "FR-I04", "G-04"],
    ["R-04", "<b>The 7-month window</b>: what it is for and which date it uses", "Formula not shown (G-05).", "Business owner", "FR-I05", "G-05"],
    ["R-05", "<b>Compliance % definition per type</b> (numerator, denominator, period)", "The dial turns green only at 100% (" + sref("ctT") + "), so the exact definition decides whether the area is ever green.", "Business owner", "Dashboard parity", "G-13"],
    ["R-06", "<b>Review cadence</b>: monthly, or twice a month?", "Stored 0.5 months vs “we only look at this every month” (" + sref("ctB") + ").", "Business owner", "FR-I09", "SV-02"],
    ["R-07", "<b>What “SPC flagged” means</b> and how incidents are flagged", "Six of the ten compliance types are SPC flags (" + sref("req") + "); the rule is not visible.", "Business owner", "Type definitions", "G-12"],
    ["R-08", "<b>What makes a “Serious incident”</b>", "A compliance type, but no column for it is visible; it may be the deleted column behind #REF!.", "Incident governance lead", "Type definitions", "G-06"],
]

DECISIONS = [COLS,
    ["D-01", "<b>Datix integration route</b>: API pull, scheduled report to a secure folder, or manual upload", "Removes the manual export and paste (EX-01) and decides the security set-up.", "IT + business owner", "FR-I01", "P-07"],
    ["D-02", "<b>Which Datix fields may be stored</b>; in particular Description and Name", "They hold patient narratives and personal names (redacted in the spec). The default is not to store them.", "IG lead / DPO", "Before any data load", "P-06, FM-06"],
    ["D-03", "<b>Category map ownership</b> and approval of new mappings, incl. “Staff Inadequately Trained → Information Governance”", "New Datix categories appear over time; someone must own the map (" + sref("cat1") + ").", "Business owner", "FR-I03", "G-11"],
    ["D-04", "<b>Single subject or per service?</b>", "Incidents carry Division and Service (e.g. Vasectomy Service Essex &amp; Suffolk); the dashboard may need them instead of one Provide Wellbeing subject.", "Business owner", "Data model", "§2.3"],
    ["D-05", "<b>History</b>: keep each monthly import as a snapshot?", "Needed to show how incidents moved from open to closed and to re-create past months.", "Business owner", "FR-I02", "FM-05"],
    ["D-06", "<b>DPIA and retention</b> for incident data in the new system", "Incident records are special-category health data in an NHS context.", "IG lead / DPO", "Before any data load", "NFR-I01"],
    ["D-07", "<b>Named approver</b> for each monthly incidents publication", "Today one person pastes, checks by eye and publishes.", "Business owner", "FR-I06", "BR-08"],
]
