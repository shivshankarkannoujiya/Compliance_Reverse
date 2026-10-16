# -*- coding: utf-8 -*-
"""Pre-build client requirements for the Survey Feedback recording (data for build_prereq.py)."""
from build_prereq import COLS, sref

META = dict(
    title="Survey Feedback – Pre-Build Client Requirements",
    header="Survey Feedback Compliance — Pre-Build Client Requirements (Inputs & Decisions)",
    subtitle="Files, sheets, VBA, business rules and client decisions that must be supplied or confirmed before the modern Survey "
             "Feedback compliance system can be built, each with the reason it is required",
    applies="Survey feedback workflow (Survicate → 24 hr All Surveys / Survey Management → Compliance Data.xlsm → dashboard)",
    spec="Feedback_Compliance_Workflow_Specification.pdf",
    evidence="Teams recording 20260814_111322 (7:07); timestamps are video positions",
    why="The operator follows a design they did not build (“designed by Matt, so we just follow his process”), runs two overlapping "
        "workbooks, cleans exports by hand and could not explain the SPC parameters. The acceptance rule spoken aloud also differs from the "
        "SPC logic in the sheets.",
    owners=["Tool owner / IT", "Operator", "IT", "Patient experience lead", "Business owner / IG"],
    figs=[[("exp", None), ("pq2", None)], [("smct", None)], [("cmR", None)], [("spch", None)], [("cmp", None)]],
    decisions_intro="These decide how patient feedback is judged and governed in the new system.",
    blockers={"F-01", "F-02", "S-01", "R-01", "R-02", "R-03", "D-01", "D-02"},
)

FILES = [COLS,
    ["F-01", "<b>Survey Management.xlsm and 24 hr All Surveys</b> (full copies) with Power Query (M) code", "Needed to read the SPC formulas and the failing queries (" + sref("pq2") + ").", "Tool owner", "Discovery", "G-06"],
    ["F-02", "<b>Survicate API access</b> (or scheduled export) and the list of surveys in scope", "Replaces the manual download (" + sref("svl") + ").", "Patient experience lead / IT", "FR-F01", "G-07"],
    ["F-03", "<b>One month of raw exports</b> (anonymised) with the cleaned versions", "Shows exactly what the manual cleaning removes.", "Operator", "FR-F02", "G-02"],
    ["F-04", "<b>Dashboard measures</b> for People › Feedback", "Parity test.", "BI owner", "T-F01", "G-08"],
]

SHEETS = [COLS,
    ["S-01", "<b>Which tool is authoritative</b>: 24 hr All Surveys or Survey Management", "Both build the same table and both write requirements (" + sref("smct") + ").", "Operator / business owner", "Scope", "G-01"],
    ["S-02", "<b>SPC sheet design</b>: baseline period, σ method, rule list", "Read from the sheets but not explained (" + sref("spch") + ").", "Operator", "FR-F04", "G-04"],
    ["S-03", "<b>Compliance tab cross-link</b> to Incident Management Estates", "Purpose unknown (" + sref("cmR") + ").", "Operator", "FR-F05", "G-05"],
    ["S-04", "<b>Self Pay Types</b> list complete and current", "Maps self-pay responses to services (" + sref("spt") + ").", "Operator", "FR-F03", "BR-05"],
]

VBA = [COLS,
    ["V-01", "<b>Confirm whether Survey Management.xlsm has VBA</b>", "Macro-enabled file; no macro used on screen.", "IT", "Discovery", "—"],
]

RULES = [COLS,
    ["R-01", "<b>Acceptance rule</b>: per-response “4 or 5 acceptable” or SPC on monthly averages?", "Spoken rule differs from the sheets (SV-01, SV-02).", "Patient experience lead", "FR-F04", "G-03"],
    ["R-02", "<b>Spoilt-response definition</b>", "Manual deletion today (00:01:46).", "Patient experience lead", "FR-F02", "G-02"],
    ["R-03", "<b>SPC parameters</b>: baseline, 3σ limits, run length 7, trend length, 2-of-3 rule", "Must be fixed and versioned before automation.", "Patient experience lead", "FR-F04", "G-04"],
    ["R-04", "<b>Service groups</b>: All, NHS, Self Pay, VAS, CTS, ND (is POD included?)", "Defines the six compliance types.", "Business owner", "Data model", "G-07"],
    ["R-05", "<b>Minimum responses per month</b> before SPC is applied", "Small months make averages unstable.", "Patient experience lead", "FR-F04", "—"],
]

DECISIONS = [COLS,
    ["D-01", "<b>Store patient comments or not</b>", "Free-text patient feedback in shared files today (FM-07).", "IG lead / DPO", "Before data load", "NFR-F01"],
    ["D-02", "<b>Retire one of the two tools and unify type names</b>", "Duplicate requirement rows in the store (SV-03).", "Business owner", "FR-F06", "G-01"],
    ["D-03", "<b>Named approver</b> for monthly feedback publication", "One person runs and publishes today.", "Business owner", "Publication", "—"],
]
