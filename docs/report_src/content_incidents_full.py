# -*- coding: utf-8 -*-
"""Specification content for the full Incidents recording (meeting 20260814_102641)."""
import html


def F(t):
    return '<font name="DVM" size="6.8">%s</font>' % html.escape(t)


DOC_TITLE = "Incident Management (Full Process) – Reverse-Engineering Specification"
HEADER = "Incident Management Compliance — Full Monthly Process — Technical Specification (Reverse-Engineered)"
SOURCE = "Source: Teams recording 20260814_102641 (10:00)"
TITLE = "Incident Management — Full Monthly Process"
SUBTITLE = ("The complete incidents update from Datix export to data store, including the pivots, SPC sheets and compliance table "
            "that the earlier recording (spec 02) did not reach")

TITLE_BLOCK = [
    ["<b>Document</b>", "Technical Specification — reverse-engineered legacy workflow (as-is), target design and build requirements"],
    ["<b>Subject workflow</b>", "Incidents compliance (Operational › Incidents) via <i>Incident Management.xlsm</i>: Datix export → Datix tab → Groupings and Harm "
     "pivots → per-group SPC sheets → Manage Compliance (10 rows) → Compliance Data.xlsm"],
    ["<b>Primary evidence</b>", "Meeting with Andrew R. Biggins-20260814_102641-Meeting Recording.mp4 — 1920×1080, 16 fps, 10:00 (601 s); camera off. "
     "The first video recorded on 14/08/2026"],
    ["<b>Relationship to spec 02</b>", "Spec 02 (recording 20260811 135933) stopped at 07:01 before the fix, pivots and publish. This recording covers the "
     "whole process and answers several of spec 02’s gaps (§0.3). Read both together"],
    ["<b>Companion documents</b>", "Incident_Full_PreBuild_Client_Requirements.pdf (same folder); 02_Incident_Management/"],
    ["<b>Report date</b>", "16 October 2026"],
    ["<b>Status</b>", "Draft for business-owner review. Datix incident descriptions and Teams notifications naming staff are blurred"],
]

EXEC_SUMMARY_INTRO = ("<b>What the recording shows.</b> The operator sets out the Requirements and Compliance Timeframes tabs, shows the Datix "
                      "export live (RLDatix web dashboard → widget → Export → Excel), explains how the Datix tab assigns groups and timeframes, "
                      "then walks through the Groupings and Harm pivots, the SPC sheets per group (rows dragged down each month), the notes tabs "
                      "and the Manage Compliance table whose 10 rows are pasted into the data store.")

EXEC_SUMMARY = [
    "<b>Ten compliance rows:</b> four harm-based (Serious incident, Moderate Harm, Severe Harm, Fatal) counted from the Datix tab, and six "
    "SPC-based (All, Clinical, IG, Safeguarding, Health and Safety, Estates) read from the per-group SPC sheets for last month.",
    "<b>The #REF! in spec 02 is explained.</b> On 14/08 the In set timeframe formula is intact; its default branch tests "
    "<i>“Q&amp;S Does the incident need to be discussed at the Incident Review Panel?” = “Yes” → 90 days, else 42</i>. The 11/08 file had lost that column. "
    "The SWITCH on <i>Description</i> instead of <i>Severity</i> is still present, so the harm-specific limits never apply.",
    "<b>Inconsistent logic between tabs:</b> the All Notes FILTER and the Manage Compliance COUNTIFS use <i>Severity</i>, but the timeframe uses "
    "<i>Description</i>; Moderate Harm’s RAG uses 3 for red while Severe Harm uses 2.",
    "<b>Live result 14/08/2026:</b> Moderate Harm non-compliant (“1 Moderate Harm incident(s) in Last 6 Weeks – Datix: 13135”, RAG 3); all others 10.",
    "<b>Manual steps:</b> export from Datix, paste, drag SPC rows down, refresh pivots, copy 10 rows to the data store, Last Updated by hand, save, refresh twice.",
    "<b>Operator knowledge gaps:</b> “This was all set up by Matt. We’ve not made any changes”; “I don’t know what that table is”; 0.5 months “doesn’t make any difference”.",
]


