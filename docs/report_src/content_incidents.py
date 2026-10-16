# -*- coding: utf-8 -*-
"""Specification content for the Incidents recording (meeting 20260811_135933)."""
import html


def F(t):
    """Formula / identifier in monospace, escaped."""
    return '<font name="DVM" size="6.8">%s</font>' % html.escape(t)


WB = "Incident Management.xlsm"
DOC_TITLE = "Incident Management Compliance Workflow – Reverse-Engineering Specification"
HEADER = "Incident Management Compliance Workflow — Technical Specification (Reverse-Engineered)"
SOURCE = "Source: Teams recording 20260811_135933 (7:16)"
TITLE = "Incident Management Compliance Datastore Update"
SUBTITLE = ("Legacy Excel / Power Query workflow fed by Datix incident exports, reverse-engineered from an operator screen "
            "recording, with a target-state architecture for its replacement")

TITLE_BLOCK = [
    ["<b>Document</b>", "Technical Specification — reverse-engineered legacy workflow (as-is) and target architecture (to-be)"],
    ["<b>Subject workflow</b>", "Monthly update of the <b>Incidents</b> area of the Compliance Dashboard data store, via the Excel “user input tool” "
     "<i>Incident Management.xlsm</i>, which takes an export from <b>Datix</b> (the incident-reporting system)"],
    ["<b>Primary evidence</b>", "Microsoft Teams meeting-20260811_135933-Meeting Recording.mp4 — 1920×1080, 16 fps, 7:16 (436 s); "
     "operator: Andrew Biggins (Provide Wellbeing); audience: Dheeraj"],
    ["<b>Secondary evidence</b>", "…135933…Recording.srt (timed subtitles; <b>matches this video</b>) and two identical TurboScribe .txt transcripts"],
    ["<b>Timestamps</b>", "All [HH:MM:SS] values are positions in the .mp4, cross-checked between the .srt and an offline Whisper re-transcription; "
     "every figure was extracted with ffmpeg at the stated second"],
    ["<b>Companion documents</b>", "Incident_Management_PreBuild_Client_Requirements.pdf (same folder); the Staff Management specification in "
     "01_Staff_Management/ (shared platform design)"],
    ["<b>Report date</b>", "16 October 2026"],
    ["<b>Status</b>", "Draft for business-owner review. <b>The recording stops part-way through the process</b> (operator pauses at 00:07:01), "
     "so §6 and the companion checklist must be closed before build starts"],
]

EXEC_SUMMARY_INTRO = ("<b>What the recording shows.</b> The operator explains how the Incidents compliance area is set up "
                      "(Requirements and Compliance Timeframes tabs), then starts the monthly update: export incident data from Datix, "
                      "paste it into the <i>Datix</i> tab of Incident Management.xlsm, and check the calculated columns. A "
                      "<font name='DVM'>#REF!</font> error appears and the operator pauses the recording at 00:07:01, before fixing it "
                      "and before any refresh or publish step.")

EXEC_SUMMARY = [
    "<b>One subject, ten compliance types.</b> Unlike Staff Management there is no Names tab: the only subject is "
    "“Provide Wellbeing”, with 10 incident types (Serious incident, Moderate/Severe Harm, Fatal, and six “SPC flagged” groups).",
    "<b>Raw source = Datix export.</b> The export itself is never shown: the operator drags the Datix window off the shared screen "
    "(00:05:14) and the screen does not change from 00:04:56 to 00:06:17 while the export and paste are described.",
    "<b>Copy-paste or Power Query?</b> The operator says the export is copied and pasted in, yet the Datix table shows Excel’s "
    "<i>Query</i> ribbon tab, meaning it is a Power Query output. Pasting over a query table is overwritten on the next refresh. This must be clarified (G-03).",
    "<b>The key timeliness formula is broken in two ways.</b> “In set timeframe” switches on the free-text <i>Description</i> instead of "
    "<i>Severity</i>, so it always falls to the default branch, and that branch references a deleted column (<font name='DVM'>#REF!</font>). Every row is affected.",
    "<b>Other defects seen:</b> the category-to-group mapping has no entry for a category present in the data (“Administrative Process "
    "(excluding documentation)”); the Missing column checks its own table and is TRUE for every row; the review frequency is 0.5 months "
    "(“twice a month”) while the operator says it is reviewed monthly.",
    "<b>Sensitive data:</b> the Datix table holds free-text incident narratives about patients and staff names. They are blurred in this "
    "report, and the target design keeps them out of the dashboard store unless the business confirms a need.",
    "<b>Target (§5) and build requirements (§7)</b> reuse the shared platform from the Staff Management specification and add a Datix "
    "ingestion contract, a versioned category map, an effective-dated harm-level SLA table and as-of-date (not TODAY()) calculations.",
]


# --------------------------------------------------------------------------------------------
def section0(c):
    para, H, table, bullets = c["para"], c["H"], c["table"], c["bullets"]
    s = [H("0. Evidence Base, Method &amp; Reading Guide", 0)]
    s += [H("0.1 Source artefacts", 1), table([
        ["Artefact", "What it is", "Used for"],
        ["…20260811_135933-Meeting Recording.mp4", "Teams screen recording, 1920×1080, 16 fps, 7:16. Git-LFS object, 31 MB", "Primary evidence: screenshots, step timings"],
        ["…20260811 135933-Meeting Recording.srt", "Timed subtitles of the <b>same</b> meeting (100 cues). This is the file that was supplied with the Staff Management video by mistake", "Timestamp anchors"],
        ["…135933…Recording.txt and …(1).txt", "Two byte-identical TurboScribe transcripts (3,341 bytes)", "Wording cross-check"],
        ["Author ASR (Whisper small.en, VAD-segmented)", "Independent re-transcription with timings", "Confirms the .srt alignment (e.g. “we download from Datix” at 00:04:43 in both)"],
    ], [52, 78, 50])]
    s += [H("0.2 Method", 1)] + bullets([
        "Frames extracted with <font name='DVM'>ffmpeg -ss</font> at full resolution and cropped to the Excel window (1675×895) or formula bar (1675×410). "
        "Each figure was checked for sharpness and for stability against the frame 0.5 s later, then inspected visually.",
        "A frame-difference scan over the whole video was used to prove where the screen did <i>not</i> change (00:04:56–00:06:17).",
        "<b>Redaction:</b> in every Datix screenshot the <i>Name</i> and <i>Description</i> cells are blurred (red outline). They hold patient "
        "narratives and personal names. Column headers and all other values are left as recorded.",
        "Confidence tags as in the Staff Management spec: <b>[Seen]</b>, <b>[Said]</b>, <b>[Inferred]</b>, <b>[Unknown]</b>.",
    ])
    s += [H("0.3 Relationship to the Staff Management specification", 1),
          para("This tool is a sibling of Staff Management.xlsm (same User input folder, same Requirements / Compliance Timeframes pattern, "
               "same data store). Where the analysis is identical (shared data store, Power Query consolidation, refresh choreography) this "
               "document refers to the Staff Management spec instead of repeating it. Differences are called out explicitly.")]
    s.append(c["PageBreak"]())
    return s


