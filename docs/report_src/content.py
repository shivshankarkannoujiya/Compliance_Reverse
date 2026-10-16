# -*- coding: utf-8 -*-
import html


def M(t):
    """Monospace inline (escaped)."""
    return '<font name="DVM" size="6.8">%s</font>' % html.escape(t)


def E(t):
    return html.escape(t)


WB = "Staff Management.xlsm"
CD = "Compliance Data.xlsm"

TITLE_BLOCK = [
    ["<b>Document</b>", "Technical Specification — reverse-engineered legacy workflow (as-is) and target architecture (to-be)"],
    ["<b>Subject workflow</b>", "Monthly update of the <b>Staff Management</b> area of the Compliance Dashboard data store, via the Excel “user input tool” "
     "<i>Staff Management.xlsm</i> (VBA + cross-workbook XLOOKUPs) feeding <i>Compliance Data.xlsm</i> (Power Query)"],
    ["<b>Primary evidence</b>", "Microsoft Teams meeting-20260811_131142-Meeting Recording (1).mp4 — 1920×1080, 16 fps, 30:54 (1,854 s); "
     "operator: Andrew Biggins (Provide Wellbeing); audience: Dheeraj"],
    ["<b>Secondary evidence</b>", "…131142…(1).txt (TurboScribe transcript, untimed, cut at 30 min); "
     "…20260811 135933…(1).srt (<b>different meeting</b> — see §0.2)"],
    ["<b>Timestamps</b>", "All [HH:MM:SS] values are positions in the .mp4, re-derived by the author with an offline Whisper (small.en/base.en) "
     "transcription and frame-accurate seeks; every figure was extracted with ffmpeg at the stated second"],
    ["<b>Report date</b>", "16 October 2026"],
    ["<b>Status</b>", "Draft for business-owner review. Items in §6 and prerequisites in §7.1 must be confirmed before build starts"],
]

EXEC_SUMMARY_INTRO = ("<b>What the recording shows.</b> A single operator demonstrates, end-to-end, how a new person "
                      "(“Testy Tester”) is onboarded into the staff-compliance data store and how compliance evidence is recorded, "
                      "amended, refreshed into the dashboard model and finally rolled back. The workflow is <i>semi-automated</i>: "
                      "eight worksheet tabs and four VBA buttons in one workbook read from, and write to, a second workbook "
                      "through structured-table XLOOKUPs and Power Query.")

EXEC_SUMMARY = [
    "<b>Two workbooks, one network share.</b> <i>Staff Management.xlsm</i> (saved to <font name='DVM'>Z:\\Performance Dashboards and Data\\User input\\</font>) "
    "is the input tool; <i>Compliance Data.xlsm</i> holds <font name='DVM'>compliance_Data_Store_Table</font> and the Power Query model the dashboard reads.",
    "<b>Three-stage data entry:</b> (1) register the person on <i>Names</i>; (2) declare which of 22 compliance types apply on "
    "<i>Manage Requirements</i> → appended to <font name='DVM'>requirements_Table</font>; (3) log evidence (date, status, RAG, notes) "
    "on <i>Manage Compliance</i> → written to the external data store, with due date = completion date + “Every x months”.",
    "<b>Composite keys are string concatenations</b> (<font name='DVM'>Name &amp; \"-\" &amp; Compliance Type</font>), so a rename or a stray space silently breaks "
    "every lookup. There are no surrogate keys, no record IDs and no history version numbers.",
    "<b>Seven defects or fragilities are visible on screen</b>, including: a VBA run-time error 13 on close (29:17); a non-working "
    "“last updated” macro; Managed By resolving to <font name='DVM'>0</font> until a manual fix; a metric that counts onboarding rows "
    "against a 22-type denominator (23/22, 45/22); a Roles table whose header row is a data value; a stale Role field; and "
    "an entered “Core” flag that contradicts what the operator said for two compliance types.",
    "<b>The provided .srt does not belong to this video</b> (it covers an <i>Incidents</i>/Datix workflow from a different meeting). "
    "Elements requested in the brief that come from that workflow — Datix CSV pastes, <font name='DVM'>#REF!</font>/<font name='DVM'>#N/A</font> fixes, "
    "“Copy Data” flags — do <b>not</b> occur in this recording. This report documents what is actually on screen and flags the mismatch (§0.2, §6).",
    "<b>Build requirements (§7):</b> 11 business prerequisites, 20 functional and 10 non-functional requirements, technology, migration, testing, roles "
    "and phasing. Each one states why it is required and points to the evidence, and §7.9 traces every observed problem to the requirement that removes it.",
    "<b>Target design (§5):</b> a staged-ingest, relational model with surrogate keys, immutable versioned reference data, "
    "an append-only compliance-event ledger with derived current-state views, a review gate, and atomic publication "
    "batches replacing the save → refresh → save → refresh choreography.",
]

# --------------------------------------------------------------------------------------------
def section0(c):
    para, H, table, bullets, figure = c["para"], c["H"], c["table"], c["bullets"], c["figure"]
    s = [H("0. Evidence Base, Method &amp; Reading Guide", 0)]
    s += [H("0.1 Source artefacts", 1), table([
        ["Artefact", "What it is", "Used for"],
        ["…20260811_131142-Meeting Recording (1).mp4", "Teams screen recording, 1920×1080, 16 fps, 30:54. Git-LFS object, 130 MB", "Primary evidence: all screenshots, all step timings"],
        ["…20260811_131142-Meeting Recording (1).txt", "TurboScribe transcript of the <b>same</b> meeting; no timestamps; stops at ~30:00 (free-tier cap)", "Wording cross-check of spoken business rules"],
        ["…20260811 135933-Meeting Recording (1).srt", "Timed subtitles from a <b>different</b> meeting (13:59:33, ~7 min, Incidents tool)", "Not used for anchoring (see §0.2)"],
        ["Author-generated ASR (Whisper small.en / base.en, VAD-segmented)", "Re-transcription of the .mp4 audio with start/end per utterance", "Timestamp anchors for every step"],
    ], [52, 78, 50])]
    s += [H("0.2 Critical finding: the .srt describes another workflow", 1),
          para("The .srt opens with “Hi Dheeraj, it’s me again. So I’m going to make a video now to show how we update the compliance for "
               "<b>incidents</b>…” and goes on to describe downloading from <b>Datix</b>, pasting the export, a category-grouping lookup column "
               "and a “hashtag REF” error (srt cues 75–98, 00:04:43–00:06:56). None of this appears in the .mp4, which covers <b>Staff "
               "Management</b> and never shows Datix, a CSV export, a paste of raw rows or a #REF! error. The file names confirm it: "
               "the .mp4 and .txt are <font name='DVM'>…131142…</font>, the .srt is <font name='DVM'>…135933…</font> (about 48 minutes later).", "callout"),
          para("<b>Consequence:</b> timing cannot be taken from the .srt. All timestamps were rebuilt from the video’s own audio track "
               "(offline Whisper; the Hugging Face model host was blocked, so ONNX exports from GitHub were used) and checked against "
               "visible screen changes. The Incidents workflow needs its own recording and its own specification (Gap G-01).")]
    s += [H("0.3 Timestamp & screenshot method", 1)] + bullets([
        "Frames were pulled with <font name='DVM'>ffmpeg -ss &lt;t&gt; -frames:v 1</font> at full 1920×1080 resolution, then cropped to the Excel "
        "window (1675×895) or the formula bar (1675×410) so headers and formulas stay legible on A4.",
        "Calibration: a 1/5 s <font name='DVM'>fps</font>-filter sweep sat about 2.5–5 s <i>later</i> than its nominal label. All "
        "figures were therefore re-seeked and verified frame by frame. Where a transient UI element (dropdown, taskbar preview) lasted under "
        "a second, the exact frame was found by image-difference search at 4 fps and 0.2 s steps.",
        "Readability gate: every figure was checked for (a) edge-energy sharpness and (b) stability against a frame 0.5 s later, so "
        "no figure catches a screen redraw, then inspected visually. " + c["figref"]("rec") + " (camera) and " + c["figref"]("tb") + " (a 0.3 s taskbar hover) are "
        "deliberately transient. Figures are numbered in video-time order; a figure is embedded once, and later mentions point back to it.",
        "Caption format: <b>Figure N [HH:MM:SS] — File › Tab: content / change</b>. “BEFORE”/“AFTER” pairs bracket each macro or edit.",
    ])
    s += [H("0.4 Conventions", 1)] + bullets([
        "<b>Table names</b> appear exactly as they do in formulas: <font name='DVM'>name_Table</font>, <font name='DVM'>requirements_Table</font>, "
        "<font name='DVM'>Compliance_Timeframe_Table</font>, <font name='DVM'>compliance_Data_Store_Table</font>.",
        "<b>Confidence tags</b> on inferred facts: <b>[Seen]</b> read directly on screen; <b>[Said]</b> stated by the operator; "
        "<b>[Inferred]</b> deduced from behaviour; <b>[Unknown]</b> not determinable, so logged in §6.",
    ])
    s.append(c["PageBreak"]())
    return s


# --------------------------------------------------------------------------------------------
def section1(c):
    para, H, table, bullets, figure, figref = c["para"], c["H"], c["table"], c["bullets"], c["figure"], c["figref"]
    s = [H("1. Complete File, Workbook &amp; Sheet Inventory", 0)]
    s += [H("1.1 Files and external systems", 1), table([
        ["#", "File / system", "Format", "Location (as seen)", "Role", "Evidence"],
        ["F1", "<b>Staff Management.xlsm</b>", ".xlsm (macro-enabled; AutoSave Off; “Saved to this PC”)",
         "<font name='DVM'>Z:\\Performance Dashboards and Data\\User input\\Staff Management.xlsm</font>",
         "User-input tool: master lists, requirement set-up, compliance entry UI; hosts the VBA buttons", figref("reqS") + ", " + figref("nmY") + ", " + figref("sv")],
        ["F2", "<b>Compliance Data.xlsm</b>", ".xlsm", "Not shown; open in a second Excel window (taskbar preview). Same share assumed [Inferred]",
         "The “data store”: holds <font name='DVM'>compliance_Data_Store_Table</font>; Power Query builds requirements/timeframe tables from every user-input tool; feeds the dashboard",
         figref("mcV") + ", " + figref("tb")],
        ["F3", "Other “user input tools” (e.g. <i>Estates</i>, <i>Medical Devices</i>)", ".xlsm [Said]", "Not shown",
         "Sibling tools with the same Names/Requirements/Timeframes pattern; Power Query pulls them all", "Said 00:03:22, 00:27:02"],
        ["S1", "Compliance Dashboard", "BI front-end (product not named; gauge visuals, “Active = TRUE” filter)", "Not shown",
         "Consumer of the Power Query model; uses Threshold 1–5 for gauge colouring", "Said 00:04:27, 00:10:30"],
        ["S2", "GMC register", "Website", "—", "Source of Professional Registration evidence (“downloaded from the GMC today”)", "Said 00:20:58"],
        ["S3", "VPN", "Network", "—", "Refresh is slow remotely (“five or six seconds in the office”)", "Said 00:27:19"],
    ], [7, 30, 24, 40, 50, 29])]

    s += [H("1.2 Worksheet tabs in Staff Management.xlsm", 1),
          para("Tab order as shown on the tab bar (" + figref("mc0") + ", " + figref("rol") + "): <b>Instructions · Names · Manage Requirements · "
               "Manage Onboarding · Manage Compliance · Roles · Compliance Timeframes · Requirements</b>. Tab colours: light blue = UI/master data, "
               "green = reference, purple = generated table."),
          table([
              ["Tab", "Architectural role", "Key objects", "Read / written by", "Shown at"],
              ["Instructions", "Documentation", "—", "Not opened", "Tab bar only [Gap G-12]"],
              ["Names", "<b>Master data</b> (entity register: one row per person)", "<font name='DVM'>name_Table</font> (A:Q, ~140 rows)",
               "Manual entry; read by Requirements!G, J and by the Manage* dropdowns", "02:58–07:03, 19:03, 28:53"],
              ["Manage Requirements", "<b>Staging / data-entry UI</b> for requirement set-up",
               "Named cell <font name='DVM'>add_Requirements_Name</font> (D6); Add grid C10:F32; Update panel I10:L32; helper cols M:T; buttons <i>Add Requirements</i>, <i>List Missing</i>, <i>Update Requirements</i>",
               "VBA writes to <font name='DVM'>requirements_Table</font>", "13:23–18:04"],
              ["Manage Onboarding", "Staging UI for onboarding checklist (parallel to Manage Compliance)", "Not opened", "[Unknown]", "Tab bar only [Gap G-12]"],
              ["Manage Compliance", "<b>Staging / data-entry UI</b> for compliance evidence",
               "Add grid B8:O…; named cell <font name='DVM'>update_Co…</font> (R5, name truncated); Existing panel R:W (cross-workbook lookups); Update panel X:AC; buttons <i>Add New Compliance</i>, <i>Update Existing Compliance</i>",
               "VBA writes to <font name='DVM'>Compliance Data.xlsm!compliance_Data_Store_Table</font>", "00:53, 20:13–26:03, 29:23"],
              ["Roles", "Reference / lookup", "Unnamed table A1:B22 (Role → Clinical/Non-clinical)", "Use unknown (“I’m not sure this is actually used”)", "12:23"],
              ["Compliance Timeframes", "<b>Reference</b> (compliance-type catalogue, frequencies, grouping, thresholds)",
               "<font name='DVM'>Compliance_Timeframe_Table</font> (A:O); side lists Q (named <font name='DVM'>Compliance_Type</font> [Inferred]) and S (Onboarding)",
               "Manual; read by Requirements!I, Names!P, Manage Compliance (Time Frame), Power Query", "07:33–12:09"],
              ["Requirements", "<b>Generated master table</b>: person × compliance-type applicability",
               "<font name='DVM'>requirements_Table</font> (A:J, ~2,320 rows)", "Appended by VBA <i>Add Requirements</i>; read by Power Query, Names!O, CT!J, Manage Requirements", "12:53, 18:33–19:53"],
          ], [25, 33, 52, 42, 28])]
    s += [H("1.3 Cross-workbook links, Power Query and VBA", 1), table([
        ["Mechanism", "Trigger", "Behaviour observed", "Evidence"],
        ["XLOOKUP into <font name='DVM'>'Compliance Data.xlsm'!compliance_Data_Store_Table</font>", "Recalculation (needs F2 open)",
         "Existing panel R:W on Manage Compliance shows the stored record for <i>Name-Type</i> keys (via <font name='DVM'>[Unique Lookup 3]</font>)",
         figref("mcV")],
        ["Power Query (in F2)", "Data › Refresh All (twice, with saves between) [Said]",
         "Builds the requirements and compliance-timeframe tables from every <i>saved</i> user-input tool; status bar “Running background query… (Click here to cancel)”",
         figref("rf1") + "; 27:27–28:35 and from 29:20"],
        ["VBA <i>List Missing</i>", "Button, Manage Requirements", "Lists the compliance types with no requirement row for the selected name", figref("mrL")],
        ["VBA <i>Add Requirements</i>", "Button", "Appends one <font name='DVM'>requirements_Table</font> row per filled grid line", figref("reqA")],
        ["VBA <i>Update Requirements</i>", "Button", "Overwrites existing requirement rows (not exercised) [Said 13:50]", figref("mrT")],
        ["VBA <i>Add New Compliance</i>", "Button, Manage Compliance", "Appends rows to the external data store; clears the grid. “Doesn’t like it if you miss a row” [Said 20:45]", figref("mcA")],
        ["VBA <i>Update Existing Compliance</i>", "Button", "Overwrites the matching stored record in place (no history); supports a Delete flag (AC)", figref("mcU2")],
        ["VBA close / last-updated prompt", "Workbook close", "Should ask “update the last updated date?”; instead throws <b>Run-time error 13: Type mismatch</b>", figref("vba")],
        ["Auto refresh on close", "Closing F1 while F2 is open [Said 29:29]", "Power Query restarts; lookups “can corrupt” if F2 closes first, so the operator does not save at this point", figref("sv")],
    ], [42, 32, 76, 30])]
    s += [H("1.4 Overview screenshots", 1), figure("mc0"), figure("rol", 95 * c["mm"]), figure("tb", 100 * c["mm"])]
    s.append(c["PageBreak"]())
    return s


