# -*- coding: utf-8 -*-
"""Pre-build client requirements for the Staff Management recording (data for build_prereq.py)."""
from build_prereq import COLS, sref

META = dict(
    title="Staff Management – Pre-Build Client Requirements",
    header="Staff Management Compliance — Pre-Build Client Requirements (Inputs & Decisions)",
    subtitle="Files, sheets, VBA, business rules and client decisions that must be supplied or confirmed before the modern Staff "
             "Management compliance system can be built, each with the reason it is required",
    applies="Staff Management compliance workflow (Staff Management.xlsm → Compliance Data.xlsm → dashboard)",
    spec="Staff_Management_Compliance_Workflow_Specification.pdf",
    evidence="Teams recording 20260811_131142 (30:54); timestamps are video positions",
    why="The recording shows how the operator <i>uses</i> the tool, but not the code, the hidden columns, "
        "the data store or the policy behind it. Building without these inputs would mean guessing, and the spec found 16 failure modes, "
        "9 spoken-vs-recorded discrepancies and 19 open gaps that guesses would either copy or get wrong.",
    owners=["Tool owner / IT", "Operator", "IT", "Business owner", "Richard / IG lead"],
    figs=[[("vba", None), ("tb", 95)], [("ct2", None), ("rol", 95)], [("mcU", None), ("mcU2", None)], [("mcA", None)], [("reqA", None)]],
    decisions_intro="These are policy choices only the business can make. The operator named Richard as the decision-maker for the open policy questions (00:09:54).",
    blockers={"F-01", "F-02", "F-03", "S-05", "S-08", "V-05", "R-01", "R-03", "R-06", "R-09", "D-01", "D-02", "D-03", "D-07", "D-08"},
)

FILES = [COLS,
    ["F-01", "<b>VBA project export</b> of Staff Management.xlsm (all modules and form code, as .bas/.cls, or the .xlsm with the project unlocked)",
     "All write logic sits in macros that were never shown. Without the code we cannot reproduce how <i>Add New Compliance</i> appends, which row <i>Update Existing Compliance</i> overwrites, or why a blank row stops a batch. The close macro fails with run-time error 13 (" + sref("vba") + ") and an internal expert could not debug it (00:28:09).",
     "IT / tool owner", "Phase 0 exit; FR-09, FR-10, FR-14", "P-01, G-04, G-15"],
    ["F-02", "<b>Compliance Data.xlsm</b>: full copy with every table and all Power Query (M) queries",
     "This is the real data store and the dashboard feed, and it was never on screen (" + sref("tb") + " is a 0.3 s glimpse). We need compliance_Data_Store_Table’s columns (only Unique Lookup 3 and Compliance Notes are known, " + sref("mcV") + ") and the PQ tables built from every tool, which set the migration source and the dashboard contract.",
     "Tool owner", "Schema design, migration, parity test", "P-02, G-02, G-06"],
    ["F-03", "<b>Staff Management.xlsm</b> itself (current production copy), with hidden columns left as they are",
     "Lets us read every formula directly instead of from video frames, and catches columns never scrolled to. It is also the main migration source (~140 names, ~2,320 requirement rows).",
     "Operator", "Migration (DM-01)", "§2, DM-01"],
    ["F-04", "<b>Dashboard file</b> (likely Power BI, to confirm) with its measures and visuals",
     "The gauge colours use Threshold 1–5 and the dashboard filters on Active = TRUE (00:04:16, 00:10:40), but the tool, measures and meaning of Threshold 1 (= 1) were never shown. The new views must feed the same visuals.",
     "BI owner", "FR-20, T-03 parity", "G-16"],
    ["F-05", "<b>The other user-input tools</b> (Estates, Medical Devices, Incidents …) or one example of each",
     "The operator says they share the same pattern and that PQ merges them all (00:03:22, 00:27:02). The generic subject model must fit them before its schema is frozen.",
     "Tool owner", "FR-18, schema freeze", "P-11"],
    ["F-06", "<b>The matching video for the Incidents workflow</b> (meeting 20260811 135933) and its transcript",
     "The supplied .srt belongs to that meeting, not this one. It describes a Datix export pasted into a tool and a #REF! error that need their own specification.",
     "Operator", "Incidents scope", "G-01"],
    ["F-07", "<b>Last Updated tab / process note</b>", "“Last updated” is filled in by hand because its macro fails (00:27:57–00:29:22). We need to know where it lives and who reads it, to replace it with an automatic publish timestamp.",
     "Operator", "FR-14", "EX-03"],
]

