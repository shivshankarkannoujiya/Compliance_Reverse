# -*- coding: utf-8 -*-
"""Pre-build client requirements for the full Incidents recording (data for build_prereq.py)."""
from build_prereq import COLS, sref

META = dict(
    title="Incident Management (Full Process) – Pre-Build Client Requirements",
    header="Incident Management Compliance (Full Process) — Pre-Build Client Requirements",
    subtitle="Additional files, rules and decisions needed for the incidents build, beyond the list in 02_Incident_Management, each with the reason it is required",
    applies="Incidents compliance (RLDatix → Incident Management.xlsm → Compliance Data.xlsm → dashboard)",
    spec="Incident_Full_Compliance_Workflow_Specification.pdf",
    evidence="Teams recording 20260814_102641 (10:00); timestamps are video positions",
    why="This recording shows the full process, so most of the earlier unknowns are now answered. What remains are rule decisions "
        "(timeframe on Severity, SPC for counts, one RAG rule) and a stable Datix extract. Use this list together with the checklist in 02_Incident_Management.",
    owners=["Datix admin / IT", "Operator", "IT", "Incident governance lead", "Business owner / IG"],
    figs=[[("expd", None)], [("d57", None)], [("mc", None)], [("dxT", None)], [("e4", None)]],
    decisions_intro="These decisions finalise the incident rules the new system will apply automatically.",
    blockers={"F-01", "R-01", "R-02", "R-03", "D-01"},
)

FILES = [COLS,
    ["F-01", "<b>Datix report definition</b> (or API query) replacing the dashboard widget export", "The export is one widget’s Excel download (" + sref("expd") + "); its columns changed between 11/08 and 14/08.", "Datix admin", "FR-IF01", "G-01"],
    ["F-02", "<b>Current Incident Management.xlsm</b> (the 14/08 version)", "It still has the review-panel column that the 11/08 file lost; it is the migration baseline.", "Operator", "Migration", "G-06"],
]

SHEETS = [COLS,
    ["S-01", "<b>SPC sheets</b>: purpose of the unexplained table and the rule columns", "“I don’t know what that table is” (00:07:45).", "Operator", "FR-IF03", "G-02"],
    ["S-02", "<b>Harm Pivot</b>: is it used?", "Not opened in detail.", "Operator", "Scope", "G-05"],
]

VBA = [COLS,
    ["V-01", "<b>Confirm there is no VBA</b> in Incident Management.xlsm", "None run on screen; the operator contrasts it with Staff Management’s VBA.", "IT", "Discovery", "—"],
]

RULES = [COLS,
    ["R-01", "<b>Timeframe by Severity</b> (42 / 90 / 365 days and the review-panel rule)", "The SWITCH tests Description, so it never applies (" + sref("dxT") + ").", "Incident governance lead", "FR-IF02", "SV-01"],
    ["R-02", "<b>SPC method for counts</b> (chart type, baseline, rules)", "LCL is negative for counts; rows extended by hand (" + sref("spc") + ").", "Incident governance lead", "FR-IF03", "G-07"],
    ["R-03", "<b>One RAG mapping</b> for non-compliance", "3 for Moderate Harm, 2 for Severe Harm (" + sref("e4") + ").", "Business owner", "FR-IF05", "SV-02"],
]

DECISIONS = [COLS,
    ["D-01", "<b>Which Datix fields are stored</b>, especially Description", "Patient narratives are in the export and workbook (" + sref("dx") + ").", "IG lead / DPO", "Before data load", "FM-01"],
    ["D-02", "<b>Store Datix IDs as evidence</b> on non-compliant rows", "Replaces the notes tabs (" + sref("notesJ") + ").", "Business owner", "FR-IF04", "—"],
]