# --------------------------------------------------------------------------------------------
def section1(c):
    para, H, table, figure, figref = c["para"], c["H"], c["table"], c["figure"], c["figref"]
    s = [H("1. Complete File, Workbook &amp; Sheet Inventory", 0)]
    s += [H("1.1 Files and external systems", 1), table([
        ["#", "File / system", "Format", "Location (as seen)", "Role", "Evidence"],
        ["F1", "<b>Incident Management.xlsm</b>", ".xlsm (macro-enabled), 267 KB, modified 28/07/2026 14:46; AutoSave Off",
         "Performance Dashboards and Data › User input (same share as Staff Management, Z:\\… in that recording)",
         "User-input tool for incidents: requirements, timeframes, Datix staging and analysis tabs", figref("exp") + ", " + figref("req")],
        ["F2", "~$Incident Management", "Office lock file, 1 KB, 13:56", "Same folder", "Shows the workbook was already open before recording", figref("exp")],
        ["S1", "<b>Datix</b>", "Incident-reporting system (web dashboard + export)", "Not shown (window moved off-screen)",
         "Raw source of every incident row", "Said 00:04:43–00:06:04"],
        ["F3", "Compliance Data.xlsm (data store)", ".xlsm [Inferred from Staff spec]", "Not shown",
         "Receives the Requirements lookup (“pulled through into the requirements table in the compliance data”)", "Said 00:02:28"],
        ["S2", "Compliance Dashboard", "BI (dial visual)", "Not shown", "Shows % compliance per type; green only at 100%", "Said 00:04:04–00:04:22"],
        ["F4–F14", "Sibling user-input tools", ".xlsm / .xlsx", "Same folder",
         "Audit, Contract, Estates, Hand Hygiene &amp; IPC Audits, Medical Devices, Policy &amp; Procedure, RTT Data (.xlsx), "
         "Sickness/Annual Leave/Vacancy, Survey (.xlsx), Staff Management; plus an Archive folder", figref("exp")],
    ], [9, 30, 28, 36, 50, 27])]
    s += [H("1.2 Worksheet tabs in Incident Management.xlsm", 1),
          para("Order as shown on the tab bar (" + figref("req") + ", " + figref("tabs") + ", " + figref("cat2") + "). Only four tabs were opened."),
          table([
              ["Tab", "Architectural role", "Opened?", "Notes"],
              ["Manage Compliance", "Entry form (as in Staff Management) [Inferred]", "No", "First tab; contradicts “doesn’t work in the same way” unless unused [Gap G-07]"],
              ["Requirements", "<b>Reference</b>: subject × compliance type", "Yes 01:24–02:57", "10 rows, all for Provide Wellbeing"],
              ["Compliance Timeframes", "<b>Reference</b>: catalogue, frequency, grouping, thresholds", "Yes 03:08–04:26", "10 rows"],
              ["Estates · Health and Safety · Safeguarding · IG · Clinical · SPC · Miscellaneous", "Per-group analysis views [Inferred]", "No", "Names match the Datix groupings and SPC types"],
              ["Groupings Pivot · Harm Pivot", "Pivot / reporting outputs [Inferred]", "No", "Probably counts by group and by harm level"],
              ["<b>Datix</b>", "<b>Raw source staging</b> (Power Query table + calculated columns)", "Yes 04:43–07:16", "~70 rows (scroll tip “Row: 70”), 2023–2026 incidents"],
              ["<b>Datix Category</b>", "<b>Reference / lookup</b>: Datix category → dashboard group", "Yes 06:35–06:47", "25 mappings"],
              ["All Notes · Clinical Notes · Information Governance Notes · Health and Safety Notes · Estates Notes · Sa… (more off-screen)", "Notes/commentary per group [Inferred]", "No", "Tab list continues past the visible bar [Gap G-08]"],
          ], [55, 45, 25, 55])]
    s += [H("1.3 Links, queries and macros", 1), table([
        ["Mechanism", "Behaviour observed", "Evidence"],
        ["Power Query on the Datix table", "Excel shows the <i>Query</i> ribbon tab when a Datix cell is active; the source of the query is not shown", figref("dx1")],
        ["Structured-table lookups", "Grouping uses " + F("datix_Category_Table") + "; Missing uses the named range " + F("add_Requirements_Name"), figref("dxR") + ", " + figref("ctI")],
        ["Data-store pull", "Requirements Unique Lookup is said to be pulled into the data store’s requirements table", "Said 00:02:28"],
        ["VBA", "None triggered in the recording. The file is .xlsm and has a Manage Compliance tab, so macros probably exist", "[Unknown] G-07"],
    ], [45, 100, 35])]
    s += [H("1.4 Overview screenshots", 1), figure("rec", 80 * c["mm"]), figure("exp"), figure("tabs")]
    s.append(c["PageBreak"]())
    return s