SHEETS = [COLS,
    ["S-01", "<b>Instructions</b> tab contents", "Never opened. It may hold rules or steps the operator follows but did not mention.", "Operator", "Discovery", "G-12"],
    ["S-02", "<b>Manage Onboarding</b> tab and its workflow", "Never opened, yet onboarding rows already exist in Requirements (e.g. Shahzad Aslam rows 2102–2119, " + sref("req0") + ") and in the type list (" + sref("ct2") + "). Scope depends on decision D-03.",
     "Operator", "Onboarding scope", "G-12"],
    ["S-03", "<b>Manage Compliance hidden columns H–N</b> unhidden and explained", "Column letters jump from G to O (" + sref("mcS") + "). Hidden columns usually hold lookups the macros rely on.", "Operator", "FR-06…FR-08", "G-10"],
    ["S-04", "<b>Manage Requirements helper columns M:T</b> (“originally hidden”) explained", "The macro reads them (T11 = coalesce of new and existing values, " + sref("mrT") + "); the operator was unsure what they do (00:13:56). A “Site” header shows the form was copied from the Estates tool.",
     "Operator / IT", "FR-04", "G-10"],
    ["S-05", "<b>Full Compliance_Timeframe_Table</b> (all rows, including row 43 onwards)", "IR35 Compliant is in the 22-item list and has a 12-month timeframe, but is not among the table rows seen (" + sref("ct2") + ", " + sref("ct3") + "). The catalogue drives every requirement, due date and gauge.",
     "Operator", "Reference data load", "P-03, G-05"],
    ["S-06", "<b>Roles tab</b>: corrected list, and whether it is used at all", "The header row holds data (“Reception | Non-clinical”, " + sref("rol") + "), so one role is lost. The operator thinks the tab may be unused (00:12:17).",
     "Operator", "FR-17", "FM-12"],
    ["S-07", "<b>Manage Requirements Role cell (D8)</b>: source and purpose", "It showed “Surgical Clinician – NHS Only” for two different people (" + sref("mr0") + ", " + sref("mrB") + "). It is either a broken lookup or dead UI.",
     "Operator", "FR-04", "G-11"],
    ["S-08", "<b>Names columns</b>: which are mandatory, and what Contract, WTE, PD Name and PD Login Email mean", "Only Name and Active are known to matter (00:03:41–00:04:16). Managed By may or may not be required (00:03:56). " + sref("nm1"),
     "Business owner", "FR-01, FR-11", "P-07, G-17"],
    ["S-09", "<b>Start Date column</b>: cell type and the intended format", "The new row shows 8/1/2026 while others show dd/mm/yyyy (" + sref("nmX") + "): a text-vs-date or locale problem that will break the migration.",
     "Operator", "DM-02", "G-09"],
]

VBA = [COLS,
    ["V-01", "<b>List Missing</b>: confirm its logic", "It appears to use the Missing column, which only checks the person selected on the form (" + sref("ctJ") + ", " + sref("mrL") + "). Confirms the rule for the new missing-requirements view.", "IT", "FR-05", "SV-09"],
    ["V-02", "<b>Add Requirements</b>: duplicate handling", "Requirement counts of 23 and 45 against 22 types (" + sref("nm3") + ") suggest duplicate or onboarding rows. Does the macro prevent a second row for the same person and type?", "IT", "FR-04, DM-03", "FM-11"],
    ["V-03", "<b>Update Requirements</b>: what it overwrites", "Not shown in the video. We need to know whether it edits in place or adds a row, to design the requirement history (SCD-2).", "IT", "FR-04", "§2.5"],
    ["V-04", "<b>Add New Compliance</b>: append rule and the “miss a row” behaviour", "Operator: “it doesn’t like it if you miss a row” (00:20:45). We must know whether later rows are silently skipped (FM-08), and whether the due date is stored or calculated.", "IT", "FR-07, FR-11", "FM-08"],
    ["V-05", "<b>Update Existing Compliance</b>: which record it overwrites when several exist", "The store keeps history, but lookups return the first match (" + sref("mcV") + "). The amendment overwrote 01/06 with 01/05 in place (" + sref("mcU2") + "). The answer decides whether migrated history can be trusted.", "IT", "FR-09, FR-10, DM-03", "G-04"],
    ["V-06", "<b>Delete flag (column AC)</b>: accepted values and effect", "Mentioned (00:24:59) but never used. Is it a hard delete? Needed to map it to a voided event with a reason.", "IT", "FR-09", "§2.6"],
    ["V-07", "<b>Close / last-updated macro</b>: code and the cause of error 13", "Shown failing (" + sref("vba") + "). Its intended behaviour becomes the automatic publish timestamp.", "IT", "FR-14", "G-15"],
    ["V-08", "<b>Workbook events</b> (Open, BeforeSave, BeforeClose) and any auto-refresh triggers", "Closing the tool restarted a background query (00:29:20 onward), and the operator avoids saving at close because lookups “can corrupt” (00:29:29). Hidden event code may explain both.", "IT", "NFR-06", "G-18"],
]