def section0(c):
    para, H, table, bullets = c["para"], c["H"], c["table"], c["bullets"]
    s = [H("0. Evidence Base, Method &amp; Reading Guide", 0)]
    s += [H("0.1 Source artefacts", 1), table([
        ["Artefact", "What it is", "Used for"],
        ["…20260814_102641-Meeting Recording.mp4", "Teams recording, 10:00, Git-LFS object 40 MB", "Screenshots, timings"],
        ["…20260814 102641-Meeting Recording.srt / .txt", "Timed subtitles and transcript", "Timestamps and wording"],
    ], [52, 78, 50])]
    s += [H("0.2 Method and redaction", 1)] + bullets([
        "Figures matched to verified frames at 0.25 s steps. Datix Description cells (patient narratives) and Teams pop-ups naming staff are blurred.",
    ])
    s += [H("0.3 Gaps in spec 02 answered by this recording", 1), table([
        ["Spec 02 gap", "Answer from this recording", "Evidence"],
        ["G-01 second half not recorded", "Pivots, SPC sheets, notes, Manage Compliance and paste are shown", "§3 steps 7–11"],
        ["G-02 Datix export off-screen", "RLDatix › Capture › Dashboard › Provide Wellbeing Dashboard › widget menu › Export › Excel → DatixWebReport (n).xlsx", c["figref"]("web") + ", " + c["figref"]("dl")],
        ["G-05 In last 7 months formula", F('=IF([@Reported]<>"",(TODAY()-[@Reported])<=217,"")'), c["figref"]("dxS")],
        ["G-06 column behind #REF!", "“Q&amp;S Does the incident need to be discussed at the Incident Review Panel?” (Yes → 90 days, else 42)", c["figref"]("dxT")],
        ["G-08 tabs not opened", "Groupings Pivot, Harm Pivot, SPC sheets per group, All Notes and group Notes tabs shown", c["figref"]("gp") + ", " + c["figref"]("spc") + ", " + c["figref"]("notesJ")],
        ["G-07 Manage Compliance", "It is the output table (10 rows), filled by formulas, copied by hand", c["figref"]("mc")],
    ], [42, 98, 40])]
    s.append(c["PageBreak"]())
    return s


def section1(c):
    para, H, table, figure, figref = c["para"], c["H"], c["table"], c["figure"], c["figref"]
    s = [H("1. Complete File, Workbook &amp; Sheet Inventory", 0), table([
        ["#", "File / system", "Role", "Evidence"],
        ["S1", "<b>RLDatix</b> (providecic.gateway.prod-uk.datixcloudiq.co.uk)", "Incident system; Provide Wellbeing Dashboard; export to Excel", figref("web")],
        ["F1", "DatixWebReport (n).xlsx", "Raw export (Protected View); sheet “Datix listing report”", figref("webrep")],
        ["F2", "<b>Incident Management.xlsm</b>", "Tool: Manage Compliance, Requirements, Compliance Timeframes, Estates, Health and Safety, Safeguarding, IG, Clinical, SPC, Miscellaneous, Groupings Pivot, Harm Pivot, Datix, Datix Category, All Notes, Clinical / IG / H&amp;S / Estates / Safeguarding Notes", figref("mc")],
        ["F3", "<b>Compliance Data.xlsm</b>", "Data store (UNABLE TO REFRESH banner)", figref("cdd")],
    ], [8, 55, 85, 32]), figure("rec", 70 * c["mm"])]
    s.append(c["PageBreak"]())
    return s