# --------------------------------------------------------------------------------------------
def section2(c):
    para, H, table, figure, figref = c["para"], c["H"], c["table"], c["figure"], c["figref"]
    mm = c["mm"]
    W = [9, 32, 25, 16, 98]
    hdr = ["Col", "Header", "Type / format", "Origin", "Lineage, rule and evidence"]
    s = [H("2. Exhaustive Column-Level Schema &amp; Data Lineage Catalogue", 0),
         para("Origin codes: <b>RAW</b> = from the Datix export; <b>MAN</b> = typed by the operator; <b>CALC</b> = Excel formula; <b>REF</b> = reference value.")]

    s += [H("2.1 Requirements (requirements table)", 1), table([hdr,
        ["A", "Name", "Text", "MAN", "Always “Provide Wellbeing” (single subject). No Names tab exists [Said 00:01:50]"],
        ["B", "Compliance Type", "Text", "MAN", "Serious incident, Moderate Harm, Severe Harm, Fatal, SPC Flagged – All, SPC Flagged – Clinical, SPC flagged – IG, "
         "SPC flagged – Safeguarding, SPC flagged – Health and Safety, SPC flagged – Estates. Note inconsistent capitalisation “Flagged”/“flagged”"],
        ["C", "Required (T/F)", "Boolean", "MAN", "TRUE for all (“all required to be reported”)"],
        ["D", "Core Requirement", "Text", "MAN", "Core for all"],
        ["E", "Notes", "Text", "MAN", "Empty"],
        ["F", "Unique Lookup", "Text key", "CALC", F('=CONCAT([@Name],"-",[@[Compliance Type]])') + " → “Provide Wellbeing-Serious incident”. Pulled into the data store [Said 00:02:28]. " + figref("reqF")],
        ["G", "Active", "Boolean", "<b>MAN</b>", "Typed constant TRUE (" + figref("reqG") + "); switched off by hand if needed. In Staff Management this column is a lookup to Names"],
    ], W), para("<b>Schema drift between tools:</b> Staff Management’s requirements table has 10 columns (incl. Onboarding, Managed By, "
               "Compliance Timeframe); this one has 7. Power Query consolidation must cope with both shapes [Gap G-09].")]
    s += [figure("req"), figure("reqF", 50 * mm), figure("reqG", 50 * mm)]

    s += [H("2.2 Compliance Timeframes (Compliance_Timeframe_Table)", 1), table([hdr,
        ["A", "Compliance Type", "Text key", "REF", "Same 10 types as Requirements"],
        ["B", "Every x months", "Decimal", "REF", "<b>0.5</b> for all (“Matt set it for twice a month; we only look at this every month”, 00:03:20). " + figref("ctB")],
        ["C", "Core Requirement", "Text", "REF", "Core"],
        ["D", "Compliance Group 1", "Text", "REF", "Operational (one of People / Operational / Clinical)"],
        ["E", "Compliance Group 2", "Text", "REF", "Incidents"],
        ["F–G", "Compliance Group 3, 4", "Text", "REF", "Blank"],
        ["H", "Unique Lookup", "Text", "CALC", F('=CONCAT([@[Compliance Group 1]],"-",[@[Compliance Group 2]],"-",[@[Compliance Group 3]])') +
         " → “Operational-Incidents-” (trailing dash). Staff Management uses Group 1-Group 2 only, so keys differ between tools. " + figref("ctH")],
        ["I", "Missing", "Boolean", "CALC", F('=XLOOKUP(CONCAT(add_Requirements_Name,"-",[@[Compliance Type]]),[Unique Lookup],[Unique Lookup],"")=""') +
         ". <b>Defect:</b> it searches this table’s own Unique Lookup (“Operational-Incidents-”), which can never equal “Name-Type”, so it is TRUE for every row. "
         "In Staff Management the same formula searches requirements_Table. Operator: “not 100% sure what that does” (00:03:49). " + figref("ctI")],
        ["J–N", "Threshold 1–5", "Decimal", "REF", "1, 1, 1, 1, 0.99. Dial is green only at 100%, red below [Said 00:04:08–00:04:19]. " + figref("ctT")],
    ], W)]
    s += [figure("ct1"), figure("ctB", 50 * mm), figure("ctH", 50 * mm), figure("ctI", 50 * mm), figure("ctT")]

    s += [H("2.3 Datix (raw incident staging; Power Query table)", 1),
          para("Blue headers (A–Q) come from the Datix export; orange headers (R–T) are calculated. The header spelling is kept as seen."),
          table([hdr,
              ["A", "ID", "Integer", "RAW · key", "Datix incident reference (e.g. 77, 13073). <b>A real natural key exists</b>, unlike Staff Management"],
              ["B", "Name", "Text", "RAW", "Personal name (redacted here). Blank on the 2023 row"],
              ["C", "Incident date", "Date dd/mm/yyyy", "RAW", "e.g. 28/03/2023, 07/04/2026"],
              ["D", "Reported", "Date", "RAW", "e.g. 05/04/2023, 08/06/2026. Used by T"],
              ["E", "Category", "Text", "RAW", "Datix category, e.g. Personal Property/Data/Information, Administrative Process (excluding documentation). Key for R"],
              ["F", "Sub category", "Text", "RAW", "e.g. Confidentiality Breach, Follow-up Process"],
              ["G", "Description", "Long free text", "RAW · <b>sensitive</b>", "Incident narrative about patients (redacted). Wrapped text makes each row very tall. <b>Wrongly used by T</b>"],
              ["H", "Severity", "Text", "RAW", "Harm level: No Harm, Low Harm (Moderate/Severe Harm, Fatal expected). The column T should use"],
              ["I", "Other service – Division", "Text", "RAW", "e.g. Provide Wellbeing"],
              ["J", "Other Service – Service", "Text", "RAW", "e.g. Vasectomy Service Essex &amp; Suffolk; Carpal Tunnel Service (CORA)"],
              ["K", "How did this incident/near miss occur?", "Text", "RAW", "Not populated on visible rows"],
              ["L", "Service", "Text (hierarchy path)", "RAW", "“Provide Group / Provide Wellbeing / Enterprise Directorate / Provide Wellbeing / Vasectomy Service Essex &amp; Suffolk”"],
              ["M", "Name of External Organisation", "Text", "RAW", "Blank on visible rows"],
              ["N", "Oraganisation Type", "Text", "RAW", "Header misspelt in source; blank"],
              ["O", "Q&amp;S Does the incident need to be discussed at the Incident Review Panel?", "Yes/No", "RAW", "Blank on visible rows. Possibly what the deleted #REF! column held [Inferred]"],
              ["P", "Q&amp;S Date of Incident Review Panel", "Date", "RAW", "Blank"],
              ["Q", "Approval status", "Text (conditional fill)", "RAW", "e.g. “Incident Approved &amp; Record Closed” (green). Used by T"],
              ["R", "Grouping", "Text", "CALC", F('=XLOOKUP([@Category],datix_Category_Table[Datix reference],datix_Category_Table[Category],"")') +
               ". Unmapped categories silently return blank. " + figref("dxR")],
              ["S", "In last 7 months", "Boolean", "CALC", "Formula not shown [Gap G-05]. FALSE for the 2023 row (" + figref("refz") + ")"],
              ["T", "In set timeframe", "Boolean", "CALC", F('=IF([@Reported]<>"",OR((TODAY()-[@Reported])<=SWITCH([@Description],"No Harm",42,"Low Harm",42,"Moderate Harm",42,"Severe Harm",90,"Fatal",365,IF(#REF!="Yes",90,42)),[@[Approval status]]<>"Incident Approved & Record Closed"),"")') +
               ". Shows <b>#REF!</b>. See §4.3. " + figref("dxT")],
          ], [9, 36, 23, 18, 94])]
    s += [figure("dxN"), figure("dx1"), figure("dx2")]

    s += [H("2.4 Datix Category (datix_Category_Table)", 1), table([
        ["Row", "Datix reference", "Category", "Row", "Datix reference", "Category"],
        ["2", "Personal Property/Data/Information", "Information Governance", "15", "Referral Issue", "Clinical"],
        ["3", "Behaviour", "Health and Safety", "16", "Patient Care Issue (DO NOT USE FOR PRESSURE SORES)", "Clinical"],
        ["4", "Documentation", "Information Governance", "17", "Equipment/Medical Device Issue", "Clinical"],
        ["5", "Medication", "Clinical", "18", "Fall Patient", "Clinical"],
        ["6", "Accident/Injury to Service User(s)", "Clinical", "19", "Safeguarding Issue", "Safeguarding"],
        ["7", "Illness", "Clinical", "20", "Person Unwell", "Clinical"],
        ["8", "Diagnostic Process/Procedure", "Clinical", "21", "Wound – not categorised as a Pressure Ulcer’", "Clinical"],
        ["9", "Service User Fall", "Clinical", "22", "Infection Prevention &amp; Control", "Clinical"],
        ["10", "Property", "Estates", "23", "Medical Devices, Equipment, Supplies, Furnishings", "Estates"],
        ["11", "Communication/Consent Issues", "Information Governance", "24", "Accidents/Falls/Injury", "Health and Safety"],
        ["12", "Incidents relating to personal data", "Information Governance", "25", "Contact with Sharps", "Health and Safety"],
        ["13", "Unwell", "Clinical", "26", "Staff Inadequately Trained", "Information Governance <b>(?)</b>"],
        ["14", "Medical Records Issue", "Information Governance", "", "", ""],
    ], [7, 50, 33, 7, 50, 33]),
        para("<b>Observations:</b> (1) “Administrative Process (excluding documentation)”, the category of incident 13073 (" + figref("dxN") + "), "
             "is <b>not in the table</b>, so its Grouping is blank and it drops out of every group count. (2) “Staff Inadequately Trained → Information "
             "Governance” looks wrong and needs confirming. (3) Several near-duplicates map to one group (Fall Patient / Service User Fall / "
             "Accidents/Falls/Injury), which suggests Datix categories changed over time. (4) Six groups exist (Clinical, IG, H&amp;S, Estates, "
             "Safeguarding, plus Miscellaneous as a tab) and match the SPC compliance types.")]
    s += [figure("cat1"), figure("cat2")]
    s.append(c["PageBreak"]())
    return s