# --------------------------------------------------------------------------------------------
def section2(c):
    para, H, table, bullets, figure, figref, code = c["para"], c["H"], c["table"], c["bullets"], c["figure"], c["figref"], c["code"]
    mm = c["mm"]
    W = [9, 30, 25, 18, 98]
    hdr = ["Col", "Header", "Type / format", "Origin", "Lineage, rule and evidence"]
    s = [H("2. Exhaustive Column-Level Schema &amp; Data Lineage Catalogue", 0),
         para("Origin codes: <b>RAW</b> = typed or selected by the operator from an external fact (no upstream system feed exists in this workflow); "
              "<b>CALC</b> = Excel formula; <b>VBA</b> = written by a macro; <b>REF</b> = maintained reference value; <b>PQ</b> = Power Query output.")]

    # Names
    s += [H("2.1 Staff Management.xlsm › Names (name_Table)", 1), table([hdr,
        ["A", "Name", "Text, free", "RAW · key", "Natural key used by every lookup (no ID). New rows are appended at the bottom (Testy Tester row 140 after Zoe Porter, so the list is no longer alphabetical). "
         "Spelling must match exactly across workbooks. " + figref("nmB")],
        ["B", "Managed By", "Text, dropdown (Provide Wellbeing / Provide CIC / Workforce Solutions)", "RAW", "Feeds <font name='DVM'>requirements_Table[Managed By]</font>. Left blank for the new starter, so Requirements showed <b>0</b> until fixed at 19:03. " + figref("nmMB")],
        ["C", "Employment Type", "Text, list (Substantive / Contractor / Third Party Contract)", "RAW", "Informational [Said 04:09]"],
        ["D", "Role", "Text, list (GPwSI, Nurse, OSALT, BSO, Med Sec, Paed Cons, …)", "RAW", "Informational; values match <i>Roles</i>!A (relationship not enforced)"],
        ["E", "Works with", "Text (Adult / Children / Both / Adults)", "RAW", "Informational. Note “Adult” vs “Adults”: uncontrolled vocabulary. " + figref("nm2")],
        ["F", "Tel Num", "Text", "RAW", "Informational, mixed formats"],
        ["G", "Email", "Text", "RAW", "Informational; some cells hold several addresses or “NAME (PROVIDE) &lt;email&gt;” strings"],
        ["H", "Contract", "Text (e.g. Permanent)", "RAW", "Seen at 28:53 only (" + figref("nmX") + "); sparsely populated"],
        ["I", "WTE", "Number", "RAW", "Whole-time equivalent; sparse"],
        ["J", "Start Date", "Date", "RAW", "Typed for Testy Tester as 1 Aug; displays <b>8/1/2026</b> (m/d) while other rows show dd/mm/yyyy, so the format is inconsistent [Gap G-09]. Not used by any visible formula"],
        ["K", "SystmOne Name", "Text", "RAW", "Alias in the clinical system (e.g. “Dr Ashraf Ali”). Informational"],
        ["L", "PD Name", "Text", "RAW", "Alias in “PD” (an unnamed system). Informational"],
        ["M", "PD Login Email", "Text", "RAW", "Informational"],
        ["N", "Active", "Boolean TRUE/FALSE", "RAW · <b>essential</b>", "Dashboard filter: only Active = TRUE people are shown [Said 04:16]. Propagated to <font name='DVM'>requirements_Table[Active]</font>. Set FALSE at 29:01 to retire the test record. " + figref("nm3")],
        ["O", "Compliance Types Added to Record", "Integer", "CALC", "<font name='DVM'>=COUNTIFS(requirements_Table[Name],[@Name])</font>. Counts <i>all</i> requirement rows, onboarding ones included, so values of 23 and 45 appear against a denominator of 22. " + figref("nmO")],
        ["P", "Total Compliance Types", "Integer (22)", "CALC", "<font name='DVM'>=COUNTIFS(Compliance_Type,\"&lt;&gt;\")</font>: non-blank count of the 22-item list on Compliance Timeframes!Q. " + figref("nmP")],
        ["Q", "Name if Active", "Text", "CALC", "<font name='DVM'>=IF([@Active]=TRUE,[@Name],\"\")</font>: probably the source of the active-name dropdowns [Inferred]. Operator: “wasn’t actually needed… ignore that” [Said 05:14]. " + figref("nmQ")],
    ], W)]
    s += [figure("nm1"), figure("nm2"), figure("nm3"), figure("nmO", 50 * mm), figure("nmP", 50 * mm), figure("nmQ", 50 * mm)]

    # Compliance Timeframes
    s += [H("2.2 Staff Management.xlsm › Compliance Timeframes (Compliance_Timeframe_Table)", 1), table([hdr,
        ["A", "Compliance Type", "Text · key", "REF", "Catalogue key: 22 staff types (rows 2–22) plus onboarding items (rows 23→, “Onboarding begun”, “ID supplied”, “Laptop”, …)"],
        ["B", "Every x months", "Integer", "REF", "Review frequency: 6, 12, 24, 36, 60. <b>10000</b> = “never expires” sentinel for onboarding. Drives the due date (completion + B months) and <font name='DVM'>requirements_Table[Compliance Timeframe]</font>"],
        ["C", "Core Requirement", "Text (Core / blank)", "REF", "Catalogue-level default. Operator disputes the values (accreditation and performance review “should be core”) [Said 08:32]. The per-person value on Requirements!D overrides it"],
        ["D", "Compliance Group 1", "Text (People / Operational / Clinical)", "REF", "Top-level dashboard grouping; all staff types = People"],
        ["E", "Compliance Group 2", "Text (Staff Requirements / Accreditation Prep / Onboarding)", "REF", "Sub-group. “Accreditation Prep” was a proposed change [Said 08:06]"],
        ["F", "Compliance Group 3", "Text (Fitness to Practice / Safeguarding / blank)", "REF", "Cross-cutting grouping (e.g. PI insurance also affects the Clinical score). Future of groups 3–4 is for Richard to decide [Said 09:17–09:54]"],
        ["G", "Compliance Group 4", "Text (Clinical / blank)", "REF", "As F"],
        ["H", "Unique Lookup", "Text", "CALC", "<font name='DVM'>Group 1 &amp; \"-\" &amp; Group 2</font>, e.g. “People-Staff Requirements” [Inferred from values; formula not shown]. Pulled into PQ tables [Said 10:06]"],
        ["I", "Unique Lookup 2", "Text", "CALC", "<font name='DVM'>=IF(CONCAT([@[Compliance Group 4]],\"-\",[@[Compliance Group 3]])=\"-\",\"\",CONCAT(…))</font>, e.g. “Clinical-Fitness to Practice”. " + figref("ctI")],
        ["J", "Missing", "Boolean", "CALC", "<font name='DVM'>=XLOOKUP(CONCAT(add_Requirements_Name,\"-\",[@[Compliance Type]]),requirements_Table[Unique Lookup],requirements_Table[Unique Lookup],\"\")=\"\"</font>: TRUE if the person <i>currently selected</i> on Manage Requirements lacks this type. UI-state-dependent; probably what <i>List Missing</i> reads [Inferred]. " + figref("ctJ")],
        ["K–O", "Threshold 1 … Threshold 5", "Decimal 0–1", "REF", "Gauge colour bands: 1 / 0.9 / 0.8 / 0.7 / 0.6 (DBS rows 1 / 0.98 / 0.9 / 0.8 / 0.7). ≥0.9 green, &lt;0.6 red, graded between [Said 10:40]. Blank for onboarding rows"],
        ["P", "(blank spacer)", "—", "—", "—"],
        ["Q", "Compliance Type (list)", "Text, 22 items", "REF", "Stand-alone list PI Insurance … <b>IR35 Compliant</b>. Probably the named range <font name='DVM'>Compliance_Type</font> used by Names!P [Inferred]. IR35 Compliant is in this list but not in table rows 2–22 [Gap G-05]"],
        ["S", "Onboarding (list)", "Text, ~24 items", "REF", "Onboarding checklist items (Onboarding begun … Prescribing)"],
    ], W)]
    s += [figure("ct1"), figure("ct2"), figure("ctI", 50 * mm), figure("ctJ", 50 * mm), figure("ct3")]

    # Roles
    s += [H("2.3 Staff Management.xlsm › Roles", 1), table([hdr,
        ["A", "“Reception” (header)", "Text", "REF", "Role code list: GPwSI, HCA, PSCH, OSALT, Nurse, Paed Cons, Data/Comp, Med Sec, Vas Assessment, GM, OT, BSO, Physio, BSO/HCA, ADHD Specialist, Audio, Head Nurse, DGM, MD, OD, Podiatry. "
         "<b>Defect:</b> the header cell holds the data value “Reception”, so that role has been lost to the header [Seen]"],
        ["B", "“Non-clinical” (header)", "Text (Clinical / Non-clinical)", "REF", "Classification. Header is again a data value"],
    ], W), para("See " + figref("rol") + " in §1.4.")]

    # Requirements
    s += [H("2.4 Staff Management.xlsm › Requirements (requirements_Table)", 1), table([hdr,
        ["A", "Name", "Text", "VBA", "From Manage Requirements D6 (<font name='DVM'>add_Requirements_Name</font>). " + figref("reqA")],
        ["B", "Compliance Type", "Text", "VBA", "From the grid, column C"],
        ["C", "Required (T/F)", "Boolean", "VBA (operator choice)", "Whether the type applies to the person"],
        ["D", "Core Requirement", "Text (Core / Non Core / blank)", "VBA (operator choice)", "Person-level core flag; overrides the catalogue default"],
        ["E", "Notes", "Text", "VBA", "Grid column F; blank in demo"],
        ["F", "Onboarding", "Boolean", "VBA / default", "FALSE for staff types, TRUE for onboarding items (e.g. Shahzad Aslam rows 2102–2119). Operator doubts it is used [Said 18:39]"],
        ["G", "Managed By", "Text", "CALC", "<font name='DVM'>=XLOOKUP([@Name],name_Table[Name],name_Table[Managed By],\"\")</font>. Returns <b>0</b> (not blank) when the source is empty. " + figref("reqG")],
        ["H", "Unique Lookup", "Text · composite key", "CALC", "<font name='DVM'>=CONCAT([@Name],\"-\",[@[Compliance Type]])</font>, e.g. “Testy Tester-PI Insurance”. Key for Manage Requirements and CT!J. Uniqueness not enforced"],
        ["I", "Compliance Timeframe", "Integer months", "CALC", "<font name='DVM'>=XLOOKUP([@[Compliance Type]],Compliance_Timeframe_Table[Compliance Type],Compliance_Timeframe_Table[Every x months],\"\")</font>. " + figref("reqI")],
        ["J", "Active", "Boolean", "CALC", "<font name='DVM'>=XLOOKUP([@Name],name_Table[Name],name_Table[Active],\"\")</font>, so deactivating a person cascades to all their rows. " + figref("reqS")],
    ], W)]
    s += [figure("req0"), figure("reqG", 50 * mm), figure("reqI", 50 * mm)]

    # Manage Requirements
    s += [H("2.5 Staff Management.xlsm › Manage Requirements (entry form)", 1), table([hdr,
        ["D6", "Name (<font name='DVM'>add_Requirements_Name</font>)", "Text, dropdown of names", "RAW", "Drives CT!J “Missing” and the Update panel. " + figref("mr0")],
        ["D8", "Role", "Text", "CALC? [Unknown]", "Showed “Surgical Clinician – NHS Only” for the previous person <b>and</b> for Testy Tester (whose Role is GPwSI), so it is stale or unrelated. Operator: “I don’t think it actually uses this” [Said 15:05]"],
        ["C11:C32", "Compliance Type", "Text", "VBA (List Missing)", "Populated by List Missing (" + figref("mrL") + ")"],
        ["D11:D32", "Required", "Boolean dropdown", "RAW", "TRUE/FALSE per type (" + figref("mrD") + ")"],
        ["E11:E32", "Requirement", "Core / Non Core dropdown", "RAW", "Core flag"],
        ["F11:F32", "Notes", "Text", "RAW", "Blank in demo"],
        ["J6", "Name (update panel)", "Text", "CALC", "Mirrors D6 (shows Testy Tester)"],
        ["I11:I…", "Compliance Type (update)", "Text", "CALC", "Full type list for the update panel"],
        ["J11", "Required (existing)", "Boolean", "CALC", "<font name='DVM'>=IF(I11&lt;&gt;\"\",XLOOKUP(CONCAT($J$6,\"-\",I11),requirements_Table[Unique Lookup],requirements_Table[Required (T/F)],\"\"),\"\")</font>"],
        ["K11", "Requirement (existing)", "Text", "CALC", "<font name='DVM'>=IF(I11&lt;&gt;\"\",IF(XLOOKUP(CONCAT($J$6,\"-\",I11),…,requirements_Table[Core Requirement],\"\")&lt;&gt;0,XLOOKUP(…),\"\"),\"\")</font>: suppresses 0 from blank sources. " + figref("mrB")],
        ["L11", "Notes (existing)", "Text", "CALC", "Same pattern on [Notes] [Inferred]"],
        ["M:O", "Required / Core Requirement / Notes (new values)", "Mixed", "RAW", "Operator types replacement values here for <i>Update Requirements</i>"],
        ["P:Q…T", "Site / Compliance Type / … / helper", "Text", "CALC", "“Originally hidden” helper columns for the macro [Said 13:56]. T11: <font name='DVM'>=IF(I11&lt;&gt;\"\",IF(O11&lt;&gt;\"\",O11,IF(L11&lt;&gt;\"\",L11,\"\")),\"\")</font> = coalesce(new, existing). " + figref("mrT") + ". Header “Site” shows the form was cloned from the Estates tool"],
    ], [13, 33, 24, 18, 92])]
    s += [figure("mrT", 50 * mm)]

    # Manage Compliance
    s += [H("2.6 Staff Management.xlsm › Manage Compliance (entry form)", 1), table([hdr,
        ["B", "Name", "Text, dropdown/autocomplete", "RAW", "Per row (allows several people in one batch)"],
        ["C", "Compliance Type", "Text, dropdown", "RAW", "Per row"],
        ["D", "Completion Date", "Date dd/mm/yyyy", "RAW", "Date the evidence was seen or the activity done (e.g. GMC check “today” = 11/08/2026)"],
        ["E", "Completion Status", "List: Completed / Sign-off Required / Scheduled", "RAW", figref("mc3")],
        ["F", "RAG Rating", "List: Green / Amber / Red (cell fill follows)", "RAW", "Chosen by hand, not derived from dates [Seen]"],
        ["G", "Notes", "Text", "RAW", "“Certificate on file”, “Copy on file”"],
        ["H–N", "(hidden)", "—", "—", "Columns H–N are hidden (letters jump G→O) [Gap G-10]"],
        ["O", "Time Frame (Months)", "Integer", "CALC", "Fills as soon as C is set (12, 24, 60…), so it is a lookup on <font name='DVM'>Compliance_Timeframe_Table[Every x months]</font> [Inferred]. " + figref("mcS")],
        ["R5", "Name (<font name='DVM'>update_Co…</font>)", "Text", "RAW", "Selects the person whose stored records are shown. " + figref("mc1")],
        ["R9:R…", "Compliance Type", "Text", "CALC", "Rows filled for the selected person (pink until a record exists)"],
        ["S", "Completion Date (stored)", "Date", "CALC (x-wb)", "XLOOKUP into the data store, key <font name='DVM'>R5&amp;\"-\"&amp;R</font> [Inferred, same pattern as V]"],
        ["T", "Completion Status (stored)", "Text", "CALC (x-wb)", "As S"],
        ["U", "RAG Rating (stored)", "Text", "CALC (x-wb)", "As S; conditional fill"],
        ["V", "Notes (stored)", "Text", "CALC (x-wb)", "<font name='DVM'>=IF(XLOOKUP(CONCAT($R$5,\"-\",R9),'Compliance Data.xlsm'!compliance_Data_Store_Table[Unique Lookup 3],'Compliance Data.xlsm'!compliance_Data_Store_Table[Compliance Notes],\"\")&lt;&gt;0, XLOOKUP(…),\"\")</font>. " + figref("mcV")],
        ["W", "Due Date (stored)", "Date", "CALC (x-wb)", "Completion + Time Frame months (01/06/2026 → 01/06/2027). Whether it is stored or derived is [Unknown]"],
        ["X", "Completion Date (new)", "Date", "RAW", "Amendment value (01/05/2026). " + figref("mcU")],
        ["Y", "Completion Status (new)", "Text", "RAW", "Blank = keep existing [Inferred from T-column pattern]"],
        ["Z", "RAG Rating (new)", "Text", "RAW", "As Y"],
        ["AA", "Notes (new)", "Text", "RAW", "As Y"],
        ["AB", "Due Date (new)", "Date", "<b>RAW</b>", "<b>Typed by hand</b> (“1/5/27”) on the update path, so it is not computed: a due-date/timeframe mismatch is possible. Spoken: “the due date’s gonna have to change” [Said 24:52]"],
        ["AC", "Delete", "Flag", "RAW", "Marks a stored record for deletion [Said 24:59]; value format [Unknown]"],
    ], W)]

    # Compliance Data store
    s += [H("2.7 Compliance Data.xlsm › compliance_Data_Store_Table (external, partially visible)", 1),
          para("Only the column names used in formulas, and the destination of the VBA writes, are visible. Inferred schema:"),
          table([hdr,
                 ["?", "Name", "Text", "VBA", "From Manage Compliance B [Inferred]"],
                 ["?", "Compliance Type", "Text", "VBA", "From C"],
                 ["?", "Completion Date / Status / RAG / Due Date", "Date / Text / Text / Date", "VBA", "From D/E/F and the computed due date; overwritten in place by <i>Update</i>"],
                 ["?", "Compliance Notes", "Text", "VBA", "Seen in V9 formula"],
                 ["?", "Unique Lookup 3", "Text · key", "CALC/VBA", "Seen in V9 formula; evidently Name &amp; \"-\" &amp; Compliance Type. “Unique” fails once history accumulates (“build up a picture over time”, 25:08), and XLOOKUP returns only the <i>first</i> match [Gap G-04]"],
                 ["?", "(Unique Lookup list with 024/025/026 prefixes)", "Text", "PQ? [Unknown]", "Glimpsed in the taskbar preview of F2: values such as “026 Clinical-Audit”, “024 People/Workforce-Employment Requirements”. Possibly a group code + Unique Lookup [Gap G-06]. " + figref("tb")],
                 ["PQ", "Requirements / Timeframes (built)", "Tables", "PQ", "Built from the saved Requirements and Compliance Timeframes tabs of every tool [Said 11:21, 27:02]. Operator says “there we go” at 11:50 but the window shown is still Staff Management, so the PQ table was not visible to the viewer [Gap G-02]"],
          ], W)]
    s.append(c["PageBreak"]())
    return s