def section2(c):
    para, H, table, figure, figref = c["para"], c["H"], c["table"], c["figure"], c["figref"]
    W = [18, 40, 122]
    s = [H("2. Column-Level Schema &amp; Formula Catalogue", 0),
         para("Columns already catalogued in spec 02 §2 (Requirements, Compliance Timeframes, Datix A–T, Datix Category) are not repeated; below are the "
              "formulas confirmed or newly seen here.")]
    s += [H("2.1 Reference tabs", 1), table([
        ["Cell", "Meaning", "Formula / value"],
        ["Req A:G", "10 incident types, all Required, Core, Active", figref("req")],
        ["CT B", "Every x months", "0.5 (“doesn’t make any difference… we only update it once a month”)"],
        ["CT H", "Unique Lookup", F('=CONCAT(Group1,"-",Group2,"-",Group3)') + " → “Operational-Incidents-”"],
        ["CT I", "Missing", "Always TRUE (searches own table)"],
        ["CT J:N", "Thresholds", "1, 1, 1, 1, 0.99"],
    ], W), figure("req"), figure("ct"), figure("ctB"), figure("ctH"), figure("ctI"), figure("thr")]
    s += [H("2.2 Datix tab (calculated columns)", 1), table([
        ["Col", "Header", "Formula"],
        ["R", "Grouping", F('=XLOOKUP([@Category],datix_Category_Table[Datix reference],datix_Category_Table[Category],"")')],
        ["S", "In last 7 months", F('=IF([@Reported]<>"",(TODAY()-[@Reported])<=217,"")')],
        ["T", "In set timeframe", F('=IF([@Reported]<>"",OR((TODAY()-[@Reported])<=SWITCH([@Description],"No Harm",42,"Low Harm",42,"Moderate Harm",42,"Severe Harm",90,"Fatal",365,IF([@[Q&S Does the incident need to be discussed at the Incident Review Panel?]]="Yes",90,42)),[@[Approval status]]<>"Incident Approved & Record Closed"),"")')],
    ], [10, 30, 140]), figure("dxT"), figure("dxR"), figure("dxS"), figure("cat")]
    s += [H("2.3 Pivots, SPC sheets and notes", 1), table([
        ["Object", "Content", "Formula / rule"],
        ["Groupings Pivot", "Count of Grouping by year/month", figref("gp")],
        ["Harm Pivot", "Count by harm level by year/month", "Not opened in detail"],
        ["Estates / H&amp;S / Safeguarding / IG / Clinical / SPC / Miscellaneous", "Monthly count per group since 01/04/2022, mean, LCL, UCL, SPC rule columns",
         F("C63 =IFERROR(GETPIVOTDATA(\"Grouping\",'Groupings Pivot'!$A$3,\"Grouping\",$B$2,\"Months (Incident date)\",MONTH(B63),\"Years (Incident date)\",YEAR(B63)),…)") + "; " + F("AC6 UCL =AC3+(AC4*3)") + "; LCL negative for counts"],
        ["SPC flag cell", "Show the month only if a rule fires", F('D57 =IF(P54=2,"",IF(AND(T57=0,P57=0,K57=0,Z57=0),"",C57))')],
        ["All Notes", "Datix IDs per type in timeframe; text used in Manage Compliance notes", F('J2 =IFERROR(FILTER(Datix_2[ID],(Datix_2[Severity]="Moderate Harm")*(Datix_2[In set timeframe]=TRUE)),"Moderate harm not found")')],
    ], [38, 62, 80]), figure("spc"), figure("spcG"), figure("d57"), figure("notesJ")]
    s += [H("2.4 Manage Compliance (output rows)", 1), table([
        ["Col", "Header", "Formula / value"],
        ["A–B", "Name, Compliance Type", "Provide Wellbeing; 10 types"],
        ["C–D", "Completion Date, Status", "14/08/2026, Completed"],
        ["E", "RAG Rating", F("E4 =IF(N4>0,3,10)") + " (Moderate Harm) but " + F("E5 =IF(N5>0,2,10)") + " (Severe Harm)"],
        ["F", "Notes", F("F6 =IF(N6>0,'All Notes'!K2,\"No incidents resulting in a fatality in last year\")") + "; " + F("F9 =IF(N9>0,'Information Governance Notes'!$I$2,\"Incidents within SPC criteria\")")],
        ["G–H", "Managed By, Due Date", "Provide Wellbeing; 24/08/2026"],
        ["I–M", "Groups, Weighting", "Operational › Incidents (SPC rows add Group 3/4, e.g. Safeguarding › Clinical); 1"],
        ["N", "Count", F("N4 =COUNTIFS(Datix_2[Severity],'Manage Compliance'!B4,Datix_2[In set timeframe],TRUE)") + " (harm rows)"],
        ["O", "SPC value", F("O10 =XLOOKUP(EDATE(DATE(YEAR(TODAY()),MONTH(TODAY()),1),-1),Safeguarding!$B:$B,Safeguarding!$C:$C,\"\")") + " (SPC rows)"],
    ], [10, 40, 130]), figure("mc"), figure("n4"), figure("o10"), figure("f6"), figure("f9"), figure("e5"), figure("e4")]
    s.append(c["PageBreak"]())
    return s