# --------------------------------------------------------------------------------------------
STEPS = [
    (1, "00:00:00", "00:01:24", "Introduce the video; start and retry the screen share",
     "On camera: “show how we update the compliance for incidents”. First share (00:00:55–00:01:08) shows File Explorer on the User input folder; "
     "the operator is unsure it is sharing and re-shares (“That’s more like it”, 00:01:24).", "—", "No data change.", ["rec", "exp"]),
    (2, "00:01:24", "00:02:05", "Open the input tool; explain why there is no Names tab",
     "Incident Management.xlsm open on Requirements. “It doesn’t work in the same way as the other ones… we don’t need a names tab… there’s only one name, Provide Wellbeing.”",
     "Read-only.", "None.", ["req"]),
    (3, "00:02:05", "00:02:57", "Walk through Requirements",
     "Selects A3, B3, D (Core), F3 (formula), G5. “All required to be reported… all core… no notes… lookup pulled into the compliance data… active all the time, can switch off manually.”",
     "Read-only.", "None.", ["reqF", "reqG"]),
    (4, "00:02:57", "00:04:26", "Walk through Compliance Timeframes",
     "Opens the tab; selects A, B2 (0.5), C2, D2, E2, H4 (formula), I2 (Missing formula), J:N thresholds.",
     "Read-only.", "None. Spoken frequency (monthly) differs from the stored value (0.5).", ["ct1", "ctB", "ctH", "ctI", "ctT"]),
    (5, "00:04:26", "00:04:43", "Scroll the tab bar to Datix",
     "“Let me go through the process of how we update it.” Uses “See all sheets” scrolling past Estates…Harm Pivot.", "—", "None.", ["tabs"]),
    (6, "00:04:43", "00:05:00", "Open the Datix tab",
     "Sheet opens scrolled to a 2026 row (ID 13073); operator jumps to the top row (ID 77, 2023) and scrolls right to N:T and back. “We download from Datix all of the incident data and load it into there.”",
     "Read-only.", "None.", ["dxN", "dx1", "dx2"]),
    (7, "00:05:00", "00:06:18", "Export from Datix and paste (described, <b>not shown</b>)",
     "“I’ll pull this over to here” (00:05:14) moves the Datix window off the shared screen. “We go into Datix… the dashboard… pull out the export… "
     "and then we just copy and paste it into here” (00:05:26–00:06:04). Frame-difference scan: no screen change from 00:04:56 to 00:06:17.",
     "Datix export → Datix tab A:Q (claimed). Paste type, range and whether existing rows are replaced are unknown.",
     "Not observable: the Datix tab shows the same rows before and after.", ["dx3"]),
    (8, "00:06:18", "00:06:48", "Explain the Grouping lookup and open Datix Category",
     "Selects F2, scrolls to R2 (Grouping formula). “It looks at the category… references that with a table… puts it into one of our categories.” "
     "Opens Datix Category, scrolls to row 26, returns.", "Datix[Category] → datix_Category_Table → Datix[Grouping].",
     "None. Row 2 Grouping = Information Governance (correct).", ["dxR", "refz", "cat1", "cat2"]),
    (9, "00:06:48", "00:07:01", "Check the calculated column; find #REF!",
     "“What we generally do when we copy it in is we’ll check that column. Oh look, #REF!… that needs fixing.” Selects T2 showing the In set timeframe formula.",
     "—", "T2 (In set timeframe) = <b>#REF!</b>; Grouping is fine. The fix is not shown.", ["dxT"]),
    (10, "00:07:01", "00:07:16", "Pause the recording",
     "“I’m just going to pause the recording there.” The video ends. No fix, save, refresh or publish is recorded.", "—", "—", ["end"]),
]