# --------------------------------------------------------------------------------------------
STEPS = [
    # (n, start, end, title, action, mapping, mutation, figs)
    (1, "00:00:00", "00:00:56", "Start recording and share the correct screen",
     "Operator on camera, then switches off the camera and starts a screen share; first attempt shares the wrong screen and is re-done (00:33–00:48).",
     "—", "No data change.", ["rec"]),
    (2, "00:00:56", "00:02:34", "Introduce the user-input tool; clear a prior attempt",
     "Workbook Staff Management.xlsm is open on <i>Manage Compliance</i> with a previous person (Emma Lindsley: Enhanced DBS 26/02/2026, Performance Review 08/05/2026) loaded. "
     "Operator says he “want[s] to get rid of something I did on my abortive attempt” (01:50–02:03); no visible change follows.",
     "—", "Possibly a removal of test data from the earlier, unrecorded attempt [Gap G-03].", ["mc0"]),
    (3, "00:02:34", "00:05:28", "Tour the Names tab (master register)",
     "Opens <i>Names</i>; scrolls right across A→Q; selects N (Active) and points at O, P, Q, which displays their formulas.",
     "Read-only.", "None. Calculated O/P/Q explained. Pink banding = Active FALSE rows [Inferred].", ["nm1", "nm2", "nm3", "nmO", "nmP", "nmQ"]),
    (4, "00:05:28", "00:07:11", "Register new person “Testy Tester”",
     "Types into A140 (first blank row of <font name='DVM'>name_Table</font>, so the table auto-extends), then C = Contractor, D = GPwSI, J = 1 Aug 2026, N = TRUE. Leaves B (Managed By) blank on purpose (“freelance… not managed by anybody”).",
     "Manual keyboard entry → <font name='DVM'>name_Table</font> row 140.",
     "BEFORE: row 140 empty. AFTER: A–D, J, N set; O = <b>0</b>, P = <b>22</b>, Q = “Testy Tester” (calculated columns fill automatically).", ["nmB", "nmA"]),
    (5, "00:07:11", "00:11:13", "Review Compliance Timeframes (reference catalogue)",
     "Switches to <i>Compliance Timeframes</i>; selects Group 1 (People), Group 2 (Accreditation Prep block E11:E22), Group 3/4, scrolls to rows 23–42 (onboarding, 10000 months), opens formulas I7 and J2, then selects K–O (thresholds).",
     "Read-only.", "None. Operator voices disagreement with the Core flags and the grouping design (see §4.3).", ["ct1", "ct2", "ctI", "ctJ", "ct3"]),
    (6, "00:11:13", "00:12:09", "Explain Power Query build of timeframe tables",
     "States that on the first refresh the data store builds compliance-timeframe tables from every tool by Power Query, and that the staff-management compliance table is there. Screen stays on Compliance Timeframes.",
     "PQ: Staff Management!Compliance_Timeframe_Table → Compliance Data model.", "None on screen.", []),
    (7, "00:12:09", "00:12:41", "Glance at Roles",
     "Clicks the <i>Roles</i> tab; “I’m not sure this is actually used at all… I don’t think it’s essential”.", "—", "None.", ["rol"]),
    (8, "00:12:41", "00:13:11", "Introduce Requirements (per-person applicability)",
     "Opens <i>Requirements</i> (~2,300 rows; Shahzad Aslam’s block visible, onboarding rows TRUE/Core).", "Read-only.", "None.", ["req0"]),
    (9, "00:13:11", "00:14:16", "Select the new person on Manage Requirements",
     "Opens <i>Manage Requirements</i>; the D6 dropdown now offers Testy Tester (proving name_Table drives it); selects Testy Tester; inspects the Update panel and helper formulas K11 and T11.",
     "<font name='DVM'>add_Requirements_Name</font> ← “Testy Tester”.",
     "BEFORE: D6 = Annamarie Webster, panel J6 = Zoe Porter (stale). AFTER: D6 = J6 = Testy Tester; Update panel pink with blank Required/Requirement, so <b>no existing requirements</b>.", ["mr0", "mrB", "mrT"]),
    (10, "00:14:16", "00:14:50", "Run VBA “List Missing”",
     "Clicks <i>List Missing</i>.",
     "VBA reads the types with no requirement row for D6 (the CT!J logic) → writes them into C11:C32.",
     "BEFORE: grid C11:C32 empty. AFTER: 22 compliance types listed (all of them, as expected for a new person).", ["mrL"]),
    (11, "00:14:50", "00:17:53", "Declare Required / Core for each of the 22 types",
     "Row by row selects Required (TRUE/FALSE) and Requirement (Core/Non Core) from dropdowns, partly by copy-and-paste (status bar “Select destination and press ENTER or choose Paste”).",
     "Manual → D11:E32.",
     "See the table under this step: what the operator said against what was actually entered (two mismatches).", ["mrD", "mrF"]),
    (12, "00:17:53", "00:18:29", "Run VBA “Add Requirements”",
     "Clicks <i>Add Requirements</i>; waits about 15 s.",
     "VBA: grid C/D/E/F + D6 → appends 22 rows to <font name='DVM'>requirements_Table</font> (rows 2299–2320). Values written as values; G–J recalculate.",
     "BEFORE: last row 2298 (Annamarie Webster-IR35 Compliant). AFTER: rows 2299–2320 Testy Tester; G (Managed By) = <b>0</b> for all; I = 12/12/24/24/36/24/12/24/24/12/12/12/6/6/12/6/24/24/24/12/60/12; J = TRUE.", ["reqA", "reqG"]),
    (13, "00:18:29", "00:19:14", "Fix Managed By (manual exception)",
     "Notices Managed By = 0, decides “it will probably actually be Provide Wellbeing for everybody”, goes to <i>Names</i>!B140 and selects Provide Wellbeing.",
     "Manual → name_Table[Managed By] → recalc → requirements_Table[Managed By].",
     "BEFORE: Requirements!G2299:G2320 = 0. AFTER: “Provide Wellbeing”. Names!O140 goes 0 → 22.", ["nmMB", "reqMB"]),
    (14, "00:19:14", "00:20:03", "Inspect H–J and save the workbook",
     "Explains Unique Lookup, Compliance Timeframe and Active; saves (Ctrl+S), because the data store can only build from a <i>saved</i> tool.",
     "File save → Z:\\…\\Staff Management.xlsm.", "Persisted state of name_Table and requirements_Table.", ["reqI", "reqS"]),
    (15, "00:20:03", "00:23:24", "Enter compliance evidence on Manage Compliance",
     "Opens <i>Manage Compliance</i>; types “TEST” in R5 (autocompletes to Testy Tester); fills the Add grid one row per evidence item (Name, Type, Date, Status, RAG, Notes). Leaves non-applicable types out. A stray “test” entry in row 16 is overtyped. Warns that the VBA “doesn’t like it if you miss a row”.",
     "Manual → Add grid B9:G16; O fills automatically.",
     "Rows entered (Completion Date → Time Frame): PI Insurance 01/06/2026 (12) Completed/Green “Certificate on file”; Professional Registration 11/08/2026 (12) “Copy on file”; VAS Accreditation 01/08/2026 (24); "
     "Performance Review 01/08/2026 (12); Enhanced DBS 15/07/2026 (24); Medic Appraisal 01/06/2026 (12); Medic Revalidation 01/03/2025 (60); IR35 Compliant 15/07/2026 (12). All Completed / Green.",
     ["mc1", "mcS", "mc2", "mc3", "mcB"]),
    (16, "00:23:24", "00:24:30", "Run VBA “Add New Compliance”",
     "Clicks <i>Add New Compliance</i>; the grid clears; the Existing panel fills from the external store.",
     "VBA: grid rows → append to <font name='DVM'>'Compliance Data.xlsm'!compliance_Data_Store_Table</font>; R:W re-evaluate by XLOOKUP on Unique Lookup 3.",
     "BEFORE: S:W blank and pink for Testy Tester. AFTER: e.g. PI Insurance 01/06/2026 · Completed · Green · “Certificate on file” · Due <b>01/06/2027</b>; Professional Registration 11/08/2026 → Due 11/08/2027.", ["mcA", "mcV"]),
    (17, "00:24:30", "00:26:18", "Amend an existing record via “Update Existing Compliance”",
     "Scenario: PI insurance actually ran from 1 May, not 1 June. Types X9 = 01/05/2026 and AB9 = 01/05/2027 (due date by hand), then clicks <i>Update Existing Compliance</i> (about 25:47). Mentions the Delete column AC.",
     "VBA: X:AC for the row → overwrite the matching store record in place.",
     "BEFORE: S9 01/06/2026, W9 01/06/2027. AFTER: S9 <b>01/05/2026</b>, W9 <b>01/05/2027</b>; X:AC cleared. The previous value is not kept (no audit trail).", ["mcU", "mcU2"]),
    (18, "00:26:18", "00:28:24", "Explain the monthly cycle and start the data refresh",
     "Describes the monthly loop (update what you can, chase staff, input replies) and the publish sequence <b>save data store → Refresh → save → Refresh → save</b>, plus updating the “last updated” tab by hand because its VBA is broken. Triggers a refresh in Compliance Data.xlsm (status: “Calculating (14 Threads)” 26:20, “Loading .Net Framework” 27:20, “Running background query” 27:27–28:35).",
     "PQ: all saved tools → Compliance Data model tables.",
     "Not visible: the PQ output tables are in the other window.", ["rf1"]),
    (19, "00:28:24", "00:29:13", "Stop the refresh; deactivate the test person; save",
     "“I’m going to stop that… I don’t particularly want to add Testy Tester in any way.” Cancels the query, sets Names!N140 = FALSE, saves.",
     "Manual → name_Table[Active] → requirements_Table[Active].",
     "BEFORE: N140 = TRUE. AFTER: N140 = FALSE (person stays in the store, flagged inactive). The 22 requirement rows and 8 store records are <b>not</b> deleted.", ["nmX", "nmY"]),
    (20, "00:29:13", "00:29:27", "Close the workbook: VBA run-time error",
     "Closes Staff Management; the close macro (“do you want to update the last updated date?”) fails.",
     "—", "<b>Run-time error ‘13’: Type mismatch</b> dialog (Continue disabled; End/Debug/Help). Operator dismisses it.", ["vba"]),
    (21, "00:29:27", "00:29:45", "Decline to save; background refresh restarts",
     "“Save your changes to this file?” → operator chooses <b>Don’t Save</b>, explaining that saving now can corrupt the lookups if Compliance Data closes first, and it re-triggers a data update. Taskbar hover (29:38) shows a second workbook “Comp…” open.",
     "—", "Workbook closed without saving the post-error state; background query running again in Compliance Data.", ["sv", "tb"]),
    (22, "00:29:45", "00:30:54", "Stop screen share and wrap up",
     "Camera tile only. Operator says he will send the video plus a list of compliance areas that use this method, and record the others.", "—", "—", []),
]