STEPS = [
    (1, "00:00:00", "00:00:44", "Introduce the incidents process", "Camera off; “a little bit different from the first video”.", "—", "—", ["rec"]),
    (2, "00:00:44", "00:02:09", "Requirements (set up by hand)", "No Names tab, one entity; requirements typed rather than added by VBA; can switch types off.", "—", "—", ["req"]),
    (3, "00:02:09", "00:03:39", "Compliance Timeframes and thresholds", "0.5 months, Operational › Incidents, lookup “used somewhere”, Missing, thresholds (“simple compliant, not compliant”).", "—", "—", ["ct", "ctB", "ctH", "ctI", "thr"]),
    (4, "00:03:39", "00:05:00", "Export from Datix (shown)", "Opens Datix tab, then RLDatix › Dashboard › Provide Wellbeing Dashboard; widget menu › Export › Excel; downloads DatixWebReport (13)/(14).xlsx and opens it.", "RLDatix → .xlsx export", "File downloaded", ["dxT", "web", "expd", "dl", "webrep"]),
    (5, "00:05:00", "00:06:18", "Datix tab calculations", "Paste location; Grouping via Datix Category (“or is that hidden? No. There we go”); In last 7 months; In set timeframe (“once it falls out of a particular time frame for harm, it doesn’t get reported”).", "Export → Datix tab (paste, described)", "—", ["dx", "dxR", "notesJ", "cat", "dxS"]),
    (6, "00:06:18", "00:06:46", "Pivots", "“It then informs a pivot for groupings and a pivot for harm.”", "Datix → Groupings / Harm pivots", "Refresh described", ["gp"]),
    (7, "00:06:46", "00:07:52", "SPC sheets per group", "“We drop down our heading and our date and drop down all these columns. That updates the statistical data… I don’t know what that table is.”", "Pivots → SPC sheets (rows extended by hand)", "Described", ["spc", "spcG", "d57"]),
    (8, "00:07:52", "00:08:51", "Notes and Manage Compliance", "Notes tabs name the Datix IDs causing non-compliance; Manage Compliance rows, RAG “10 green, 3 red”.", "SPC sheets + Datix → Manage Compliance", "Moderate Harm = 3", ["mc", "f9", "n4", "o10", "f6", "e5", "e4"]),
    (9, "00:08:51", "00:10:00", "Copy to the data store; save; refresh twice", "Selects the rows; shows the bottom of Compliance Data and its requirements table; “where Visual Basic was copying it in with staff management, we copy and paste it in”.", "Manage Compliance → Compliance Data", "Not performed", ["cdd", "req2", "mcEnd"]),
]