RULES = [COLS,
    ["R-01", "<b>Due-date rule</b>: due = completion + frequency; is the due date the expiry day or the day before?", "Speech: PI insurance runs “to 31 May next year”; the screen shows due 01/06/2027 (" + sref("mcA") + "). It is a one-day difference on every item.", "Business owner", "FR-07", "P-05, SV-03"],
    ["R-02", "<b>Due date on correction</b>: always recalculated, or may it be typed?", "On the update path it was typed by hand (" + sref("mcU") + "), so it can drift from the frequency.", "Business owner", "FR-07, FR-09", "FM-09"],
    ["R-03", "<b>RAG rule</b>: amber window; how Scheduled and Sign-off Required count", "RAG is picked by hand today (" + sref("mc2") + ", " + sref("mc3") + "), so a lapsed item can stay Green.", "Business owner", "FR-08", "P-06, FM-10"],
    ["R-04", "<b>Gauge thresholds</b>: confirm 1 / 0.9 / 0.8 / 0.7 / 0.6 (DBS 1 / 0.98 / 0.9 / 0.8 / 0.7) and what Threshold 1 means", "They were set by one person (00:11:03) and drive dashboard colours (" + sref("ct3") + ").", "Business owner", "FR-17, FR-20", "G-16"],
    ["R-05", "<b>Coverage metric definition</b>: which rows count toward “compliance types added”", "The current count mixes onboarding rows with a 22-type total, giving 23/22 and 45/22 (" + sref("nm3") + ").", "Business owner", "FR-19", "FM-11"],
    ["R-06", "<b>History vs overwrite</b>: keep every compliance record, or only the latest?", "The operator says the store builds “a picture over time” (00:25:08) but corrections overwrite (00:25:52). The target design keeps everything; please confirm this is wanted.", "Business owner", "FR-09, FR-10", "BR-11"],
    ["R-07", "<b>Deactivation rule</b>: when someone leaves, are their records kept and hidden, or removed?", "Testy Tester was hidden with Active = FALSE and kept (" + sref("nmY") + "). Effective dates (active from/to) need the agreed rule.", "Business owner", "FR-03", "BR-05"],
    ["R-08", "<b>Never-expiring items</b>: confirm that 10000 months means “no renewal”", "Onboarding items use 10000 as a sentinel (" + sref("ct2") + "). It will become an explicit never-expires flag.", "Business owner", "FR-17", "BR-07"],
    ["R-09", "<b>Mandatory fields</b> for a person and for a compliance record", "A blank Managed By became 0 in 22 rows until fixed by hand (" + sref("reqA") + " → " + sref("reqMB") + ").", "Business owner", "FR-11", "P-07, EX-01"],
]

DECISIONS = [COLS,
    ["D-01", "<b>Core vs non-core list</b> for all 22 types (catalogue default)", "The operator disagrees with the current flags: accreditation and performance review “should be core”; “Matt very much decided these on his own” (00:08:32–00:08:48). The core percentage on the dashboard depends on it.", "Richard (business owner)", "Policy v2, go-live", "P-04, G-08"],
    ["D-02", "<b>Compliance Group 3/4</b>: keep the cross-cutting groups or drop them", "“The current feeling is… a main group and a subgroup but not other groups… something Richard needs to make a call on” (00:09:35–00:09:54). It changes the data model and the dashboard groupings.", "Richard", "Schema freeze", "P-04, G-08"],
    ["D-03", "<b>Onboarding in scope?</b>", "“We no longer do [it] routinely… Richard might decide we should be using it” (00:09:00). It decides whether Manage Onboarding and about 24 checklist items are built.", "Richard", "Scope", "P-04, S-02"],
    ["D-04", "<b>Correct values for Testy Tester-style entries</b>: VAS Mentor/CPD and Surgical Reflective Review, Core or Non Core?", "Spoken “not core” but saved as Core (" + sref("reqA") + "). Confirms which source wins and whether existing people have the same error.", "Operator + Richard", "DM-03, T-02", "SV-01/02"],
    ["D-05", "<b>Role templates</b>: which types apply to each role", "Today the operator picks 22 types from memory for each person (00:14:50–00:17:53). Templates remove that variation.", "Clinical lead + Richard", "FR-04", "P-08"],
    ["D-06", "<b>Meaning of Managed By</b> (contracting organisation or line manager?)", "A freelance contractor “not managed by anybody” was set to Provide Wellbeing to clear a 0 (00:05:45 against 00:19:00).", "Richard", "FR-01", "SV-04"],
    ["D-07", "<b>Named approver(s)</b> for the four-eyes review and publish", "Today one person edits and publishes with no second check.", "Richard", "FR-13", "P-09"],
    ["D-08", "<b>Information governance</b>: DPIA, lawful basis, retention for DBS, indemnity and appraisal evidence; who may see contact details", "The system will store staff personal data and evidence files centrally (" + sref("nm2") + ").", "IG lead / DPO", "Before any real data is loaded", "P-10"],
    ["D-09", "<b>Test data in production</b>: delete or keep Testy Tester’s 22 requirement rows and 8 store records", "They were left in the live files, hidden only by Active = FALSE (FM-16).", "Operator", "DM-05", "FM-16"],
    ["D-10", "<b>Technology constraints</b>: hosting (Azure tenant?), approved database, BI tool, budget owner", "The recommended defaults in spec §7.4 assume the Microsoft 365 estate seen in the recording; the organisation must confirm what is allowed.", "IT / budget holder", "Phase 1", "§7.4"],
    ["D-11", "<b>Success measures</b> for go-live (e.g. parity within agreed tolerance, Excel retired)", "Needed to sign off the parallel run (spec T-03, phase 4).", "Richard", "Go-live", "§7.8"],
]