REQ_COMPARE = [
    ["Compliance type", "Spoken (timestamp)", "Entered: Required / Core (Requirements row)", "Match?"],
    ["PI Insurance", "Needed, core (15:10)", "TRUE / Core (2299)", "✓"],
    ["Professional Registration", "Core (15:17)", "TRUE / Core (2300)", "✓"],
    ["VAS Accreditation", "Core, every 2 years (15:26)", "TRUE / Core (2301)", "✓"],
    ["CTS / Minor Skin / NDD Accreditation", "Not doing (15:35–15:41)", "FALSE / – (2302–2304)", "✓"],
    ["Performance Review", "Core (15:46)", "TRUE / Core (2305)", "✓"],
    ["Standard DBS", "Not needed, has enhanced (15:46)", "FALSE / – (2306)", "✓"],
    ["Enhanced DBS", "Core (15:46–16:06)", "TRUE / Core (2307)", "✓"],
    ["VAS Mentor Review or CPD", "<b>Needed but not core</b> (16:12)", "TRUE / <b>Core</b> (2308)", "<b>✗</b>"],
    ["CTS / Minor Skin Mentor Review", "Not needed (16:25)", "FALSE (2309–2310)", "✓"],
    ["VAS Peer Review", "Recommended, not core (16:42–16:53)", "TRUE / Non Core (2311)", "✓"],
    ["CTS Peer Review", "Not core / not required (16:55)", "FALSE (2312)", "✓"],
    ["Surgical Reflective Review", "<b>Required but not core</b> (17:03)", "TRUE / <b>Core</b> (2313)", "<b>✗</b>"],
    ["Minor Skin Peer / CTS & MS Practical Mentor", "Not required (17:08)", "FALSE (2314–2316)", "✓"],
    ["VAS Practical Mentor Session", "Required, non-core (17:19)", "TRUE / Non Core (2317)", "✓"],
    ["Medic Appraisal", "Required, core (17:24)", "TRUE / Core (2318)", "✓"],
    ["Medic Revalidation", "Core (17:33)", "TRUE / Core (2319)", "✓"],
    ["IR35 Compliant", "Core (trades as a company) (17:33–17:47)", "TRUE / Core (2320)", "✓"],
]


def section3(c):
    para, H, table, bullets, figure, figref = c["para"], c["H"], c["table"], c["bullets"], c["figure"], c["figref"]
    s = [H("3. Chronological Step-by-Step Operator Workflow", 0),
         para("Twenty-two steps cover the whole 30:54 recording with no gaps. Start and end times are the utterance boundaries from the re-transcription; "
              "macro moments are pinned to the first frame showing the result."),
         table([["Step", "Window", "Action", "Tab"]] + [[str(st[0]), st[1] + "–" + st[2], st[3],
                 {1: "—", 2: "Manage Compliance", 3: "Names", 4: "Names", 5: "Compliance Timeframes", 6: "Compliance Timeframes", 7: "Roles", 8: "Requirements",
                  9: "Manage Requirements", 10: "Manage Requirements", 11: "Manage Requirements", 12: "Requirements", 13: "Names → Requirements",
                  14: "Requirements", 15: "Manage Compliance", 16: "Manage Compliance", 17: "Manage Compliance", 18: "Manage Compliance / (Compliance Data)",
                  19: "Names", 20: "Manage Compliance", 21: "Manage Compliance", 22: "—"}[st[0]]] for st in STEPS], [10, 32, 92, 46]),
         c["PageBreak"]()]
    for n, a, b, title, act, mp, mut, figs in STEPS:
        blk = [H("Step %d [%s – %s]: %s" % (n, a, b, title), 1),
               table([["<b>Action performed</b>", act], ["<b>Source → target</b>", mp], ["<b>State mutation (before → after)</b>", mut]], [38, 142], head=False, zebra=False)]
        s += blk
        if n == 11:
            s += [c["Spacer"](1, 4), para("<b>Spoken intent against values recorded</b> (Requirements rows 2299–2320, " + figref("reqA") + "):"),
                  table(REQ_COMPARE, [46, 50, 60, 12])]
        for f in figs:
            s.append(figure(f))
        s.append(c["Spacer"](1, 6))
    s.append(c["PageBreak"]())
    return s