def section3(c):
    para, H, table, figure = c["para"], c["H"], c["table"], c["figure"]
    s = [H("3. Chronological Step-by-Step Operator Workflow", 0),
         para("Ten steps cover the whole 7:16 recording. Steps 7 and 9 contain the actual update; both are only partly observable."),
         table([["Step", "Window", "Action"]] + [[str(x[0]), x[1] + "–" + x[2], x[3]] for x in STEPS], [10, 34, 136]),
         c["PageBreak"]()]
    for n, a, b, title, act, mp, mut, figs in STEPS:
        s += [H("Step %d [%s – %s]: %s" % (n, a, b, title.replace("<b>", "").replace("</b>", "")), 1),
              table([["<b>Action performed</b>", act], ["<b>Source → target</b>", mp], ["<b>State mutation (before → after)</b>", mut]],
                    [38, 142], head=False, zebra=False)]
        for f in figs:
            s.append(figure(f))
        s.append(c["Spacer"](1, 6))
    s.append(c["PageBreak"]())
    return s


# --------------------------------------------------------------------------------------------
def section4(c):
    para, H, table, figref = c["para"], c["H"], c["table"], c["figref"]
    s = [H("4. Data Quality Checks, Manual Exceptions &amp; Edge Cases", 0)]
    s += [H("4.1 Business rules visible in the tool", 1), table([
        ["ID", "Rule", "Where", "Evidence"],
        ["BR-01", "Incident identity = Datix ID", "Datix!A", figref("dx1")],
        ["BR-02", "Datix category → dashboard group via a lookup table", "Datix!R, datix_Category_Table", figref("dxR")],
        ["BR-03", "Allowed days by harm level: No/Low/Moderate Harm 42, Severe Harm 90, Fatal 365; otherwise 90 if a (deleted) flag = “Yes”, else 42", "Datix!T", figref("dxT")],
        ["BR-04", "An incident counts as “in set timeframe” if (today − Reported) ≤ allowed days <b>or</b> it is not yet “Incident Approved &amp; Record Closed”", "Datix!T", figref("dxT")],
        ["BR-05", "A reporting window of the last 7 months", "Datix!S (formula not shown)", figref("refz")],
        ["BR-06", "All 10 types are required, core and active for the one subject", "Requirements", figref("req")],
        ["BR-07", "Dial: green only at 100% (Threshold 1–4 = 1), red otherwise (Threshold 5 = 0.99)", "Compliance Timeframes J:N", figref("ctT")],
        ["BR-08", "After pasting, the operator checks the calculated columns for errors", "Manual check", "Said 00:06:41"],
    ], [12, 82, 46, 40])]
    s += [H("4.2 Manual steps and exceptions", 1), table([
        ["ID", "Exception", "Handling", "Evidence"],
        ["EX-01", "Datix export must be produced by hand from the Datix dashboard", "Operator exports and copies; off-screen", "00:05:26–00:06:04"],
        ["EX-02", "#REF! in a calculated column", "Spotted by eye after paste; fix not recorded", figref("dxT")],
        ["EX-03", "Requirements can be switched off manually", "Edit Active to FALSE", "Said 00:02:41"],
        ["EX-04", "Screen-share does not follow the window", "Datix window moved to another screen", "Said 00:05:06–00:05:19"],
    ], [12, 62, 66, 40])]
    s += [H("4.3 Spoken vs. visual discrepancies and formula defects", 1), table([
        ["ID", "Spoken / intended", "On screen / in data", "Impact"],
        ["SV-01", "“We just copy and paste it into here” (00:06:01)", "Datix table is a Power Query output (Query ribbon tab)", "A paste over a query table is replaced at the next refresh, or the paste goes to a hidden source sheet; the real path is unknown"],
        ["SV-02", "“We only look at this every month” (00:03:20)", "Every x months = 0.5 for all types", "Due-date and compliance maths run on a half-month cycle the business does not follow"],
        ["SV-03", "“We’ll check that column” after describing Grouping (00:06:48)", "The #REF! is in <i>In set timeframe</i> (T), not Grouping (R)", "The check the operator relies on is not the column at fault"],
        ["SV-04", "Missing “just checks that there’s a requirement” (00:03:49)", "Formula searches its own table, so it is TRUE for all rows", "The column gives no information"],
        ["SV-05", "“Doesn’t work in the same way… no Names tab” (00:01:38)", "A Manage Compliance tab still exists, and the named range add_Requirements_Name is referenced", "Leftovers from cloning the Staff tool; behaviour unknown"],
        ["FD-01", "T should vary by harm level", "SWITCH tests [@Description] (free text), never [@Severity]", "Always takes the default branch, so the 42/90/365-day rule never applies"],
        ["FD-02", "Default branch tests a flag", "IF(#REF!=\"Yes\",…): the referenced column was deleted", "Every row shows #REF!; any count or % built on T fails"],
        ["FD-03", "Timeliness should be stable", "TODAY() − Reported", "The value changes every day and cannot be reproduced for a past month"],
        ["FD-04", "Compliance means closed within the time limit [Inferred]", "OR(within limit, not closed)", "Open incidents always count as “in timeframe”, even when overdue, and every closed incident older than its limit counts as out of timeframe even if it was closed in time (TODAY() is used, not the closure date). The logic may be inverted (G-04)"],
    ], [12, 50, 56, 62])]
    s += [H("4.4 Hidden failure modes", 1), table([
        ["ID", "Failure mode", "Mechanism", "Severity"],
        ["FM-01", "<b>Silent unmapped categories</b>", "XLOOKUP returns blank for a category missing from the map (e.g. “Administrative Process (excluding documentation)”), so the incident disappears from group totals", "High"],
        ["FM-02", "<b>Broken timeliness flag</b>", "FD-01 + FD-02: every row #REF!", "High"],
        ["FM-03", "<b>Paste vs query conflict</b>", "SV-01: data may be lost at refresh, or stale data published", "High"],
        ["FM-04", "<b>Non-reproducible results</b>", "TODAY() in T (and probably S)", "Medium"],
        ["FM-05", "<b>Full-replace imports</b>", "If each paste replaces all rows, status history (open → closed) is lost; if it appends, duplicates appear. No key-based merge is visible", "High"],
        ["FM-06", "<b>Sensitive data in a shared workbook</b>", "Patient narratives and names in a file on a shared drive, copied into a reporting tool", "High (IG)"],
        ["FM-07", "<b>Schema drift between tools</b>", "Different Requirements columns and Unique Lookup formulas from Staff Management", "Medium"],
        ["FM-08", "<b>Mapping table drift</b>", "Datix categories change over time; near-duplicates already present", "Medium"],
        ["FM-09", "<b>Process not recorded end to end</b>", "Fix, refresh and publish steps were not shown", "Medium"],
    ], [12, 40, 108, 20])]
    s.append(c["PageBreak"]())
    return s