def section3(c):
    para, H, table, figure = c["para"], c["H"], c["table"], c["figure"]
    s = [H("3. Chronological Step-by-Step Operator Workflow", 0),
         para("Nine steps cover the 10:00 recording."),
         table([["Step", "Window", "Action"]] + [[str(x[0]), x[1] + "–" + x[2], x[3]] for x in STEPS], [10, 34, 136]), c["PageBreak"]()]
    for n, a, b, title, act, mp, mut, figs in STEPS:
        s += [H("Step %d [%s – %s]: %s" % (n, a, b, title), 1),
              table([["<b>Action performed</b>", act], ["<b>Source → target</b>", mp], ["<b>State mutation</b>", mut]], [38, 142], head=False, zebra=False)]
        s += [figure(f) for f in figs]
        s.append(c["Spacer"](1, 6))
    s.append(c["PageBreak"]())
    return s


def section4(c):
    para, H, table, figref = c["para"], c["H"], c["table"], c["figref"]
    s = [H("4. Data Quality Checks, Discrepancies &amp; Failure Modes", 0), table([
        ["ID", "Finding", "Evidence", "Impact"],
        ["SV-01", "Timeframe SWITCH tests Description, but notes and counts use Severity", figref("dxT") + ", " + figref("notesJ"), "Harm-specific limits (90/365 days) never apply; a fatal incident drops out after 42 or 90 days"],
        ["SV-02", "RAG red = 3 for Moderate Harm, 2 for Severe Harm", figref("e4") + ", " + figref("e5"), "Inconsistent values in the store"],
        ["SV-03", "0.5 months “doesn’t make any difference”", figref("ctB"), "Constant with no agreed meaning"],
        ["SV-04", "The review-panel column existed on 14/08 but was gone on 11/08 (spec 02)", figref("dxT"), "Columns of the Datix export change between runs; formulas break"],
        ["FD-01", "SPC LCL can be negative for count data", figref("spc"), "Lower-limit rules can never fire"],
        ["FD-02", "SPC rows extended by dragging each month", figref("d57"), "Missed months; formulas misaligned"],
        ["FD-03", "TODAY()-based 217-day and timeframe tests", figref("dxS"), "Not reproducible"],
        ["FD-04", "Datix export is one widget’s report, not a defined extract", figref("expd"), "Scope depends on the dashboard widget’s filter"],
        ["FM-01", "Patient narratives in the workbook", figref("dx"), "IG risk"],
        ["FM-02", "Manual copy to the store; Last Updated by hand", figref("mcEnd"), "Duplicates, stale timestamps"],
    ], [12, 62, 40, 66])]
    s.append(c["PageBreak"]())
    return s


def section5(c):
    para, H, bullets = c["para"], c["H"], c["bullets"]
    s = [H("5. Target Modern System Architecture", 0),
         para("The target design in spec 02 §5 applies unchanged (Datix ingestion by ID, versioned category map, harm SLA table, as-of dates). "
              "This recording adds:")] + bullets([
        "<b>SPC engine shared with Feedback (spec 05):</b> monthly counts per group from the incident table, versioned rule parameters, and a "
        "count-appropriate chart (c-chart or u-chart, with no negative lower limits) chosen by the business.",
        "<b>Notes as data:</b> the Datix IDs behind a non-compliant row are stored with the compliance record, replacing FILTER text in notes tabs.",
        "<b>One RAG rule</b> per result (compliant / not compliant) mapped to a single value set.",
        "<b>Defined Datix extract</b> (report definition or API query) instead of a dashboard widget export.",
    ])
    s.append(c["PageBreak"]())
    return s