# --------------------------------------------------------------------------------------------
def section4(c):
    para, H, table, bullets, figure, figref = c["para"], c["H"], c["table"], c["bullets"], c["figure"], c["figref"]
    s = [H("4. Data Quality Checks, Manual Exceptions &amp; Edge Cases", 0)]
    s += [H("4.1 Implicit business rules and keys", 1), table([
        ["ID", "Rule", "Where enforced today", "Evidence"],
        ["BR-01", "A person is identified by <b>Name</b> alone; no ID", "Every XLOOKUP on name_Table[Name]", figref("reqG")],
        ["BR-02", "Requirement identity = <font name='DVM'>Name-ComplianceType</font>; at most one per pair (intended)", "requirements_Table[Unique Lookup]; List Missing excludes existing pairs. <b>Not</b> enforced against duplicates", figref("mrL")],
        ["BR-03", "Compliance-record identity = <font name='DVM'>Name-ComplianceType</font> (Unique Lookup 3)", "Cross-workbook XLOOKUP (first match)", figref("mcV")],
        ["BR-04", "Due Date = Completion Date + Every x months (EDATE)", "Add path: automatic. <b>Update path: typed by hand</b>", figref("mcA") + ", " + figref("mcU")],
        ["BR-05", "Only Active = TRUE people appear on the dashboard; deactivation keeps history", "name_Table[Active] → requirements_Table[Active] → dashboard filter", figref("nmY")],
        ["BR-06", "Gauge colour: ≥T2 green … &lt;T5 red (0.9/0.8/0.7/0.6; DBS 0.98/0.9/0.8/0.7)", "Thresholds on Compliance Timeframes; applied in the dashboard", figref("ct3")],
        ["BR-07", "Onboarding items never expire (10000 months)", "Sentinel value in Every x months", figref("ct2")],
        ["BR-08", "Core flag is per person and overrides the catalogue default", "requirements_Table[Core Requirement]", figref("reqA")],
        ["BR-09", "The data store builds only from <b>saved</b> tool files", "Power Query reads files on disk", "Said 19:41–19:58"],
        ["BR-10", "Add-compliance batches must be contiguous (no blank rows)", "VBA loop stops at the first blank [Inferred]", "Said 20:45"],
        ["BR-11", "Evidence is cumulative (“build up a picture over time”) but corrections overwrite", "Add appends; Update overwrites", "Said 25:08, 25:52"],
    ], [13, 62, 65, 40])]
    s += [H("4.2 Manual exceptions and workarounds observed", 1), table([
        ["ID", "Exception", "How the operator handled it", "Evidence"],
        ["EX-01", "Managed By blank → Requirements!G shows 0", "Back-filled the master record (Names!B140 = Provide Wellbeing); recalculation fixed 22 rows", figref("nmMB") + " → " + figref("reqMB")],
        ["EX-02", "Wrong completion date stored (PI from 1 May, not 1 June)", "Update panel X/AB with the due date re-typed by hand, then <i>Update Existing Compliance</i>", figref("mcU") + " → " + figref("mcU2")],
        ["EX-03", "“Last updated” VBA does not run (error 13)", "Update the Last Updated tab by hand (“not a big deal”)", figref("vba") + "; Said 27:57–29:22"],
        ["EX-04", "Close-time save risks corrupting lookups", "Choose <b>Don’t Save</b> at close; save only at controlled points", figref("sv")],
        ["EX-05", "Slow Power Query over VPN", "Accept the wait; stop the query when not needed", figref("rf1")],
        ["EX-06", "Test person must not reach the dashboard", "Deactivate (Active = FALSE) rather than delete; rows remain in both workbooks", figref("nmY")],
        ["EX-07", "Non-applicable compliance types", "Set Required = FALSE at requirement stage; leave them out of compliance entry", figref("mrF")],
    ], [13, 52, 75, 40])]
    s += [H("4.3 Spoken vs. visual discrepancies", 1), table([
        ["ID", "Spoken", "On screen / in data", "Impact"],
        ["SV-01", "VAS Mentor Review or CPD: “needed, but it’s not core” (16:12)", "Requirements!D2308 = <b>Core</b>", "Inflates the core denominator; dashboard core % wrong for this person"],
        ["SV-02", "Surgical Reflective Review: “required, but it’s not core” (17:03)", "Requirements!D2313 = <b>Core</b>", "As SV-01. Probably a copy-paste carry-over (status bar shows paste mode)"],
        ["SV-03", "PI insurance “goes through to the 31st of May next year” (20:28)", "Due date shown 01/06/2027 (EDATE +12)", "One-day boundary ambiguity: is the due date the expiry day or the day after?"],
        ["SV-04", "Testy Tester is “not actually managed by anybody” (05:45)", "Managed By later set to Provide Wellbeing to clear a 0", "Managed By semantics unclear (contracting entity vs line manager)"],
        ["SV-05", "Person is a vasectomist / GPwSI (05:55)", "Manage Requirements!D8 Role = “Surgical Clinician – NHS Only” (left over from previous person)", "The form shows misleading context; field possibly unused"],
        ["SV-06", "“There is the compliance table… it’s pulled all these in” (11:50)", "Screen still on Staff Management!Compliance Timeframes", "PQ output never shown; schema unknown"],
        ["SV-07", "“We would save the data store first… do one refresh, save, refresh, save” (26:49–27:43)", "No visible save of Compliance Data.xlsm; one refresh started then cancelled", "Real publication sequence not demonstrated"],
        ["SV-08", "“There are 22 compliance areas” (06:56)", "Names!O shows 23 and 45 for some people against P = 22", "“Added / Total” ratio is not a completeness measure"],
        ["SV-09", "Missing: “I think it’s saying is it in the requirements or not” (10:25)", "Formula depends on <font name='DVM'>add_Requirements_Name</font> (one selected person), not a per-row person", "Column is only meaningful for the person on the form at that moment"],
    ], [13, 58, 57, 52])]
    s += [H("4.4 Hidden failure modes in the current process", 1), table([
        ["ID", "Failure mode", "Mechanism", "Severity"],
        ["FM-01", "<b>Key drift</b>", "String keys (Name, Name-Type). A rename, trailing space or a duplicate name (two “John Smith”) breaks or merges records silently; XLOOKUP falls back to \"\"/0 with no error", "High"],
        ["FM-02", "<b>First-match lookups on a history table</b>", "Store keeps multiple records per Name-Type, but XLOOKUP returns the first (oldest) match by default. The UI may show stale evidence, and <i>Update</i> may overwrite the wrong row", "High"],
        ["FM-03", "<b>Destructive updates</b>", "Update overwrites in place; Delete flag removes. No before-image, user stamp or timestamp, so there is no audit trail for compliance evidence", "High"],
        ["FM-04", "<b>Workbook coupling and close-order corruption</b>", "Manage Compliance formulas reference an open external workbook. Closing in the wrong order or saving at close corrupts the lookups [Said 29:29–29:43]", "High"],
        ["FM-05", "<b>Unsaved-state publication</b>", "PQ reads files on disk. Forgetting to save a tool before refresh publishes stale data, and nothing warns about it", "Medium"],
        ["FM-06", "<b>Non-atomic publish</b>", "Save → refresh → save → refresh can stop half-way (cancelled query at 28:24, VBA error at 29:17), leaving the dashboard partially updated", "High"],
        ["FM-07", "<b>Silent null coercion</b>", "XLOOKUP of a blank cell returns 0 (Managed By = 0) and is passed downstream as a value", "Medium"],
        ["FM-08", "<b>Batch truncation</b>", "Add VBA stops at a blank row, so items after a gap are silently not written [Said 20:45]", "Medium"],
        ["FM-09", "<b>Manual due dates on update</b>", "AB typed by hand can disagree with Every x months; no recalculation", "Medium"],
        ["FM-10", "<b>Manual RAG</b>", "RAG is chosen, not derived from due date/status, so a lapsed item can stay Green", "Medium"],
        ["FM-11", "<b>Metric denominator mismatch</b>", "Names!O counts onboarding rows while P counts only 22 staff types (23/22, 45/22)", "Low"],
        ["FM-12", "<b>Reference-data hygiene</b>", "Roles header row contains data (“Reception” lost); “Adult”/“Adults”; Start Date formats differ; IR35 in list Q but not in the table rows seen", "Low"],
        ["FM-13", "<b>UI-state-dependent formulas</b>", "CT!J depends on whichever name is currently selected; PQ snapshots taken while a name is selected embed that state", "Medium"],
        ["FM-14", "<b>Broken/undebuggable VBA</b>", "Error 13 on close; the last-updated macro could not be fixed by an internal expert [Said 28:09]", "Medium"],
        ["FM-15", "<b>Unbounded table growth and row order</b>", "Requirements is appended unsorted (~2,320 rows); new names are appended after Z; nothing archives inactive people", "Low"],
        ["FM-16", "<b>Test data left in production</b>", "Demo person’s 22 requirement rows and 8 store records were left (inactive); the Requirements save at 19:53 was committed", "Medium"],
    ], [13, 40, 107, 20])]
    s.append(c["PageBreak"]())
    return s