# --------------------------------------------------------------------------------------------
def section5(c):
    para, H, table, bullets, code = c["para"], c["H"], c["table"], c["bullets"], c["code"]
    s = [H("5. Target Modern System Architecture Blueprint", 0),
         para("Incidents run on the <b>same platform</b> as Staff Management (spec 01, §5): staged ingestion, review gate, append-only "
              "ledger, atomic publication and audit. Below is what is <b>specific to incidents</b>.")]
    s += [H("5.1 Ingestion of Datix data", 1)] + bullets([
        "<b>Preferred:</b> scheduled pull from the Datix API or a scheduled Datix report delivered as CSV to a secure drop folder. "
        "<b>Fallback:</b> the operator uploads the export file in the web UI. No copy-paste in either case.",
        "<b>Header contract</b> for the export (columns A–Q in §2.3), versioned. Unknown or missing columns fail the file before staging.",
        "<b>Cell checks:</b> ID integer and unique in the file; dates parsed as dd/mm/yyyy; Severity in the harm list; Approval status in the status list; "
        "Category must exist in the category map, otherwise the row goes to the exception queue (fixes FM-01).",
        "<b>Data minimisation:</b> drop Description and Name at ingestion unless the business confirms a use (fixes FM-06). Keep the Datix ID as the link back to Datix.",
    ])
    s += [H("5.2 Data model additions", 1), table([
        ["Table", "Key columns", "Replaces"],
        ["<b>incident</b>", "incident_id (PK, = Datix ID), incident_date, reported_date, datix_category, sub_category, severity_id, division, service, approval_status, review_panel_flag, review_panel_date", "Datix tab"],
        ["<b>incident_version</b>", "incident_id, import_batch_id, row hash, values as imported; new version only when something changed", "Repeated full pastes (keeps status history, fixes FM-05)"],
        ["<b>ref_datix_category_map</b> (versioned)", "datix_category, group_code, valid_from, valid_to, approved_by", "Datix Category tab"],
        ["<b>ref_harm_sla</b> (versioned)", "severity, allowed_days (42 / 90 / 365 …), valid_from, valid_to", "SWITCH(…) constants in T"],
        ["<b>ref_compliance_type</b> / policy", "Shared tables from spec 01; frequency stored as an explicit cadence (monthly) instead of 0.5", "Compliance Timeframes"],
        ["<b>requirement</b>", "Shared table; subject = Provide Wellbeing (organisation subject type)", "Requirements tab"],
    ], [40, 105, 35])]
    s += [H("5.3 Rules as deterministic SQL (as-of date, not TODAY())", 1), code(
        "CREATE VIEW mart.v_incident_timeliness AS\n"
        "SELECT i.incident_id, s.as_of_date,\n"
        "       g.group_code,                                   -- NULL only if mapping missing (blocked at ingestion)\n"
        "       (s.as_of_date - i.reported_date)              AS age_days,\n"
        "       sla.allowed_days,\n"
        "       (i.approval_status = 'Incident Approved & Record Closed') AS is_closed,\n"
        "       CASE WHEN i.approval_status = 'Incident Approved & Record Closed'\n"
        "            THEN i.closed_date - i.reported_date <= sla.allowed_days   -- closed within limit\n"
        "            ELSE s.as_of_date - i.reported_date <= sla.allowed_days    -- still open, not yet overdue\n"
        "       END                                           AS in_set_timeframe,   -- rule to confirm (G-04)\n"
        "       i.incident_date >= s.as_of_date - INTERVAL '7 months'  AS in_last_7_months\n"
        "FROM core.incident i\n"
        "CROSS JOIN mart.snapshot s                          -- the publication's as-of date\n"
        "JOIN ref.harm_sla sla ON sla.severity = i.severity\n"
        " AND s.as_of_date BETWEEN sla.valid_from AND coalesce(sla.valid_to,'infinity')\n"
        "LEFT JOIN ref.datix_category_map g ON g.datix_category = i.datix_category\n"
        " AND s.as_of_date BETWEEN g.valid_from AND coalesce(g.valid_to,'infinity');")]
    s += bullets([
        "Severity drives the SLA (fixes FD-01); there is no reference to a deleted column (FD-02); the as-of date makes every month reproducible (FD-03).",
        "The OR/AND meaning of “in set timeframe” is written once, tested and approved (FD-04, G-04).",
        "Compliance % per type = in-timeframe incidents ÷ applicable incidents, per group and harm level, for the snapshot; the dial reads the stored thresholds.",
    ])
    s += [H("5.4 Human-in-the-loop and publication", 1)] + bullets([
        "<b>Exception queue:</b> unmapped category, unknown severity, duplicate ID, date errors. The operator maps a new category once (with approval) and it applies from then on.",
        "<b>Import diff:</b> before publishing, show new, changed (e.g. status open → closed) and disappeared incidents against the last import.",
        "<b>Atomic publish</b> with an as-of date and snapshot ID, exactly as in spec 01 §5.6; the dashboard reads only published snapshots.",
        "<b>Access:</b> incident data restricted to roles approved by the IG lead; the dashboard shows only counts and percentages.",
    ])
    s.append(c["PageBreak"]())
    return s


