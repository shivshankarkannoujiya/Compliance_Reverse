# -*- coding: utf-8 -*-
"""Pre-build items that come from the client's source template (sources/Wellbeing Dashboard current data template.xlsx).

build_prereq.py appends these rows to the per-area tables. IDs carry a -DS suffix so they never clash with the
recording-based IDs; "DSL §n" refers to 00_Overview/Compliance_Data_Store_Logic.pdf.
"""

TOOL = {"staff": "Staff Management.xlsm", "incidents": "Incident Management.xlsm", "incidents_full": "Incident Management.xlsm",
        "complications": "Complications Report.xlsm", "training": "the Training Matrix", "feedback": "the survey tools",
        "rtt": "the RTT tool"}


def _shared(p):
    return {
        "VBA": [["V-DS1", "<b>Copy-to-store and Last Updated macros</b> of " + TOOL[p] + " (.bas export), or a statement that the tool has none",
                 "The template says each tool copies into Compliance Data “via VBA” and that Last Updated is written “semi-automatically by each user input tool”, "
                 "but the only macro supplied is the Self-Pay one (tab 04 row 49), and the recording shows manual work. The write rule decides how duplicates are prevented.",
                 "IT / tool owner", "Loader design", "DSL §7, DS-12"]],
        "RULES": [["R-DS1", "<b>Missing record and Active rules</b>: a requirement with no record counts as Non Compliant, and only Required + Active rows count toward %",
                   "Written in the data store’s Requirements formulas (tab 04 rows 212–217). The new scoring must keep them or change them on purpose.",
                   "Business owner", "Scoring parity", "DSL §4.3, DS-06"]],
        "DECISIONS": [["D-DS1", "<b>Keep or retire</b> the data store’s unexplained calculations (Snapshot, Encoded and Rank columns, Column1) as they affect this area",
                       "The client marks 17 of the 88 data-store rows as Unclear/Unknown. Rebuilding them without a purpose adds cost; dropping one the dashboard uses breaks a visual.",
                       "Business owner + BI owner", "Dashboard scope", "DSL §8, DS-17"]],
    }


SPECIFIC = {
    "staff": {"RULES": [["R-DS2", "<b>Blank due date</b>: should a staff item with no due date count as compliant?",
                         "The data store’s default rule marks it Compliant (tab 04 row 192), so missing data shows green.",
                         "Business owner", "FR-08", "DSL §3, DS-02"]]},
    "incidents": {"RULES": [["R-DS2", "<b>Issue = 10 means compliant</b> and the Incidents sub-group RAG rule (non-SPC failure → 0; one Moderate Harm → 0.5; ≥ 2 SPC → 0.5; 1 SPC → 0.8)",
                             "Now documented by the client (tab 04 rows 192, 243). Two failing Moderate Harm types are not caught and can score 1.",
                             "Incident governance lead", "Scoring", "DSL §5.1, DS-07"]]},
    "incidents_full": {"RULES": [["R-DS2", "<b>Incidents sub-group RAG rule</b>: confirm the order of the checks and the score for two failing Moderate Harm types",
                                  "The client’s formula (tab 04 row 243) scores one Moderate Harm failure 0.5 but lets two fall through to the SPC rules, where they can score 1.",
                                  "Incident governance lead", "Scoring", "DSL §5.1, DS-07"]]},
    "complications": {"DECISIONS": [["D-DS2", "<b>Complications in Requirements_Detailed</b>: should it be added?",
                                     "complications_requirements_Table is combined into Requirements and the timeframes table but not into Requirements_Detailed (tab 04 rows 202, 227, 249), "
                                     "so Complications may be missing from one dashboard table.", "Tool owner + BI owner", "Dashboard parity", "DSL §2.1, DS-10"]]},
    "training": {"RULES": [["R-DS2", "<b>Training compliance rule</b>: compliant whenever Completion Status is filled, or only until the training expires?",
                            "The data store marks Training compliant on Completion Status alone (tab 04 row 192), ignoring the due date that the Training Matrix calculates.",
                            "Business owner", "Rules engine", "DSL §3, DS-03"]]},
    "feedback": {"RULES": [["R-DS2", "<b>Issue = 10 means compliant</b> for Feedback: confirm how the SPC result sets Issue",
                            "The data store judges Feedback only by Issue = 10 (tab 04 row 192), so the mapping from the survey SPC result to Issue is the whole rule.",
                            "Business owner", "Scoring", "DSL §3"]]},
    "rtt": {"DECISIONS": [["D-DS2", "<b>Which compliance area and Level 2 group RTT belongs to</b>",
                           "RTT is not one of the 12 areas named in the Power Query combine lists (tab 04 rows 202, 227). The group decides whether Issue = 10, a due date or an SPC rule makes it compliant.",
                           "Tool owner", "Scoring", "DSL §2.1, DS-11"]]},
}


def extra(profile):
    out = _shared(profile)
    for k, rows in SPECIFIC.get(profile, {}).items():
        out[k] = out.get(k, []) + rows
    return out