# --------------------------------------------------------------------------------------------
def section5(c):
    para, H, table, bullets, code, figref = c["para"], c["H"], c["table"], c["bullets"], c["code"], c["figref"]
    s = [H("5. Target Modern System Architecture Blueprint", 0),
         para("Design goals, from the failure modes in §4.4: (1) identity by surrogate key, never by display string; (2) compliance evidence as an "
              "append-only event ledger with derived “current” state; (3) reference data versioned and effective-dated; (4) every "
              "rule deterministic and testable as SQL; (5) publication atomic and reversible; (6) human judgement captured as explicit, "
              "audited decisions. The same pattern must serve sibling domains (Estates sites, Medical Devices, Incidents), so the model "
              "is <b>subject-generic</b>.")]
    s += [H("5.1 Logical flow", 1), code(
        "  [Operator UI / API]        [Bulk import (CSV/XLSX)]       [External checks: GMC, DBS]\n"
        "          |                            |                              |\n"
        "          v                            v                              v\n"
        "   +---------------------------------------------------------------------------+\n"
        "   | INGESTION & PREFLIGHT GATE  (header contract, types, FK resolution, dedup) |\n"
        "   +---------------------------------------------------------------------------+\n"
        "          | staged rows (batch_id)          | rejected rows -> exception queue\n"
        "          v                                  v\n"
        "   +-------------------+   rules engine   +-------------------------+\n"
        "   | STAGING (per batch)| --------------> | REVIEW GATE (HITL)       |\n"
        "   +-------------------+   (SQL views)    +-------------------------+\n"
        "                                                    | approve\n"
        "                                                    v\n"
        "   +---------------------------------------------------------------------------+\n"
        "   | CORE: subject, requirement, compliance_event (append-only), ref_* (versioned)|\n"
        "   +---------------------------------------------------------------------------+\n"
        "          |  publish(batch) = single transaction + snapshot id\n"
        "          v\n"
        "   +---------------------------+        +-----------------------------------+\n"
        "   | MART: v_current_compliance |  --->  | Dashboard (reads snapshot_id only) |\n"
        "   +---------------------------+        +-----------------------------------+")]
    s += [H("5.2 Ingestion & preflight gate", 1)] + bullets([
        "<b>No copy-paste.</b> Data enters through (a) the web form (replacing Manage Requirements / Manage Compliance), (b) a bulk upload (CSV/XLSX template) "
        "for migrations and sibling tools, or (c) connector jobs for registers (GMC, DBS update service) where licensing allows.",
        "<b>Header contract:</b> each upload type has a versioned JSON-Schema/Frictionless descriptor (column names, order-insensitive, required set, types). "
        "Unknown or missing columns fail the whole file before any row is staged.",
        "<b>Cell-level validation:</b> dates parsed in an explicit locale (fixes the 8/1/2026 ambiguity), enums checked against ref tables "
        "(Completion Status, RAG, Role, Managed By), booleans strict, text trimmed and NFC-normalised, and every row checked to resolve to an existing subject and compliance type.",
        "<b>Staging:</b> rows land in <font name='DVM'>stg_*</font> tables tagged with <font name='DVM'>batch_id</font>, source file hash, uploader and line number; they are never edited in place.",
        "<b>Idempotency:</b> re-uploading the same file hash for the same scope is a no-op. A natural-key hash per row detects duplicates inside and across batches.",
    ])
    s += [H("5.3 Relational data model & identity resolution", 1), table([
        ["Table", "Purpose / key columns", "Replaces"],
        ["<b>subject_type</b>", "staff | site | device | … (one engine for all user-input tools)", "One workbook per domain"],
        ["<b>subject</b>", "subject_id (PK, identity), subject_type_id, display_name, managed_by_org_id (FK), employment_type, role_id (FK), start_date, "
         "active_from/active_to (replaces Active boolean), created_by/at", "Names!A:N"],
        ["<b>subject_alias</b>", "subject_id, system (SystmOne | PD | Email | Payroll), alias_value, UNIQUE(system, alias_value)", "Names!K:M, free-text emails"],
        ["<b>organisation</b>", "org_id, name (Provide Wellbeing, Provide CIC, Workforce Solutions)", "Managed By text"],
        ["<b>ref_role</b>", "role_id, code, label, is_clinical, valid_from/to", "Roles tab (fixes header defect)"],
        ["<b>ref_compliance_type</b>", "compliance_type_id, code, label, group1..n via <b>ref_compliance_group</b> (many-to-many with weight), "
         "is_onboarding, never_expires (replaces 10000)", "Compliance Timeframes A, D:I, Q, S"],
        ["<b>ref_compliance_policy</b> (versioned)", "policy_id, compliance_type_id, frequency_months, default_core, threshold_1..5, "
         "<b>version, valid_from, valid_to, approved_by</b>. Immutable once published; changes create a new version", "Compliance Timeframes B, C, K:O"],
        ["<b>requirement</b>", "requirement_id (PK), subject_id, compliance_type_id, is_required, is_core, notes, valid_from/to, "
         "UNIQUE(subject_id, compliance_type_id, valid_from)", "requirements_Table"],
        ["<b>compliance_event</b> (append-only)", "event_id (PK), requirement_id (FK), event_type (RECORDED | CORRECTED | VOIDED), completed_on, status_id, rag_override, notes, "
         "evidence_uri, <b>supersedes_event_id</b>, batch_id, entered_by, entered_at", "compliance_Data_Store_Table + Update/Delete VBA"],
        ["<b>evidence_file</b>", "file_id, event_id, storage_uri, sha256, uploaded_by", "“Certificate on file”"],
        ["<b>ingest_batch / publication</b>", "batch_id, status (STAGED → VALIDATED → APPROVED → PUBLISHED | REJECTED), snapshot_id, approver, timestamps", "Save/refresh choreography"],
        ["<b>audit_log</b>", "row-level CDC (table, pk, before, after, actor, ts) via triggers or logical replication", "— (none today)"],
    ], [38, 102, 40])]
    s += [para("<b>Identity resolution:</b> every inbound row resolves to <font name='DVM'>subject_id</font> by (1) explicit ID, (2) exact alias match, "
               "(3) normalised-name match with uniqueness check. Ambiguous or unmatched rows go to the exception queue, never to fuzzy auto-merge. "
               "Renames update <font name='DVM'>display_name</font> only, so no history breaks (fixes FM-01).")]
    s += [H("5.4 Transformation & business-rules engine (Excel/VBA → SQL)", 1), table([
        ["Legacy artefact", "Deterministic replacement"],
        ["Names!O COUNTIFS / P COUNTIFS", "<font name='DVM'>v_subject_coverage</font>: COUNT(requirements WHERE NOT is_onboarding) / COUNT(active staff policy types), on the same domain (fixes FM-11)"],
        ["Names!Q Name if Active", "Filter <font name='DVM'>WHERE now() BETWEEN active_from AND coalesce(active_to,'infinity')</font>"],
        ["CT!H/I Unique Lookup 1/2 (CONCAT)", "Join to <font name='DVM'>ref_compliance_group</font>; no string keys"],
        ["CT!J Missing (UI-state XLOOKUP)", "<font name='DVM'>v_missing_requirements</font>: subject × policy types LEFT JOIN requirement WHERE requirement IS NULL (for all subjects; parameter-free)"],
        ["VBA List Missing", "API <font name='DVM'>GET /subjects/{id}/missing-requirements</font> backed by the view above"],
        ["VBA Add / Update Requirements", "<font name='DVM'>POST/PATCH /requirements</font> → staged; on approval, close the old row (valid_to) and insert the new one (SCD-2)"],
        ["Requirements!G/I/J XLOOKUPs", "Joins at query time (organisation, current policy version, subject activity); nothing duplicated"],
        ["Manage Compliance O (Time Frame) and W/AB (Due Date)", "<font name='DVM'>due_on = completed_on + make_interval(months =&gt; policy.frequency_months)</font> on the policy version effective at completed_on; never typed (fixes FM-09). Boundary rule (SV-03) parameterised: due_on or due_on − 1 day"],
        ["Cross-workbook XLOOKUP (first match)", "<font name='DVM'>v_current_compliance</font>: ROW_NUMBER() OVER (PARTITION BY requirement_id ORDER BY completed_on DESC, entered_at DESC) = 1, excluding superseded/voided events (fixes FM-02)"],
        ["Update Existing Compliance (overwrite)", "Insert a CORRECTED event with supersedes_event_id; the original is kept (fixes FM-03)"],
        ["Delete flag (AC)", "Insert a VOIDED event with a mandatory reason"],
        ["Manual RAG", "Derived: Green if due_on &gt; today + amber_window; Amber if within the window; Red if overdue or status ≠ Completed. An optional rag_override needs a reason (fixes FM-10)"],
        ["Gauge thresholds K:O", "Dashboard reads <font name='DVM'>ref_compliance_policy.threshold_n</font> of the published version"],
        ["Power Query merge of all tools", "One database; the mart view is filtered by subject_type"],
        ["Change detection (history)", "LAG(completed_on) OVER (PARTITION BY requirement_id ORDER BY completed_on) gives the renewal interval and a lateness KPI"],
    ], [52, 128])]
    s += [para("Example: the current-state view the dashboard reads."),
          c["code"](
              "CREATE VIEW mart.v_current_compliance AS\n"
              "WITH live AS (\n"
              "  SELECT e.*, ROW_NUMBER() OVER (PARTITION BY e.requirement_id\n"
              "                                 ORDER BY e.completed_on DESC, e.entered_at DESC) AS rn\n"
              "  FROM core.compliance_event e\n"
              "  WHERE e.event_type <> 'VOIDED'\n"
              "    AND NOT EXISTS (SELECT 1 FROM core.compliance_event s WHERE s.supersedes_event_id = e.event_id))\n"
              "SELECT r.requirement_id, r.subject_id, r.compliance_type_id, r.is_core,\n"
              "       l.completed_on, l.status_id,\n"
              "       (l.completed_on + make_interval(months => p.frequency_months))::date AS due_on,\n"
              "       core.derive_rag(l.status_id, l.completed_on, p.frequency_months, l.rag_override) AS rag\n"
              "FROM core.requirement r\n"
              "JOIN core.subject s ON s.subject_id = r.subject_id AND s.active_to IS NULL\n"
              "LEFT JOIN live l ON l.requirement_id = r.requirement_id AND l.rn = 1\n"
              "JOIN ref.compliance_policy p ON p.compliance_type_id = r.compliance_type_id\n"
              " AND coalesce(l.completed_on, current_date) BETWEEN p.valid_from AND coalesce(p.valid_to, 'infinity')\n"
              "WHERE r.is_required AND r.valid_to IS NULL;")]
    s += [H("5.5 Exception handling & human-in-the-loop controls", 1)] + bullets([
        "<b>Exception queue</b> per batch: unresolved subject, unknown compliance type, date out of range (in the future, or before the subject’s start date), missing Managed By "
        "(EX-01 becomes a blocking validation, not a silent 0), duplicate event, Core flag differing from the policy default (SV-01/02 surfaced for confirmation).",
        "<b>Requirement wizard</b> replaces List Missing: pre-selects types from <i>role templates</i> (e.g. GPwSI-Vasectomy ⇒ PI, GMC, VAS Accreditation, Enhanced DBS, Appraisal, Revalidation, IR35 if trading as a company). "
        "The operator adjusts, and each deviation from the template is logged with a reason.",
        "<b>Four-eyes review gate:</b> batches touching core requirements, policy versions or deletions need approval by a second user (role: Compliance Approver). "
        "The reviewer sees a diff (before → after) per subject, the same view as the BEFORE/AFTER figures in §3.",
        "<b>Overrides</b> (RAG override, policy exception, “not applicable”) are first-class records with reason, actor, expiry date and a link to evidence.",
        "<b>Sandbox mode</b> for training and demos (the Testy Tester scenario): a separate schema or a <font name='DVM'>is_test</font> tenant, so demo data never reaches production (fixes FM-16).",
        "<b>Last-updated</b> becomes <font name='DVM'>publication.published_at</font>, shown automatically on the dashboard (fixes EX-03 / FM-14).",
    ])
    s += [H("5.6 Atomic publication & auditability", 1)] + bullets([
        "<b>Publish = one database transaction</b>: move APPROVED staged rows into core, write audit_log, create <font name='DVM'>snapshot_id</font>, set "
        "<font name='DVM'>publication.status = PUBLISHED</font>. Any failure rolls back everything, so the save → refresh → save sequence goes away (fixes FM-05/06).",
        "<b>Snapshot reads:</b> the dashboard queries only the latest published snapshot (materialised view refreshed <i>inside</i> the publish transaction, "
        "or a <font name='DVM'>snapshot_id</font> pointer swap), so users never see a half-built state.",
        "<b>Rollback:</b> a publication can be reverted by a compensating batch (void events, close requirement versions) or by re-pointing to the previous snapshot. Both are audited.",
        "<b>Row-level lineage:</b> every core row carries batch_id → source (form/session or file hash + line) → actor → approval, and the evidence file sha256 is stored with it.",
        "<b>Concurrency:</b> optimistic locking (row version) on requirement and subject edits; publications serialised per subject_type with an advisory lock.",
        "<b>Retention and security:</b> RBAC (Operator, Approver, Viewer, Admin), personal data limited to what is needed (emails/phones in a restricted table), and an audit log retained according to NHS records-management rules (to be confirmed).",
    ])
    s += [H("5.7 Migration from the legacy workbooks", 1)] + bullets([
        "Extract name_Table, requirements_Table, Compliance_Timeframe_Table and compliance_Data_Store_Table (read-only) → load into staging → run the "
        "same preflight; expect FM-01/02/11/12 issues to surface as exceptions (duplicate Name-Type keys, Managed By = 0, onboarding rows).",
        "Seed ref_compliance_policy v1 from the current Compliance Timeframes values, then let the business owner approve v2 with the corrected Core flags (SV/§6).",
        "Run in parallel for one monthly cycle: compare v_current_compliance against the Excel-built dashboard per subject and type; sign off before switch-over.",
    ])
    s.append(c["PageBreak"]())
    return s


# --------------------------------------------------------------------------------------------
def section6(c):
    para, H, table, figref = c["para"], c["H"], c["table"], c["figref"]
    s = [H("6. Gap &amp; Ambiguity Register", 0), table([
        ["ID", "Timestamp", "Gap / ambiguity", "Why it matters", "Ask of business owner"],
        ["G-01", "whole .srt", "The supplied .srt is from a different meeting (Incidents/Datix, 13:59:33). Its Datix export, category-grouping lookup and #REF error are not in this video",
         "That workflow (raw-export ingestion, a different shape) is unspecified", "Provide the matching .mp4 for 135933 (and its .txt) for a separate spec"],
        ["G-02", "00:11:43–00:11:54", "PQ-built “staff management compliance table” referred to but not visible (other window)", "Schema of PQ outputs and the dashboard grain unknown", "Share Compliance Data.xlsm (queries + tables)"],
        ["G-03", "00:01:50–00:02:03", "“Get rid of something I did on my abortive attempt”: no visible change", "Possible undocumented clean-up step", "Confirm what was removed and how"],
        ["G-04", "00:24:03, 00:25:08", "Store keeps history, yet lookups use first-match XLOOKUP on Unique Lookup 3. Which record does Update overwrite?", "Correctness of “current” state", "Share VBA modules; confirm whether history is kept or only the latest row"],
        ["G-05", "00:09:13, 00:11:12", "IR35 Compliant appears in list Q and gets a 12-month timeframe, but is not in table rows 2–22 seen", "Catalogue completeness", "Confirm the full Compliance_Timeframe_Table (rows 43+)"],
        ["G-06", "00:29:38", "Compliance Data shows a Unique Lookup list with 024/025/026 prefixes (0.3 s glimpse)", "Unknown coding scheme", "Explain the prefixes (period? area code? query ID?)"],
        ["G-07", "00:14:28, 00:17:43", "Copy marquee and “Select destination…” during requirement entry; two Core values disagree with speech", "Data-entry error vs intended values", "Confirm the Core flag for VAS Mentor/CPD and Surgical Reflective Review"],
        ["G-08", "00:08:32–00:09:54", "Core flags and Compliance Group 3/4 disputed (“Matt decided… Richard needs to make a call”); onboarding scope undecided", "Drives policy v2 and dashboard grouping", "Richard to approve the Core list, groups and onboarding scope"],
        ["G-09", "00:06:47, 00:28:53", "Start Date typed as 1 Aug shows “8/1/2026” while others are dd/mm/yyyy", "Locale / text-date risk at migration", "Confirm the column’s cell type and format"],
        ["G-10", "00:20:13", "Manage Compliance columns H–N hidden; Manage Requirements helper M:T “originally hidden”", "Possible extra fields or logic", "Unhide and share"],
        ["G-11", "00:13:23–00:15:05", "Role (D8) source and use unknown; stale value", "May be dead UI or broken lookup", "Confirm whether Role drives anything"],
        ["G-12", "tab bar", "<i>Instructions</i> and <i>Manage Onboarding</i> never opened", "Onboarding workflow unspecified", "Record the onboarding flow"],
        ["G-13", "00:20:28, 00:24:52", "Expiry semantics: “to 31 May” against due 01/06; the update path needs the due date typed", "Off-by-one and consistency", "Define due date = expiry day or day after"],
        ["G-14", "00:26:49–00:27:43", "Publish sequence (save store, refresh ×2, save ×2, Last Updated tab) described, not performed", "Needed to replicate the outputs exactly", "Walk through one full monthly publish on video"],
        ["G-15", "00:27:57–00:29:22", "VBA ‘last updated’ macro: error 13 on close; code not shown", "Root cause unknown", "Share the VBA project (all modules)"],
        ["G-16", "00:04:27, 00:10:40", "Dashboard product, gauge formula and the meaning of Threshold 1 (=1) not shown", "Visual spec", "Share the dashboard file / measure definitions"],
        ["G-17", "00:03:56–00:04:03", "Whether Managed By is required (“I don’t think it is, but it might be”)", "Validation rule (EX-01)", "Confirm mandatory fields per subject type"],
        ["G-18", "00:29:29–00:29:50", "The corruption mechanism if Compliance Data closes first is described only vaguely", "Explains the Don’t Save practice", "Describe the observed corruption symptoms"],
        ["G-19", "00:00:00–00:30:54", "Audio quality: Whisper mis-hears names (e.g. “Dheeraj”); the TurboScribe .txt ends at ~30:00", "Small wording uncertainty only", "None. Wording cross-checked against both transcripts"],
    ], [11, 22, 58, 40, 49])]
    s.append(c["PageBreak"]())
    return s