# --------------------------------------------------------------------------------------------
def section6(c):
    H, table = c["H"], c["table"]
    s = [H("6. Gap &amp; Ambiguity Register", 0), table([
        ["ID", "Timestamp", "Gap / ambiguity", "Why it matters", "Ask"],
        ["G-01", "00:07:01–end", "Recording paused before the #REF! fix, save, refresh and publish", "The second half of the process is unknown", "Record the rest of the monthly update"],
        ["G-02", "00:05:14–00:06:17", "Datix export steps happened off-screen (report used, filters, date range, file format)", "Defines the ingestion contract", "Show or document the Datix export"],
        ["G-03", "00:04:47, 00:06:01", "Datix table is a query output but the operator describes copy-paste", "Determines where data actually lands and whether a refresh overwrites it", "Share the Power Query (M) behind the Datix table"],
        ["G-04", "00:06:53", "Intended meaning of “In set timeframe” (OR with not-closed); which date (Reported vs Incident) starts the clock", "Core compliance rule", "Business owner to define"],
        ["G-05", "00:06:24", "Formula of “In last 7 months” not shown", "Reporting window rule", "Share formula / define rule"],
        ["G-06", "00:06:53", "Which column did #REF! point to (deleted flag tested for “Yes”)", "Needed to restore the 90-day default rule", "Identify from file history"],
        ["G-07", "tab bar", "Manage Compliance tab and any VBA not opened", "May hold update logic", "Share workbook and VBA"],
        ["G-08", "00:04:36, 00:06:44", "Estates…SPC, Miscellaneous, both Pivots and the Notes tabs not opened; tab list continues off-screen", "Outputs and manual commentary unknown", "Walk through or share"],
        ["G-09", "00:02:31", "Requirements schema differs from Staff Management", "Consolidation in the data store", "Share Compliance Data.xlsm queries"],
        ["G-10", "00:03:20", "Frequency 0.5 months vs monthly review", "Due dates and cadence", "Confirm cadence"],
        ["G-11", "00:06:44", "“Staff Inadequately Trained → Information Governance” mapping; missing “Administrative Process (excluding documentation)”", "Group totals", "Approve full category map"],
        ["G-12", "00:02:13", "Definition of “SPC flagged” types and how they are counted", "Six of the ten compliance types", "Explain SPC flagging"],
        ["G-13", "00:04:04", "How the dial percentage is calculated per type", "Dashboard parity", "Share dashboard measures"],
        ["G-14", "00:04:45", "Row count and date range of the Datix table (~70 rows, 2023–2026 seen)", "Volume and history needs", "Confirm export scope"],
    ], [11, 22, 60, 42, 45])]
    s.append(c["PageBreak"]())
    return s


