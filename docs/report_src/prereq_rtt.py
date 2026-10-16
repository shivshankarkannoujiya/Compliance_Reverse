# -*- coding: utf-8 -*-
"""Pre-build client requirements for the RTT recording (data for build_prereq.py)."""
from build_prereq import COLS, sref

META = dict(
    title="RTT – Pre-Build Client Requirements",
    header="RTT Compliance — Pre-Build Client Requirements (Inputs & Decisions)",
    subtitle="Files, sheets, VBA, business rules and client decisions that must be supplied or confirmed before the modern RTT "
             "compliance system can be built, each with the reason it is required",
    applies="RTT compliance workflow (SystmOne → RTT breach report → RTT Data → Compliance Data.xlsm → dashboard)",
    spec="RTT_Compliance_Workflow_Specification.pdf",
    evidence="Teams recording sixth/MEDDAD~1.MP4 (8:42); timestamps are video positions",
    why="During the recording the operator deleted the column holding service-specific breach rules and switched the RTT week to ROUNDDOWN, "
        "which turned a breached patient into a compliant one. The breach report, Column43 and the weighting could not be explained. "
        "These must be settled before any rule is automated.",
    owners=["Operational / IT", "Operator", "IT", "RTT / operational lead", "Business owner / IG"],
    figs=[[("pq", None)], [("col43", None)], [("ref", None)], [("bd2", None), ("rdn", None)], [("e2", None)]],
    decisions_intro="RTT is a national NHS standard, so these decisions belong to the operational and contract leads as well as the dashboard owner.",
    blockers={"F-01", "F-02", "S-01", "R-01", "R-02", "R-03", "D-01", "D-02"},
)

FILES = [COLS,
    ["F-01", "<b>RTT Data workbook — the version before 14/08/2026</b> and the current one", "The live edit removed Breach Date 2 and changed rounding (" + sref("ref") + "); we need to know what is in production now and what it replaced.", "Operator / IT", "Phase 0", "G-01"],
    ["F-02", "<b>RTT breach report</b> and the SystmOne report definition behind it", "The query source and how breach dates are produced were not shown (" + sref("pq") + ").", "Operational team", "FR-R01", "G-05"],
    ["F-03", "<b>Anonymised sample</b> of one week’s RTT list", "Tests and parity without patient identifiers.", "Operator", "T-R01", "—"],
    ["F-04", "<b>Dashboard measures</b> for RTT Compliance", "Parity and threshold use.", "BI owner", "Parity", "—"],
]

SHEETS = [COLS,
    ["S-01", "<b>Compliance column formula</b> on the RTT List", "Not shown; it decides Compliant / Not Compliant.", "Operator", "FR-R03", "G-08"],
    ["S-02", "<b>Column43</b>: meaning and source", "“Can’t actually remember” (" + sref("col43") + ").", "Operational team", "Data model", "G-04"],
    ["S-03", "<b>Service list</b>: are ECC Autism in Schools and Norfolk and Waveney ASD still reported?", "They had special breach rules but are not among the ten requirements.", "Operational lead", "FR-R02", "G-02"],
]

VBA = [COLS,
    ["V-01", "<b>Confirm there is no VBA</b> in RTT Data or the breach report", "Not seen in the recording.", "IT", "Discovery", "—"],
]

RULES = [COLS,
    ["R-01", "<b>Breach test</b>: compare dates, or rounded weeks (and which rounding)?", "ROUNDDOWN hid a breach (" + sref("rdn") + ").", "RTT lead", "FR-R03", "SV-02"],
    ["R-02", "<b>Service-specific breach offsets</b> (+70 ECC Autism, +42 Norfolk and Waveney ASD): keep, change or drop", "They were deleted live (" + sref("bd2") + ").", "RTT lead", "FR-R02", "SV-01"],
    ["R-03", "<b>RAG boundary</b>: is exactly 92% compliant?", "Formula says no, speech says “less than 92 is red” (" + sref("e2") + ").", "Business owner", "FR-R04", "SV-03"],
    ["R-04", "<b>Services with no patients</b>: compliant, not applicable or hidden?", "Current formula gives #DIV/0!.", "Business owner", "FR-R04", "FD-02"],
    ["R-05", "<b>Meaning of weighting = 1</b>", "Unexplained constant.", "Business owner", "Data model", "G-07"],
]

DECISIONS = [COLS,
    ["D-01", "<b>Restore or accept the 14/08/2026 formula change</b>", "Determines whether recent weekly figures are correct.", "RTT lead + business owner", "Before parity", "G-01"],
    ["D-02", "<b>IG approval</b> for NHS-number data in the new system; dashboard aggregates only", "Patient identifiers are processed (FM-04).", "IG lead / DPO", "Before data load", "NFR-R01"],
    ["D-03", "<b>Change-control owner</b> for RTT rules", "No review of rule changes today (FM-01).", "Business owner", "FR-R05", "FM-01"],
    ["D-04", "<b>Weekly as-of day</b> for publication", "Results depend on the day the file is opened (FD-01).", "Business owner", "NFR-R02", "FD-01"],
]