# --------------------------------------------------------------------------------------------
def appendix(c):
    para, H, table, FIGS = c["para"], c["H"], c["table"], c["FIGS"]
    s = [H("Appendix A. Figure Index", 0),
         table([["Fig", "Time", "File › Tab", "Shows"]] + [[str(i), f[1], E(f[2]) + " › " + E(f[3]), E(f[4])[:150] + ("…" if len(f[4]) > 150 else "")]
                                                        for i, f in enumerate(FIGS, 1)], [8, 16, 44, 112])]
    s += [H("Appendix B. Key timestamped utterances (re-transcribed)", 0), table([
        ["Time", "Utterance (lightly cleaned)"],
        ["00:00:58", "I’m going to run you through how we update the data store for the majority of the compliance dashboard."],
        ["00:01:14", "This particular area of the compliance data is called staff management."],
        ["00:02:14", "…reads and writes from the data store. So it’s kind of a semi-automated update process."],
        ["00:02:54", "First of all, to fill in this tab that says Names."],
        ["00:04:16", "This column here, which is Active… if it’s true, it will be featured in the visuals on the dashboard."],
        ["00:05:40", "We’ll call the person Testy Tester… a freelance contractor, so they’re not actually managed by anybody."],
        ["00:06:56", "We haven’t set any compliance areas up yet. There are 22 compliance areas we could conceivably set up."],
        ["00:07:16", "…set up something called compliance timeframes."],
        ["00:08:41", "Performance review should be core. Matt very much decided these on his own."],
        ["00:10:19", "XLOOKUP, CONCAT, add requirements name, compliance type… I think it’s saying is it in the requirements or not."],
        ["00:10:40", "If it’s above 0.9 it’s going to be green; if it’s below 0.6 it’s going to be red, and shades in between."],
        ["00:11:21", "When the data is refreshed for the first time, these compliance timeframe tables are built through power queries."],
        ["00:14:18", "If I click List Missing, Visual Basic will show me for Testy Tester which of these I haven’t set up."],
        ["00:17:53", "So now I’m going to write this into the requirements data, which is done by Visual Basic."],
        ["00:19:00", "So actually let’s add Provide Wellbeing in there."],
        ["00:19:41", "Now I’m going to save that, because when I refresh my data… it can’t if I’ve not saved it."],
        ["00:20:45", "I can do these all in one go if I want. It doesn’t like it, the Visual Basic, if you miss a row."],
        ["00:23:31", "We’ll now use the Visual Basic to add the record to the compliance data."],
        ["00:24:30", "If we input some data and it happens to be wrong… we can use this section here to alter it."],
        ["00:25:52", "That has now amended that to the 1st of May, so that has overwritten that data."],
        ["00:26:49", "We would save the data store first…"],
        ["00:27:35", "We would do one refresh, we would then save, we would then do another refresh, and then save."],
        ["00:27:57", "There is Visual Basic in the tools that should do this automatically… but some of the Visual Basic’s not working."],
        ["00:28:46", "I’m just going to make Testy Tester not active."],
        ["00:29:29", "We don’t save at this stage because… it closes the compliance data before… these formulas, which are just lookups, can corrupt."],
    ], [18, 162])]
    return s