# --------------------------------------------------------------------------------------------
def section7(c):
    para, H, table, figref = c["para"], c["H"], c["table"], c["figref"]
    W = [13, 52, 115]
    s = [H("7. What Is Required to Build the Modern System", 0),
         para("Requirements specific to incidents, each with the reason it is needed. Platform requirements (identity, audit, review gate, atomic "
              "publish, SSO, backups, CI/CD) are shared with Staff Management and listed in spec 01 §7; they are not repeated here. "
              "Priority: <b>M</b> must, <b>S</b> should, <b>C</b> could. The full client checklist is in "
              "<b>Incident_Management_PreBuild_Client_Requirements.pdf</b>.")]
    s += [H("7.1 Prerequisites from the business", 1), table([
        ["ID", "What is required", "Why it is required"],
        ["P-01", "The rest of the process, recorded or written down (fix, save, refresh, publish)", "The video stops at 00:07:01 (" + figref("end") + "); half the workflow is unknown (G-01)."],
        ["P-02", "Datix export definition and a sample export file (anonymised)", "The export happened off-screen (" + figref("dx3") + "); it defines the ingestion contract (G-02)."],
        ["P-03", "The workbook and its Power Query (M) code", "The Datix table is a query output but is described as a paste (SV-01, G-03)."],
        ["P-04", "Approved rules: SLA days per harm level, start date, OR/AND meaning, 7-month window", "The current formula is broken and its meaning is unclear (FD-01…04, G-04, G-05)."],
        ["P-05", "Approved category map, including currently unmapped categories", "Unmapped categories silently drop out of totals (FM-01, G-11)."],
        ["P-06", "Decision on which Datix fields may be stored (Description, Name)", "Patient narratives and names are in the sheet (FM-06)."],
        ["P-07", "Datix integration route (API access or scheduled report) and licence", "Removes manual export and copy-paste (EX-01)."],
    ], W)]
    s += [H("7.2 Functional requirements", 1), table([
        ["ID", "Requirement (priority)", "Why it is required"],
        ["FR-I01", "Automated or uploaded Datix ingestion with header and cell validation (M)", "Replaces the off-screen manual export and paste (EX-01, SV-01)."],
        ["FR-I02", "Key-based merge on Datix ID with version history (M)", "Keeps status changes and avoids duplicates or losses between imports (FM-05)."],
        ["FR-I03", "Versioned category map with an exception queue for unmapped values (M)", "Fixes silent blank groupings (FM-01, " + figref("cat2") + ")."],
        ["FR-I04", "Effective-dated harm-level SLA table driving timeliness (M)", "Replaces the SWITCH on the wrong column and the #REF! default (FD-01, FD-02, " + figref("dxT") + ")."],
        ["FR-I05", "As-of-date calculations for every published month (M)", "TODAY() makes results change daily (FD-03)."],
        ["FR-I06", "Import diff and review before publishing (M)", "The only check today is looking at a column by eye (BR-08), and it is the wrong column (SV-03)."],
        ["FR-I07", "Group and harm-level views replacing the Estates…SPC tabs and pivots (S)", "These tabs feed the dashboard today but were not shown (G-08)."],
        ["FR-I08", "Notes/commentary per group as records with author and date (S)", "Notes tabs exist per group (" + figref("cat2") + "); content and use to be confirmed."],
        ["FR-I09", "Monthly cadence stored explicitly (M)", "0.5 months vs “we only look at this every month” (SV-02)."],
        ["FR-I10", "Single-subject support (organisation) in the shared requirement model (M)", "Incidents have one subject, Provide Wellbeing (00:01:50)."],
    ], W)]
    s += [H("7.3 Non-functional requirements", 1), table([
        ["ID", "Requirement", "Why it is required"],
        ["NFR-I01", "Data minimisation and role-based access to incident records", "Sensitive patient narratives (FM-06); NHS DSP Toolkit / UK GDPR."],
        ["NFR-I02", "Datix credentials held in a secrets store; read-only API account", "An automated pull needs safe credentials."],
        ["NFR-I03", "Reproducible monthly snapshots", "Past dashboard figures must be re-creatable (FD-03)."],
    ], W)]
    s += [H("7.4 Testing", 1), table([
        ["ID", "Test", "Why it is required"],
        ["T-I01", "Golden rows: ID 77 (No Harm, reported 05/04/2023, closed, IG) and ID 13073 (Low Harm, reported 08/06/2026, unmapped category)", "Two real cases seen in the video with known expected groupings and errors."],
        ["T-I02", "SLA boundary tests at 42/90/365 days for each harm level, open and closed", "The core rule (BR-03, BR-04)."],
        ["T-I03", "Re-import tests: same file twice (no change), status change, deleted incident", "Proves the merge (FR-I02)."],
        ["T-I04", "Parity: one month vs the Excel dashboard once #REF! is fixed", "Shows the new numbers match or that each difference is a known fix."],
    ], W)]
    s += [H("7.5 Traceability", 1), table([
        ["Observed problem", "Evidence", "Removed by"],
        ["FM-01 Unmapped categories", figref("dxN") + ", " + figref("cat2"), "FR-I03, P-05"],
        ["FM-02 / FD-01 / FD-02 Broken timeliness flag", figref("dxT"), "FR-I04, P-04"],
        ["FM-03 / SV-01 Paste vs query", figref("dx1"), "FR-I01, P-03"],
        ["FM-04 / FD-03 TODAY()", figref("dxT"), "FR-I05"],
        ["FM-05 Full-replace imports", "00:06:01", "FR-I02"],
        ["FM-06 Sensitive data", figref("dx1"), "NFR-I01, P-06"],
        ["SV-02 Frequency 0.5", figref("ctB"), "FR-I09"],
        ["SV-04 Missing always TRUE", figref("ctI"), "Shared missing-requirements view (spec 01 FR-05)"],
        ["G-01 Unrecorded second half", figref("end"), "P-01"],
    ], [62, 58, 60])]
    s.append(c["PageBreak"]())
    return s


def appendix(c):
    H, table, FIGS = c["H"], c["table"], c["FIGS"]
    E = html.escape
    s = [H("Appendix A. Figure Index", 0),
         table([["Fig", "Time", "File › Tab", "Shows"]] + [[str(i), f[1], E(f[2]) + " › " + E(f[3]), E(f[4])[:150] + ("…" if len(f[4]) > 150 else "")]
                                                        for i, f in enumerate(FIGS, 1)], [8, 16, 44, 112])]
    s += [H("Appendix B. Key timestamped utterances", 0), table([
        ["Time", "Utterance (lightly cleaned)"],
        ["00:00:04", "I’m going to make a video now to show how we update the compliance for incidents."],
        ["00:01:38", "It doesn’t work in the same way as the other ones… We don’t need a names tab for this one."],
        ["00:01:54", "There’s only one name and that’s Provide Wellbeing."],
        ["00:02:05", "This is the requirements table, which we can build manually."],
        ["00:02:28", "There’s a lookup there which gets pulled through into the requirements table in the compliance data."],
        ["00:03:20", "Matt set it for twice a month. We only look at this every month."],
        ["00:03:49", "Missing, again I’m not 100% sure what that does."],
        ["00:04:08", "If it’s 100% it’s going to show green; anything less than that, it’s going to show red."],
        ["00:04:43", "We download from Datix all of the incident data and load it into there."],
        ["00:05:14", "I’ll pull this over to here."],
        ["00:05:26", "We just go into Datix… into the dashboard… pull out the export…"],
        ["00:06:01", "…and then we just copy and paste it into here."],
        ["00:06:20", "There’s a column there that puts it into a grouping. It looks at the category… references that with a table."],
        ["00:06:48", "We’ll check that column. Oh look, #REF!… that needs fixing."],
        ["00:07:01", "I’m just going to pause the recording there."],
    ], [18, 162])]
    return s