def section6(c):
    H, table = c["H"], c["table"]
    s = [H("6. Gap &amp; Ambiguity Register", 0), table([
        ["ID", "Timestamp", "Gap / ambiguity", "Ask"],
        ["G-01", "00:04:24", "Which dashboard widget is exported and its filters", "Define the Datix extract"],
        ["G-02", "00:07:45", "“I don’t know what that table is” on the SPC sheets", "Explain or retire"],
        ["G-03", "00:08:42", "RAG values 3 vs 2", "Agree one rule"],
        ["G-04", "00:05:52", "Whether the timeframe should use Severity (as notes do)", "Confirm; fix"],
        ["G-05", "00:06:30", "Harm Pivot use", "Explain"],
        ["G-06", "whole video", "Why the review-panel column was missing in the 11/08 file", "Confirm export change"],
        ["G-07", "00:06:46", "SPC rule set and chart type for counts", "Approve"],
    ], [11, 22, 95, 52])]
    s.append(c["PageBreak"]())
    return s


def section7(c):
    para, H, table, figref = c["para"], c["H"], c["table"], c["figref"]
    W = [13, 52, 115]
    s = [H("7. What Is Required to Build the Modern System", 0),
         para("Spec 02 §7 lists the incident-specific requirements; this recording confirms them and adds the items below. Client checklist: "
              "<b>Incident_Full_PreBuild_Client_Requirements.pdf</b>."), table([
        ["ID", "Requirement (priority)", "Why it is required"],
        ["FR-IF01", "Defined Datix extract (report or API) with stable columns (M)", "The export is a dashboard widget download, and its columns changed between 11/08 and 14/08 (SV-04)."],
        ["FR-IF02", "Severity-based timeframe rule (M)", "SWITCH tests Description (SV-01, " + figref("dxT") + ")."],
        ["FR-IF03", "SPC engine for count data with versioned rules (M)", "SPC sheets extended by hand; negative LCL (FD-01, FD-02)."],
        ["FR-IF04", "Generated 10 compliance rows with Datix IDs as evidence (M)", "Replaces Manage Compliance and notes tabs (" + figref("mc") + ")."],
        ["FR-IF05", "Single RAG mapping (M)", "3 vs 2 (SV-02)."],
        ["T-IF01", "Golden case: 14/08/2026 result — Moderate Harm non-compliant with Datix 13135; all others compliant", "Parity with the recording."],
    ], W)]
    s.append(c["PageBreak"]())
    return s


def appendix(c):
    H, table, FIGS = c["H"], c["table"], c["FIGS"]
    E = html.escape
    s = [H("Appendix A. Figure Index", 0),
         table([["Fig", "Time", "File › Tab", "Shows"]] + [[str(i), f[1][:8], E(f[2]) + " › " + E(f[3]), E(f[4])[:150] + ("…" if len(f[4]) > 150 else "")]
                                                        for i, f in enumerate(FIGS, 1)], [8, 16, 44, 112])]
    s += [H("Appendix B. Key timestamped utterances", 0), table([
        ["Time", "Utterance (lightly cleaned)"],
        ["00:00:15", "This video is to go over the process to update the compliance data for incidents management."],
        ["00:00:57", "There is no names tab… only essentially one entity, Provide Wellbeing."],
        ["00:02:33", "Matt set it up as twice a month. I don’t think that actually makes any difference."],
        ["00:03:34", "So it’s a simple compliant, not compliant thing."],
        ["00:03:53", "We actually download incident data from Datix."],
        ["00:05:47", "And then it sets up a time frame. This is what Matt set up."],
        ["00:06:04", "Once it falls out of a particular time frame for harm, it doesn’t get reported."],
        ["00:06:30", "It then informs a pivot for groupings and a pivot for harm."],
        ["00:07:19", "We drop down our heading and our date and drop down all these columns."],
        ["00:07:45", "I don’t know what that table is."],
        ["00:08:42", "So 10 would be green, three would be red."],
        ["00:09:11", "And then we would refresh the power queries twice."],
        ["00:09:34", "Where Visual Basic was copying it in with staff management… we actually copy and paste it in."],
    ], [18, 162])]
    return s