# --------------------------------------------------------------------------------------------
def section7(c):
    para, H, table, bullets, figref = c["para"], c["H"], c["table"], c["bullets"], c["figref"]
    W = [13, 50, 117]
    s = [H("7. What Is Required to Build the Modern System", 0),
         para("This section lists everything needed to build the replacement described in §5: business inputs, functional and non-functional "
              "requirements, technology, data migration, testing, people and phasing. <b>Every item gives the reason it is required</b>, "
              "traced to the evidence in this report (figure, timestamp, failure mode FM-xx, exception EX-xx, discrepancy SV-xx or gap G-xx). "
              "An item with no evidence-backed reason is left out on purpose. Priority: <b>M</b> = must have for go-live, <b>S</b> = should have, "
              "<b>C</b> = could have later.")]

    # 7.1 Prerequisites
    s += [H("7.1 Prerequisites from the business (before any build starts)", 1),
          para("These are inputs only the business can supply. Without them the build would copy unknown behaviour or encode unconfirmed rules. "
               "They are expanded item by item (files, sheets, VBA, rules, decisions, plus a sign-off checklist) in the companion document "
               "<b>Staff_Management_PreBuild_Client_Requirements.pdf</b> in the same folder."),
          table([
              ["ID", "What is required", "Why it is required"],
              ["P-01", "<b>Export of the full VBA project</b> from Staff Management.xlsm (all modules: List Missing, Add/Update Requirements, Add New / Update Existing Compliance, close/last-updated)",
               "The macros hold the write logic, and none of it was visible. Without the code we cannot tell which store row <i>Update</i> overwrites (G-04), why a blank row stops a batch (FM-08), or what causes run-time error 13 (" + figref("vba") + ", G-15)."],
              ["P-02", "<b>Copy of Compliance Data.xlsm</b> with its Power Query definitions (M code), table list and the dashboard file",
               "The data store and PQ outputs were never on screen (SV-06, G-02, G-06). Their schema sets the migration source and what the dashboard expects, and they are needed for the parity test in 7.6."],
              ["P-03", "<b>Full, approved compliance-type catalogue</b> (all rows of Compliance_Timeframe_Table incl. IR35 and onboarding items)",
               "IR35 Compliant appears in a list but not in the table rows seen (G-05). Every requirement, due date and gauge depends on this catalogue, so it must be complete and signed off."],
              ["P-04", "<b>Policy decisions from the business owner (Richard)</b>: Core vs non-core per type; whether Compliance Groups 3/4 stay; whether onboarding is in scope",
               "The operator disputes the current Core flags and says the grouping and onboarding scope are “for Richard to make a call on” (00:08:32–00:09:54, G-08). Building on unapproved rules would bake in disputed numbers."],
              ["P-05", "<b>Due-date rule</b>: is the due date the expiry day or the day after? Must a corrected record recompute it?",
               "Spoken “to 31 May” vs the shown 01/06/2027 (SV-03), and the due date is typed by hand on update (" + figref("mcU") + ", FM-09). The rule decides every RAG status."],
              ["P-06", "<b>RAG rule</b> (amber window, how Scheduled / Sign-off Required count)",
               "RAG is picked by hand today (" + figref("mc2") + ", FM-10). Deriving it automatically needs an agreed rule."],
              ["P-07", "<b>Mandatory-field list</b> per subject type (e.g. is Managed By required?)",
               "A blank Managed By silently became 0 downstream (" + figref("reqA") + ", EX-01), and the operator is unsure whether it is essential (G-17)."],
              ["P-08", "<b>Role templates</b>: which compliance types apply to each role (GPwSI-Vasectomy, Nurse, HCA, …)",
               "Today the operator decides 22 types from memory for each new person (00:14:50–00:17:53), and two Core values were entered against what was said (SV-01/02). Templates make this repeatable."],
              ["P-09", "<b>Named owners and approvers</b> (data owner, compliance approver, system admin)",
               "The four-eyes review gate (§5.5) and the publication sign-off need named people. Today one operator does everything with no second check."],
              ["P-10", "<b>Information-governance sign-off</b>: DPIA, lawful basis, retention periods for DBS/indemnity/appraisal evidence",
               "The system holds personal staff data (phones, emails, DBS dates, professional registration). An NHS-facing provider must do a DPIA and set retention before storing this centrally."],
              ["P-11", "<b>Recordings of the remaining tools</b> (Incidents/Datix, Estates, Medical Devices, Onboarding)",
               "The supplied .srt is an Incidents workflow (G-01); Instructions and Manage Onboarding were never opened (G-12). The generic model (subject_type) must be checked against these before its schema is frozen."],
          ], W)]

    # 7.2 Functional
    s += [H("7.2 Functional requirements", 1), table([
        ["ID", "Requirement (priority)", "Why it is required"],
        ["FR-01", "<b>Subject register with a system ID</b>; names are display-only and can be renamed (M)",
         "Every lookup today is on the name text (BR-01). A typo, rename or a duplicate name breaks or merges records silently (FM-01)."],
        ["FR-02", "<b>Alias table</b> for SystmOne / PD / email identities, unique per system (S)",
         "Names!K:M hold the same person under other system names (" + figref("nm1") + "). Imports and connectors need a dependable way to match a person."],
        ["FR-03", "<b>Effective-dated activity</b> (active from/to) instead of a TRUE/FALSE flag (M)",
         "Active is the main dashboard filter (00:04:16) and was flipped by hand to hide a test person (" + figref("nmY") + "). With dates, history stays correct for past reporting periods."],
        ["FR-04", "<b>Requirement set-up wizard</b> pre-filled from role templates, with a reason logged for each deviation (M)",
         "Replaces List Missing and a manual 22-row grid (" + figref("mrL") + ", " + figref("mrF") + ") that produced two wrong Core flags (SV-01/02)."],
        ["FR-05", "<b>“Missing requirements” view</b> for all subjects, independent of what is on screen (M)",
         "The current Missing column only works for whichever name is selected on the form (" + figref("ctJ") + ", SV-09, FM-13)."],
        ["FR-06", "<b>Compliance evidence entry</b>: date, status, notes and an <b>evidence file upload</b> (M)",
         "Evidence today is a note like “Certificate on file” with no link to the document (" + figref("mc2") + "). Audits need the actual file and its hash."],
        ["FR-07", "<b>Automatic due date</b> from the policy version in force on the completion date (M)",
         "The due date is typed by hand on the update path (" + figref("mcU") + ") and can drift from the frequency (FM-09)."],
        ["FR-08", "<b>Automatic RAG</b> with a justified, time-limited override (M)",
         "RAG is selected by hand (" + figref("mc3") + "), so a lapsed item can stay Green (FM-10)."],
        ["FR-09", "<b>Corrections and voids as new events</b>, keeping the original (M)",
         "<i>Update Existing Compliance</i> overwrites the record (" + figref("mcU2") + "), and the Delete flag removes it, leaving no audit trail (FM-03)."],
        ["FR-10", "<b>Current-state view</b> that always picks the latest valid event (M)",
         "Lookups return the <i>first</i> match on a table that keeps history (" + figref("mcV") + ", FM-02), so stale evidence can show."],
        ["FR-11", "<b>Validation that blocks bad input</b> (missing mandatory fields, unknown types, future or impossible dates, duplicates) with clear messages (M)",
         "Blanks become 0 (FM-07), batches stop at a blank row with no warning (FM-08), and date formats are mixed (G-09)."],
        ["FR-12", "<b>Bulk import</b> (CSV/XLSX template) through the same validation (S)",
         "Needed for migration (§7.5) and for sibling tools and future exports such as Datix (G-01). It also removes copy-paste as a data path."],
        ["FR-13", "<b>Review/approval gate</b> with a before/after diff per subject (M)",
         "One operator changes requirements and evidence and publishes with no second check; errors like SV-01/02 reach the dashboard unseen."],
        ["FR-14", "<b>One-click atomic publish and rollback</b>, with a recorded publish time (M)",
         "Today’s save → refresh → save → refresh can stop half-way (cancelled at 00:28:24, error at 00:29:17; FM-05/06). “Last updated” is filled in by hand because its macro fails (EX-03)."],
        ["FR-15", "<b>Due/overdue work queue and reminders</b> to staff and managers (S)",
         "The monthly cycle is to chase clinicians and staff by hand for anything not yet updated (00:26:18–00:26:38)."],
        ["FR-16", "<b>Training/sandbox mode</b> separate from production (S)",
         "The demo left 22 test requirement rows and 8 store records in the live files, hidden only by Active = FALSE (FM-16)."],
        ["FR-17", "<b>Reference-data admin</b> for compliance types, policy versions, thresholds, roles and organisations, with approval (M)",
         "These lists are hand-edited cells today; the Roles header holds a data value (" + figref("rol") + ", FM-12), and thresholds were set by one person (00:11:03)."],
        ["FR-18", "<b>Generic subject types</b> (staff, site, device, …) on one engine (S)",
         "The same tool is cloned per domain: a “Site” header on the staff form gives this away (" + figref("mrT") + "). The operator confirms sites and devices follow the same pattern (00:03:22)."],
        ["FR-19", "<b>Correct coverage metrics</b> (requirements set up vs applicable types, same scope) (S)",
         "The current count shows 23/22 and 45/22 because it mixes onboarding rows with a staff-only total (" + figref("nm3") + ", FM-11)."],
        ["FR-20", "<b>Dashboard feed</b>: published views and policy thresholds exposed to the BI tool (M)",
         "The dashboard reads Active, the requirement and compliance tables, and Threshold 1–5 for its gauges (00:10:40, " + figref("ct3") + ")."],
    ], W)]

    # 7.3 Non-functional
    s += [H("7.3 Non-functional requirements", 1), table([
        ["ID", "Requirement", "Why it is required"],
        ["NFR-01", "<b>Database-enforced integrity</b>: primary/foreign keys, unique constraints, check constraints", "Excel cannot stop duplicate keys or orphan rows (FM-01, FM-02). The database must refuse bad data, not just a form."],
        ["NFR-02", "<b>Row-level audit log</b> (who, when, before/after) retained per policy", "There is currently no record of who changed compliance evidence or when (FM-03). Regulators and internal audit will ask."],
        ["NFR-03", "<b>Single sign-on and role-based access</b> (Operator, Approver, Viewer, Admin)", "The files sit on a shared drive (Z:\\…) open to anyone with drive access. The four-eyes gate (FR-13) needs real user identities."],
        ["NFR-04", "<b>Data protection</b>: encryption in transit and at rest, contact details in a restricted table, UK GDPR / NHS DSP Toolkit alignment", "Staff personal data and DBS details are held (" + figref("nm2") + "). See P-10."],
        ["NFR-05", "<b>Performance</b>: publish in seconds; UI responses under 1 s for one subject", "Refresh over the VPN is slow (“five or six seconds in the office”, much longer remotely: 00:27:19), and the operator cancels it."],
        ["NFR-06", "<b>No file-locking or open-order dependency</b>", "Lookups “can corrupt” if Compliance Data closes first, so saving at close is avoided (00:29:29, FM-04)."],
        ["NFR-07", "<b>Reliability</b>: daily backups, tested restore; target RPO ≤ 24 h, RTO ≤ 4 h (to confirm)", "Today the only copy is the workbook on Z:. A corrupt save, which the operator already guards against, loses data."],
        ["NFR-08", "<b>Maintainability</b>: logic as version-controlled SQL and code with automated tests", "The VBA is broken and an internal expert could not debug it (00:28:09, FM-14)."],
        ["NFR-09", "<b>Observability</b>: job logs, publish history, failed-validation counts, alerts", "Failures today are silent (FM-05/07/08) or show up as a modal error dialog (" + figref("vba") + ")."],
        ["NFR-10", "<b>Accessibility</b> (WCAG 2.2 AA) for the entry UI", "Public-sector web services are expected to meet it. The Excel status bar already flags “Accessibility: Investigate” on these sheets."],
    ], W)]

    # 7.4 Technology
    s += [H("7.4 Technology components", 1),
          para("A recommended default is given for each component; any equivalent works if it meets the reason. Defaults favour the "
               "Microsoft 365 estate shown in the recording (Teams, Excel, Power Query)."),
          table([
              ["Component", "Recommended default", "Why it is required"],
              ["Relational database", "PostgreSQL 16 (or Azure SQL)", "Needs keys and constraints (NFR-01), window functions such as ROW_NUMBER and LAG for current state and history (FR-10), and transactions for atomic publish (FR-14)."],
              ["Application API", "A typed backend service (e.g. NestJS/TypeScript or ASP.NET Core)", "One place for the business rules (BR-01…11), validation (FR-11) and the review gate (FR-13), instead of logic spread across cells and VBA."],
              ["Web user interface", "React single-page app (or Power Apps for a low-code route)", "Replaces the Manage Requirements / Manage Compliance forms with validated forms, the wizard (FR-04) and the review diff (FR-13)."],
              ["Identity provider", "Microsoft Entra ID single sign-on", "The organisation already works in Microsoft 365. It gives real user identities for audit and approvals (NFR-02/03) with no new passwords."],
              ["Evidence file storage", "Azure Blob Storage or SharePoint library, private, with SHA-256 per file", "Needed to hold the certificates and copies now noted only as “on file” (FR-06)."],
              ["Ingestion/validation library", "Frictionless/JSON-Schema contracts + import service", "Header and cell checks for bulk imports (FR-12) so nothing enters by copy-paste."],
              ["Job scheduler", "Platform scheduler (e.g. Azure Functions timer / cron worker)", "For reminders (FR-15), optional register checks (GMC, DBS update service) and nightly integrity reports (NFR-09)."],
              ["BI / dashboard", "Existing dashboard tool (likely Power BI, to confirm, G-16) on published views", "Keeps users on the dashboard they know while removing Power Query file merges (FR-20)."],
              ["Source control and CI/CD", "Git repository (this one) + pipeline with tests and migrations", "Makes rule changes reviewable and testable (NFR-08), unlike VBA that nobody can debug."],
              ["Infrastructure as code", "Bicep/Terraform", "Repeatable dev, test and prod environments; the sandbox (FR-16) becomes a normal environment."],
              ["Monitoring", "Application Insights / OpenTelemetry", "Supports NFR-09 (logs, alerts on failed publishes)."],
          ], [32, 50, 98])]

    # 7.5 Migration
    s += [H("7.5 Data migration requirements", 1), table([
        ["ID", "What is required", "Why it is required"],
        ["DM-01", "Read-only extracts of name_Table (~140 rows), requirements_Table (~2,320), Compliance_Timeframe_Table, Roles, compliance_Data_Store_Table", "These are the only records of who must comply with what, and of the evidence held (" + figref("req0") + ")."],
        ["DM-02", "Cleansing rules: trim and normalise names; map Managed By 0 → NULL or a value; fix the Roles header; standardise Start Date; split multi-address emails", "Known defects seen on screen (FM-07, FM-12, G-09) would otherwise move into the new database."],
        ["DM-03", "Duplicate-key report (Name-Type pairs with more than one row) for business resolution", "Counts of 23 and 45 per person (FM-11) and first-match lookups (FM-02) suggest duplicates and history that someone must review."],
        ["DM-04", "Policy v1 = today’s catalogue values; v2 = approved values from P-04", "Keeps past reporting reproducible while the corrected rules take effect from an agreed date."],
        ["DM-05", "Exclude or flag test records (e.g. “Testy Tester”)", "The demo left test data in production (FM-16)."],
        ["DM-06", "Freeze window and final delta load", "The Excel tool keeps changing during the parallel run, so the last changes must be carried over."],
    ], W)]

    # 7.6 Testing
    s += [H("7.6 Testing and acceptance requirements", 1), table([
        ["ID", "What is required", "Why it is required"],
        ["T-01", "Unit tests for every business rule BR-01…BR-11 and every SQL view", "The rules are reverse-engineered from a video; tests pin them down and catch regressions."],
        ["T-02", "Golden-case tests from this recording (Testy Tester: 22 requirements, 8 events, PI correction to 01/05/2026 → due 01/05/2027)", "This is the one fully observed end-to-end case (" + figref("reqA") + ", " + figref("mcU2") + "), so it is ideal as an acceptance script."],
        ["T-03", "Parity reconciliation for one monthly cycle: new mart vs Excel-built dashboard, per subject and type; differences explained", "Shows the new system gives the same answers, or that each difference is a known defect fixed (§4.4)."],
        ["T-04", "Negative tests: blank mandatory fields, duplicate names, bad dates, interrupted publish", "These are the exact failure modes found in this workflow (FM-05/06/07/08)."],
        ["T-05", "User acceptance by the operator and the approver", "They own the monthly process and the policy decisions (P-04, P-09)."],
        ["T-06", "Security and IG testing (access control, penetration test as policy requires)", "Personal and DBS data are involved (NFR-03/04, P-10)."],
    ], W)]

    # 7.7 People
    s += [H("7.7 People and roles", 1), table([
        ["Role", "Responsibility", "Why it is required"],
        ["Business owner (Richard, per recording)", "Approves policy, Core flags, grouping and scope", "Named by the operator as the decision-maker for open policy questions (00:09:54)."],
        ["Compliance SME (current operator)", "Explains the process, writes test cases, runs UAT", "The only person shown who knows the monthly routine and its workarounds."],
        ["Product owner / business analyst", "Owns the backlog; closes the §6 gaps", "19 open gaps must be closed before the schema is final."],
        ["Data engineer", "Schema, migration, views, publish transaction", "Most of the work is data modelling and migration (§5.3, §7.5)."],
        ["Backend and frontend developers", "API, rules, UI forms, wizard, review screen", "Replace the VBA and form logic (FR-04…FR-14)."],
        ["QA / test analyst", "Automated tests, parity reconciliation", "Needed for T-01…T-04."],
        ["DevOps / platform engineer", "Environments, CI/CD, backups, monitoring", "Needed for NFR-07…NFR-09."],
        ["Information-governance lead / DPO", "DPIA, retention, access policy", "Needed for P-10 and NFR-04."],
    ], [40, 60, 80])]

    # 7.8 Phasing
    s += [H("7.8 Delivery phases and exit criteria", 1),
          para("Sizes are relative (S/M/L), not time estimates; they can only be firmed up once P-01 and P-02 are received."),
          table([
              ["Phase", "Scope", "Exit criteria", "Size"],
              ["0. Discovery", "Collect P-01…P-11; close the §6 gaps; confirm the dashboard tool", "Signed policy v2; VBA and PQ logic documented; DPIA started", "S"],
              ["1. Foundation", "Database schema, reference-data admin, identity/SSO, environments, CI/CD", "Reference data loaded; access roles working; empty schema deployed to test", "M"],
              ["2. Core workflow", "Subject register, requirement wizard, evidence entry with files, derived due date/RAG, corrections", "Golden case T-02 passes end to end", "L"],
              ["3. Controls and publish", "Validation, review gate, atomic publish/rollback, audit log, dashboard views", "Interrupted-publish test passes; dashboard reads published views", "M"],
              ["4. Migration and parity", "Cleansing, load, one parallel monthly cycle", "T-03 differences all explained; business sign-off", "M"],
              ["5. Go-live and extend", "Retire Excel tool (read-only archive); add reminders; onboard next subject type", "Excel no longer used for Staff Management; next domain scoped", "S–M"],
          ], [24, 66, 70, 12])]

    # 7.9 Traceability
    s += [H("7.9 Traceability: each observed problem and the requirement that removes it", 1), table([
        ["Observed problem", "Evidence", "Removed by"],
        ["FM-01 Key drift on name strings", "BR-01, " + figref("reqG"), "FR-01, FR-02, NFR-01"],
        ["FM-02 First-match lookup on history", figref("mcV"), "FR-10"],
        ["FM-03 Destructive updates, no audit", figref("mcU2"), "FR-09, NFR-02"],
        ["FM-04 Workbook open/close coupling", "00:29:29, " + figref("sv"), "NFR-06 (single database)"],
        ["FM-05/06 Unsaved or half-finished publish", "00:27:35, 00:28:24, " + figref("vba"), "FR-14"],
        ["FM-07 Blank → 0 coercion (Managed By)", figref("reqA"), "FR-11, P-07"],
        ["FM-08 Batch stops at a blank row", "00:20:45", "FR-11, FR-12"],
        ["FM-09 Hand-typed due dates", figref("mcU"), "FR-07, P-05"],
        ["FM-10 Hand-picked RAG", figref("mc3"), "FR-08, P-06"],
        ["FM-11 Wrong coverage denominator", figref("nm3"), "FR-19"],
        ["FM-12 Reference-data hygiene", figref("rol"), "FR-17, DM-02"],
        ["FM-13 Screen-dependent formula (Missing)", figref("ctJ"), "FR-05"],
        ["FM-14 VBA nobody can debug", figref("vba") + ", 00:28:09", "NFR-08, P-01"],
        ["FM-15 Unbounded, unsorted tables", figref("reqA"), "NFR-01 (indexed tables)"],
        ["FM-16 Test data in production", figref("nmY"), "FR-16, DM-05"],
        ["SV-01/02 Core flags differ from speech", figref("reqA"), "FR-04, FR-13, P-04, P-08"],
        ["EX-03 Last-updated filled in by hand", figref("vba"), "FR-14"],
        ["Manual monthly chasing", "00:26:18", "FR-15"],
    ], [62, 58, 60])]
    s.append(c["PageBreak"]())
    return s
