# -*- coding: utf-8 -*-
"""Specification content for the Complications recording (meeting 20260814_120551)."""
import html


def F(t):
    return '<font name="DVM" size="6.8">%s</font>' % html.escape(t)


WB = "Complications Report.xlsm"
DOC_TITLE = "Complications Compliance Workflow – Reverse-Engineering Specification"
HEADER = "Complications Compliance Workflow — Technical Specification (Reverse-Engineered)"
SOURCE = "Source: Teams recording 20260814_120551 (7:58)"
TITLE = "Complications Compliance Datastore Update"
SUBTITLE = ("Manual Excel / Power Query / pivot workflow that turns appointment and SystmOne complication data into monthly "
            "compliance rows, reverse-engineered from an operator screen recording, with a target-state architecture")

TITLE_BLOCK = [
    ["<b>Document</b>", "Technical Specification — reverse-engineered legacy workflow (as-is) and target architecture (to-be)"],
    ["<b>Subject workflow</b>", "Monthly update of the <b>Complications</b> area (Clinical › Complications) of the Compliance Dashboard data store, via "
     "<i>Complications Report.xlsm</i>: appointment extract (Power Query) + SystmOne complication codes → rates → standards → 8 compliance rows "
     "pasted into <i>Compliance Data.xlsm</i>"],
    ["<b>Primary evidence</b>", "Meeting with Andrew R. Biggins-20260814_120551-Meeting Recording.mp4 — 1920×1080, 16 fps, 7:58 (479 s); camera off; "
     "audience: Dheeraj. Described by the operator as “the last video, at least for now”"],
    ["<b>Secondary evidence</b>", "…120551….srt (timed subtitles, matches this video) and …120551….txt (TurboScribe transcript)"],
    ["<b>Timestamps</b>", "Video positions, cross-checked between the .srt, an offline Whisper re-transcription and frame-accurate seeks"],
    ["<b>Companion documents</b>", "Complications_PreBuild_Client_Requirements.pdf (same folder); specs 01 (Staff Management) and 02 (Incident Management)"],
    ["<b>Report date</b>", "16 October 2026"],
    ["<b>Status</b>", "Draft for business-owner review. <b>Contains patient-level data in the source workbook</b>: NHS numbers, patient names "
     "and clinical notes are blurred in every screenshot"],
]

EXEC_SUMMARY_INTRO = ("<b>What the recording shows.</b> The operator calls this “the most manual of our compliance processes”: an "
                      "automation started by Matt was never finished, and Paul Harrison asked for something interim to reach the dashboard. "
                      "The video walks through the whole chain (appointments extract, complications import, log, pivots, rate tables, "
                      "standards, transfer table) and shows, for the first time in the series, the <i>Compliance Data.xlsm</i> data store itself.")

EXEC_SUMMARY = [
    "<b>Two raw sources:</b> (1) the appointments data store, loaded by a Power Query (<font name='DVM'>All_Appts</font>) that refreshes when the "
    "workbook opens; (2) a SystmOne report of complication Read codes, uploaded by hand into <i>Complications_from Sys1</i>, from which new rows "
    "are copied into the <i>Complications Details</i> log.",
    "<b>Patient-level matching by formula:</b> each appointment row gets Infection, Pain and VAS Failure flags from array INDEX/MATCH formulas that "
    "look for the same NHS number with a complication Read code dated after the appointment and before the next one.",
    "<b>Rates and standards:</b> four pivots (All Ops, All VAS Ops, Infections, Pain) feed GETPIVOTDATA rate grids per clinician and month. The "
    "<i>Compliance Report</i> tab counts complications over 12 months, computes monthly rates and compares 3/6/12-month averages and a "
    "12-month spike with fixed limits (2%/4% failures, 1%/2% haematoma, 3%/6% others).",
    "<b>The result is typed, not linked:</b> the <i>Compliance Data Transfer</i> table holds 8 fixed rows, all “Completed / Within benchmark”, "
    "which are copied by hand to the bottom of the data store; Last Updated is edited by hand; then the data store is saved and refreshed twice.",
    "<b>Defects seen:</b> the result block is stamped “at 09/04/26” while the recording is 14/08/2026; the monthly table stops at June; the "
    "Benchmarks tab uses different limits from the Compliance Report; the transfer table includes Dehiscence and Sperm Granuloma, which have no "
    "calculation; Next Appt Date uses a hard-coded range ending at row 30221; Compliance Data shows “UNABLE TO REFRESH – linked workbook”.",
    "<b>New evidence for the whole series:</b> the data store tabs Compliance Data, Last Updated, requirements_Detailed, "
    "compliance_Timeframes_Table, requirements_Final_Self_Ref and per-tool tables (staff_requirements_Table, estates_…) are shown, which closes "
    "several gaps in specs 01 and 02 (§1.3).",
]


# --------------------------------------------------------------------------------------------
def section0(c):
    para, H, table, bullets = c["para"], c["H"], c["table"], c["bullets"]
    s = [H("0. Evidence Base, Method &amp; Reading Guide", 0)]
    s += [H("0.1 Source artefacts", 1), table([
        ["Artefact", "What it is", "Used for"],
        ["…20260814_120551-Meeting Recording.mp4", "Teams recording, 1920×1080, 16 fps, 7:58. Git-LFS object, 42 MB", "Screenshots, step timings"],
        ["…20260814 120551-Meeting Recording.srt", "Timed subtitles of the same meeting", "Timestamp anchors"],
        ["…20260814 120551-Meeting Recording.txt", "TurboScribe transcript", "Wording cross-check"],
        ["Author ASR (Whisper small.en)", "Independent re-transcription", "Confirms timings"],
    ], [52, 78, 50])]
    s += [H("0.2 Method and redaction", 1)] + bullets([
        "Frames were taken with ffmpeg at the stated second (a 1 fps sweep was found to run about 2 s ahead and was corrected), cropped to the "
        "Excel window or the formula bar, and checked for sharpness and stability.",
        "<b>Redaction:</b> this workbook holds identifiable patient data. In every screenshot the NHS number, Appt Ref (name or NHS number + date), "
        "Patient ID, clinical Notes and the NHS-number lookup key are blurred (red outline). Formula-bar crops stop above the first data row. "
        "Clinician and staff names are left, as in specs 01 and 02.",
        "Confidence tags: <b>[Seen]</b>, <b>[Said]</b>, <b>[Inferred]</b>, <b>[Unknown]</b>.",
    ])
    s.append(c["PageBreak"]())
    return s


# --------------------------------------------------------------------------------------------
def section1(c):
    para, H, table, figure, figref = c["para"], c["H"], c["table"], c["figure"], c["figref"]
    s = [H("1. Complete File, Workbook &amp; Sheet Inventory", 0)]
    s += [H("1.1 Files and external systems", 1), table([
        ["#", "File / system", "Format", "Role", "Evidence"],
        ["F1", "<b>Complications Report.xlsm</b>", ".xlsm; VBA project present but no code found", "Analysis workbook: import, log, pivots, rates, standards, transfer table", figref("cd0") + ", " + figref("vbe")],
        ["F2", "<b>Compliance Data.xlsm</b>", ".xlsm", "The data store: rows pasted here; requirements/timeframes tables; Last Updated", figref("req") + "–" + figref("end")],
        ["S1", "Appointments data store", "Database / file behind Power Query All_Appts (source not shown)", "Every appointment (ops and procedures) since 2023", figref("pq")],
        ["S2", "<b>SystmOne</b>", "Clinical system; report export of complication Read codes", "Raw complications (NHS number, Read code, event date, service, clinician)", figref("sys1")],
        ["F3", "“Another document… the original automated version”", "Not named", "Source of the Complications requirements and timeframes rows in the data store", "Said 00:07:15–00:07:41"],
        ["S3", "Compliance Dashboard", "BI", "Shows Clinical › Complications", "Said 00:00:58"],
    ], [8, 38, 40, 64, 30])]
    s += [H("1.2 Worksheet tabs in Complications Report.xlsm", 1),
          para("Tab order from the tab bar and the VBA project list (" + figref("vbe") + "): 18 sheets."),
          table([
              ["Tab (VBA name)", "Role", "Opened"],
              ["Ops Site Clinician Pivot (Sheet7)", "Pivot: activity and infections by site → clinician → month", "04:12"],
              ["All Ops Pivot", "Pivot: count of ops per clinician per month (denominator)", "04:56"],
              ["All VAS Ops Pivot", "Pivot: vasectomy ops per clinician per month", "04:46"],
              ["Infections Pivot (Sheet2)", "Pivot: infections per clinician per month", "05:02"],
              ["Pain Pivot (Sheet3)", "Pivot: post-op pain per clinician per month", "05:04"],
              ["<b>Complications_from Sys1</b> (Sheet5)", "<b>Raw source</b>: SystmOne complications export (table All_Complications)", "03:27"],
              ["<b>Complications Details</b> (Sheet6)", "<b>Log</b>: manually curated complications (Table5)", "00:30, 03:57"],
              ["<b>All_Appts Data Auto Load</b> (Sheet4)", "<b>Raw source + calc</b>: Power Query appointments + complication flags", "02:13–03:20"],
              ["Infection Rate (Sheet9)", "Rate grid per clinician × month (GETPIVOTDATA)", "05:14"],
              ["Post-Op Reported Pain Rate", "Rate grid (same pattern) [Inferred]", "Tab only"],
              ["Vas Failure Rate", "Yearly failure rate per clinician, running rate", "05:23"],
              ["Comps Reported Pivot", "Pivot of reported complications [Inferred]", "Tab only"],
              ["<b>Compliance Report</b>", "<b>Standards and compliance result</b>", "05:26–06:30"],
              ["Clinician Overview", "Per-clinician dashboard", "06:42"],
              ["Benchmarks (Sheet16)", "Reference limits by service", "06:43"],
              ["Vas Failure Pivot (Sheet17)", "Pivot: VAS failures by clinician × year", "06:45"],
              ["<b>Compliance Data Transfer</b> (Sheet18)", "<b>Output</b>: rows to paste into the data store", "06:50"],
              ["Sheet1 (Sheet8)", "Unnamed sheet", "Never [Gap G-10]"],
          ], [55, 95, 30])]
    s += [H("1.3 The data store, Compliance Data.xlsm (closes gaps in specs 01 and 02)", 1),
          para("For the first time the data store is shown (07:00–07:50). Tabs seen: <b>Compliance Data</b> (the main table, last row 4268), "
               "<b>Last Updated</b>, <b>requirements_Detailed</b>, <b>compliance_Timeframes_Table</b>, <b>requirements_Final_Self_Ref</b>, and "
               "per-tool tables such as <b>staff_requirements_Table</b>, <b>estates_requirements_Table</b>, <b>estates_Compliance_Timeframe_Table</b>. "
               "Green tabs are Power Query outputs [Inferred], so each tool’s Requirements and Compliance Timeframes are pulled in by query and "
               "appended into consolidated tables. A banner reads “UNABLE TO REFRESH – We couldn’t get updated values from a linked workbook”."),
          table([
              ["Table", "Columns seen", "Notes"],
              ["Compliance Data", "Name, Compliance Type, Completion Date, Completion Status, Issue, Compliance Notes, Managed By, Due Date, …", "One row per evidence record from every tool (staff, sites such as Valkyrie Primary Care Centre, etc.)"],
              ["requirements_Final(_Self_Ref)", "Name, Compliance Type, Required (T/F), Core Requirement, Managed By, Unique Lookup", "Union of all tools’ requirements"],
              ["compliance_Timeframes_Table", "Compliance Type, Every x months, Core Requirement, Compliance Group 1–4, Unique Lookup", "Estates rows first; RTT Compliance rows use 0.25 months"],
              ["Last Updated", "Compliance Group Level 1, Level 2, Updated, Unique Lookup", "25 areas, e.g. Operational–Incidents 28/07/2026, Clinical–Complications 27/07/2026"],
          ], [40, 80, 60])]
    s += [H("1.4 Overview screenshots", 1), figure("rec", 70 * c["mm"]), figure("vbe"), figure("pq", 80 * c["mm"])]
    s.append(c["PageBreak"]())
    return s


# --------------------------------------------------------------------------------------------
def section2(c):
    para, H, table, figure, figref = c["para"], c["H"], c["table"], c["figure"], c["figref"]
    mm = c["mm"]
    W = [9, 32, 24, 16, 99]
    hdr = ["Col", "Header", "Type", "Origin", "Lineage, rule and evidence"]
    s = [H("2. Exhaustive Column-Level Schema &amp; Data Lineage Catalogue", 0),
         para("Origin: <b>PQ</b> = Power Query from the appointments store; <b>SYS1</b> = SystmOne export; <b>MAN</b> = typed/copied by the operator; "
              "<b>CALC</b> = formula; <b>PIV</b> = pivot.")]
    s += [H("2.1 All_Appts Data Auto Load (Power Query table + calculated columns)", 1), table([hdr,
        ["A", "NHS number", "Text (10 digits)", "PQ · <b>PID</b>", "Patient identifier; join key to complications"],
        ["B", "Appointment Date", "Date", "PQ", "e.g. 03/01/2023"],
        ["C", "Appointment status", "Text", "PQ", "e.g. Finished"],
        ["D", "Clinician", "Text", "PQ", "Pivot dimension"],
        ["E", "Service Level 1", "Text", "PQ", "e.g. Self Pay / NHS"],
        ["F", "Service Level 2", "Text", "PQ", "e.g. Minor Skin; counted as the ops denominator in rate formulas"],
        ["G", "Branch", "Text", "PQ", "Site, e.g. Tollgate Clinic"],
        ["H", "Duration", "Time", "PQ", "e.g. 00:30:00"],
        ["I–J", "Outcome 1, Outcome 2", "Text", "PQ", "Free text"],
        ["K", "Appt Type", "Text", "PQ", "Procedure / Op"],
        ["L", "Appt Ref 1", "Text", "PQ · <b>PID</b>", "“Name-dd/mm/yyyy” for procedures or “NHS number-referral date-appointment date-time” for ops"],
        ["M", "Service Name", "Text", "PQ", "e.g. SP-Minor Skin, Suffolk and NEE Vasectomy, Carpal Tunnel North East Essex"],
        ["N", "Patient ID", "Text", "CALC · <b>PID</b>", F('=LEFT([@[Appt Ref 1]],SEARCH("-",[@[Appt Ref 1]])-1)') + " → name or NHS number. " + figref("apN")],
        ["O", "Next Appt Date", "Date", "CALC", F('=IF([@[NHS number]]<>"",XLOOKUP([@[NHS number]],A3:A$30221,B3:B$30221,0),0)') +
         ": next appointment for the same NHS number, from the row below to a <b>fixed row 30221</b>; shows 00/01/1900 when none. Operator: “I don’t know why that’s required” (00:02:31). It bounds the complication window. " + figref("apO")],
        ["P", "Infection", "0/1", "CALC", "Nested IFERROR over five Read codes: " + F('INDEX(All_Complications[…Read code],MATCH(1,([@[NHS number]]=All_Complications[NHS number])*([@[Appointment Date]]<=All_Complications[…Event date])*(IF([@[Next Appt Date]]=0,1000000,[@[Next Appt Date]])>All_Complications[…Event date])*("(Xa6nk) Postoperative wound infection"=All_Complications[…Read code]),0))') + " … → 1 if found. " + figref("apP")],
        ["Q", "Pain", "0/1", "CALC", "Same pattern with (SP2y2) Postoperative pain"],
        ["R", "VAS Failure", "0/1", "CALC", "Same pattern with (61G1.) Vasectomy failure. " + figref("apR")],
        ["S", "Notes", "Text", "CALC", F('=IF([@Infection]>0,XLOOKUP(CONCAT([@[NHS number]],"-",TEXT([@[Appointment Date]],"dd/mm/yyyy")),Table5[Lookup 1],Table5[Notes],""),"")') +
         ": pulls the log’s note when an infection is flagged; the key uses Appointment Date, while the log key uses Op Date. " + figref("apS")],
    ], W)]
    s += [figure("apS"), figure("apN", 40 * mm), figure("apO", 40 * mm), figure("apP"), figure("apR", 40 * mm)]
    s += [H("2.2 Complications_from Sys1 (SystmOne export, table All_Complications)", 1), table([hdr,
        ["A", "NHS number", "Text", "SYS1 · <b>PID</b>", "Join key"],
        ["B", "Complications &amp; Infections – MT: Read code", "Text", "SYS1", "Coded complication, e.g. (SP2y2) Postoperative pain, (X000B) Haematoma – postoperative, (X76Eu) Swelling, (SP250) Postoperative stitch abscess, (61G1.) Vasectomy failure, (X79pw) Infection, (Xa1sV) Antibiotic therapy, (Xa6nk) Postoperative wound infection"],
        ["C", "…MT: Event date", "Date dd-Mmm-yy", "SYS1", "Different date format from the other tabs"],
        ["D", "xxx All Tollgate Referrals ever – MT Combined: Service offered", "Text", "SYS1", "Service, e.g. Herts and West Essex Vasectomy"],
        ["E", "…MT: Event done by", "Text", "SYS1", "Staff member who recorded the event"],
    ], W), para("About 1,000 rows (row 1003 reached, Jan 2023–Jun 2026). Re-uploaded by hand each month (“we upload from System 1”, 00:03:36). " +
                "Note that the Infection formula only tests five Read codes; codes such as (SP250) stitch abscess or (Xa1sV) antibiotic therapy are "
                "counted only if they are among those five [Gap G-04]."), figure("sys1")]
    s += [H("2.3 Complications Details (the log, Table5)", 1), table([hdr,
        ["A", "NHS number", "Text", "MAN · <b>PID</b>", "Copied from Complications_from Sys1"],
        ["B", "Read Code", "Text", "MAN", "As above"],
        ["C", "Event date", "Date", "MAN", "e.g. 17/07/2026"],
        ["D", "Service offered", "Text", "MAN", "e.g. Herts and West Essex Vasectomy"],
        ["E", "Op Date", "Date", "MAN", "Date of the original operation (looked up by hand) [Inferred]"],
        ["F", "Procedure", "Text", "MAN", "e.g. Vas"],
        ["G–I", "Location, Clinician, Nurse", "Text", "MAN", "e.g. Davenport House, Dr Hein Leonhardt"],
        ["J", "Antibiotics prescribed", "Yes/No", "MAN", ""],
        ["K", "Diagnosed By", "Text", "MAN", "e.g. N/a"],
        ["L", "Notes", "Long text", "MAN · <b>clinical</b>", "Telephone-encounter narrative (blurred)"],
        ["M", "Intra-operative/Post operative", "Text", "MAN", "e.g. Post Operative pain"],
        ["N", "Include in Statistics", "Flag", "MAN", "Manual exclusion switch [Inferred]"],
        ["O", "Lookup 1", "Text key", "CALC · <b>PID</b>", F('=CONCAT([@[NHS number]],"-",TEXT([@[Op Date]],"dd/mm/yyyy"))') + "; empty rows give “-00/01/1900”. " + figref("cd1")],
    ], W), para("Operator: “we copy any new complications into the log. There’s a lookup in the log; I don’t even know what that is specifically used for” (00:03:44–00:04:03). It is used by All_Appts!S (Notes)."),
          figure("cd0"), figure("cd1")]
    s += [H("2.4 Pivots and rate tabs", 1), table([
        ["Tab", "Rows × columns × values", "Feeds"],
        ["Ops Site Clinician Pivot", "Site → clinician → Activity / Infections × year → month", "Clinician Overview [Inferred]"],
        ["All Ops Pivot", "Year → month × clinician; count of Service Level 2 (filter Appt Type = All)", "Denominator in Infection / Pain rate"],
        ["All VAS Ops Pivot", "Same, filtered to vasectomy services", "VAS Ops for Failures"],
        ["Infections Pivot / Pain Pivot", "Year → month × clinician; sum of Infection / Pain", "Numerators"],
        ["Vas Failure Pivot", "Year × clinician; sum of VAS Failure", "Vas Failure Rate"],
        ["Infection Rate", F("=IFERROR(IFERROR(GETPIVOTDATA(\"Infection\",'Infections Pivot'!$A$3,\"Appointment Date\",MONTH(BB$1),\"Clinician\",$A14,\"Years\",YEAR(BB$1)),0)/IFERROR(GETPIVOTDATA(\"Service Level 2\",'All Ops Pivot'!$A$3,…),0),\"N/A\")") + "; pink when high", "Clinician Overview"],
        ["Vas Failure Rate", "Per clinician per year 2023–2026; Overall; Overall (minus Dr Saad); Running Rate 0.35% / 0.23% (minus Dr Saad)", "Review only"],
    ], [38, 92, 50]), para("Clinician names appear twice in different forms (e.g. “Dr Hein Leonhardt” and “Hein Leonhardt”, “Dr Alan Speers” and "
                           "“Alan Speers”, “Dr Johann H C Leonhardt”), so one person’s activity is split across pivot columns [FM-06]."),
          figure("pv1"), figure("pv2"), figure("inf"), figure("vfr")]
    s += [H("2.5 Compliance Report (standards and result)", 1), table([
        ["Block", "Content", "Rule"],
        ["A2:E9 Standards", "Type × 3-month average, 6-month average, 12-month average, 12-month spike", "Failure 2%/2%/2%/4%; Haematoma 1%/1%/1%/2%; Pain, Infection, Bleeding, Swelling, Granuloma 3%/3%/3%/6%"],
        ["F2:S9 Monthly status", "Mar-25 … Jun-26 columns of “Compliant” (May-25 blank)", "History of results, typed or pasted [Inferred]"],
        ["A11:F19 Result", "“at 09/04/26”; 12 month spike, 12/6/3 month averages per type; Compliant flag", "B13 = " + F("MAX(B31:M31)") + " (highest monthly rate); averages over the matching months; Compliant if every figure ≤ its limit [Inferred]"],
        ["A21:M30 Counts", "July…June: VAS Failures, Haematoma, Pain, Infection, Bleeding, Swelling, Granuloma; VAS Ops for Failures; Overall Ops", "Typed counts (“the compliance is really a manual process whereby we count…”, 00:05:26). Note: “Use 12 months previous (i.e. failures take 12 months to wash through)”"],
        ["A31:M37 Rates", "Monthly rate per type", F("=B22/B29") + " for failures (÷ VAS ops), others ÷ Overall Ops"],
    ], [30, 70, 80]), figure("cr1"), figure("cr2")]
    s += [H("2.6 Clinician Overview, Benchmarks and Compliance Data Transfer", 1), figure("clin"), figure("bench"),
          table([hdr,
                 ["A", "Name", "Text", "MAN", "Provide Wellbeing"],
                 ["B", "Compliance Type", "Text", "MAN", "Bleeding, Haematoma, Infection, Pain, Sperm Granuloma, Swelling, Vas Failure, Dehiscence"],
                 ["C", "Completion Date", "Date", "MAN", "14/08/2026 (the day of the update)"],
                 ["D", "Completion Status", "Text", "MAN", "Completed"],
                 ["E", "Issue", "Number", "MAN", "10 (meaning not explained) [Gap G-07]"],
                 ["F", "Compliance Notes", "Text", "MAN", "“Within benchmark” for all 8, including the two types not calculated"],
                 ["G", "Managed By", "Text", "MAN", "Provide Wellbeing"],
                 ["H", "Due Date", "Date", "MAN/CALC", "11/09/2026 (4 weeks later)"],
                 ["I–L", "Compliance Group Level 1–4", "Text", "MAN", "Clinical, Complications"],
                 ["M", "Weighting", "Number", "MAN", "1"],
          ], W), figure("vfp"), figure("cdt")]
    s += [H("2.7 Compliance Data.xlsm screens", 1), figure("req"), figure("cdd"), figure("lu"), figure("ctt"), figure("ctt2"), figure("end")]
    s.append(c["PageBreak"]())
    return s


# --------------------------------------------------------------------------------------------
STEPS = [
    (1, "00:00:00", "00:00:30", "Introduce the last video; start screen share",
     "Camera off. “This video deals with complications compliance… operational complications.”", "—", "—"),
    (2, "00:00:30", "00:01:30", "Explain why this process is manual",
     "Complications Details is on screen. “The most manual… an intention to automate it… wasn’t anywhere near finished before Matt left. Paul Harrison was quite keen for it to appear on the dashboard… cobble together something.”", "—", "—"),
    (3, "00:01:30", "00:02:13", "Check for VBA; show the Power Query",
     "Opens Developer › Visual Basic, looks at ThisWorkbook (empty): “Oh no, it probably isn’t actually.” Opens the Power Query editor: one query All_Appts, “refreshes on launch of the workbook… an extract from our appointments data store”.",
     "Appointments data store → All_Appts Data Auto Load (on open)", "Table refreshed on open (not shown happening)"),
    (4, "00:02:13", "00:03:20", "Walk through the appointment formulas",
     "Selects S6412 (Notes), N2 (Patient ID), O2 (Next Appt Date: “I don’t know why that’s required”), P2 (Infection), Q2 (Pain), R2 (VAS Failure).", "Read-only", "—"),
    (5, "00:03:20", "00:03:44", "Identify the complications source tabs",
     "Searches for “Table5”: “all complications… must be this one or is it even this one?”, opening Complications_from Sys1 and Complications Details.", "—", "Operator unsure which table feeds which [G-02]"),
    (6, "00:03:36", "00:04:10", "Upload from SystmOne and copy new rows into the log (described)",
     "“We wait for the appointments to refresh. We upload from System 1… we copy any new complications into the log.” Shows the log’s Lookup 1 column.",
     "SystmOne report → Complications_from Sys1 (paste) → new rows copied to Complications Details", "Not performed on screen"),
    (7, "00:04:10", "00:05:08", "Refresh and review the pivots",
     "“Various pivots which we refresh after the data has been loaded”: Ops Site Clinician, All VAS Ops, All Ops, Infections, Pain.", "All_Appts → pivots", "Refresh not shown"),
    (8, "00:05:08", "00:05:26", "Rate tables",
     "Infection Rate (GETPIVOTDATA), Vas Failure Rate: “a series of tables which Matt set up to calculate rates of incidence”.", "Pivots → rate grids", "—"),
    (9, "00:05:26", "00:06:26", "Count, calculate and compare with standards (Compliance Report)",
     "“We count how many complications of different types have occurred in the last 12 months… calculate the rates… a set of standards… within those they’re compliant.” Shows B31 =B22/B29 and B13 =MAX(B31:M31).",
     "Counts (typed) → rates → result vs limits", "Result block still dated “at 09/04/26”"),
    (10, "00:06:26", "00:06:58", "Prepare the transfer rows",
     "Flicks through Clinician Overview, Benchmarks, Vas Failure Pivot; selects the 8 rows of Compliance Data Transfer: “we copy the data from a simple table… you’ll recognise from the other compliance areas”.",
     "Compliance Data Transfer A2:M9 → clipboard", "Selection only"),
    (11, "00:06:58", "00:07:12", "Paste into the data store; update Last Updated (described)",
     "Switches to Compliance Data.xlsm (“UNABLE TO REFRESH” banner), shows the bottom of Compliance Data (row 4268) and the Last Updated tab: “we copy it into the bottom… we update our last update date”.",
     "Clipboard → Compliance Data (bottom); Last Updated!C24", "Not performed: last row and C24 = 27/07/2026 unchanged"),
    (12, "00:07:12", "00:07:58", "Save and refresh twice; explain requirements source",
     "“We save it and we refresh twice. The compliance timeframes and the requirements pull from another document, the original automated version… literally two tables.” Scrolls compliance_Timeframes_Table and requirements tabs. End.",
     "Other document → requirements / timeframes (query)", "Not performed"),
]

STEP_FIGS = {1: ["rec"], 2: ["cd0"], 3: ["vbe", "pq"], 4: ["apS", "apP"], 5: ["sys1"], 6: ["cd1"], 7: ["pv1", "pv2"], 8: ["inf", "vfr"],
             9: ["cr1", "cr2"], 10: ["clin", "bench", "vfp", "cdt"], 11: ["req", "cdd", "lu"], 12: ["ctt", "ctt2", "end"]}


def section3(c):
    para, H, table, figure = c["para"], c["H"], c["table"], c["figure"]
    s = [H("3. Chronological Step-by-Step Operator Workflow", 0),
         para("Twelve steps cover the 7:58 recording. The recording is a walkthrough: the monthly update itself (upload, copy, refresh, paste, "
              "save) is <b>described, not performed</b>, so no before/after state change is visible except selections."),
         table([["Step", "Window", "Action"]] + [[str(x[0]), x[1] + "–" + x[2], x[3]] for x in STEPS], [10, 34, 136]), c["PageBreak"]()]
    for n, a, b, title, act, mp, mut in STEPS:
        s += [H("Step %d [%s – %s]: %s" % (n, a, b, title), 1),
              table([["<b>Action performed</b>", act], ["<b>Source → target</b>", mp], ["<b>State mutation</b>", mut]], [38, 142], head=False, zebra=False)]
        s += [figure(f) for f in STEP_FIGS[n]]
        s.append(c["Spacer"](1, 6))
    s.append(c["PageBreak"]())
    return s


# --------------------------------------------------------------------------------------------
def section4(c):
    para, H, table, figref = c["para"], c["H"], c["table"], c["figref"]
    s = [H("4. Data Quality Checks, Manual Exceptions &amp; Edge Cases", 0)]
    s += [H("4.1 Business rules", 1), table([
        ["ID", "Rule", "Evidence"],
        ["BR-01", "A complication belongs to the appointment for the same NHS number whose date is on or before the event and whose next appointment is after it", figref("apP")],
        ["BR-02", "Infection, pain and VAS failure are identified by specific SystmOne Read codes", figref("apP") + ", " + figref("apR")],
        ["BR-03", "VAS failure rate = failures ÷ vasectomy ops of the month 12 months earlier (“failures take 12 months to wash through”)", figref("cr1")],
        ["BR-04", "Other complication rates = count ÷ overall ops of the month", figref("cr1")],
        ["BR-05", "Compliant when the 3/6/12-month averages and the 12-month spike are within the limits in Compliance Report A2:E9", figref("cr2")],
        ["BR-06", "One compliance row per complication type is published monthly for Provide Wellbeing, Clinical › Complications", figref("cdt")],
        ["BR-07", "Rates are reviewed per clinician; Dr Saad is excluded from one overall figure", figref("vfr")],
    ], [12, 128, 40])]
    s += [H("4.2 Manual steps", 1), table([
        ["ID", "Manual step", "Risk"],
        ["EX-01", "SystmOne report run and pasted each month", "Wrong date range or format; no check that all rows arrived"],
        ["EX-02", "New complications copied into the log, with Op Date, clinician, notes added by hand", "Duplicates or misses; inconsistent spelling"],
        ["EX-03", "Pivots refreshed by hand", "Stale pivots feed the rates"],
        ["EX-04", "Monthly complication counts typed into Compliance Report rows 22–30", "Typing errors; counts not traceable to records"],
        ["EX-05", "Transfer rows (fixed text) copied to the bottom of Compliance Data", "Duplicate months; wrong position; no link to the calculation"],
        ["EX-06", "Last Updated edited by hand; data store saved and refreshed twice", "Forgotten step (C24 still 27/07/2026)"],
    ], [12, 90, 78])]
    s += [H("4.3 Spoken vs visual discrepancies and defects", 1), table([
        ["ID", "Said / intended", "Seen", "Impact"],
        ["SV-01", "“A little bit of Visual Basic somewhere” (00:01:40)", "No code in ThisWorkbook; modules not inspected", "Unknown automation [G-01]"],
        ["SV-02", "Compliance is based on the last 12 months", "Result block stamped “at 09/04/26”; monthly table runs July–June", "Published result may be four months old"],
        ["SV-03", "“If they’re within those [standards] they’re compliant” (00:06:05)", "Benchmarks tab: Herts failure < 0.05%, haematoma < 1%, infection < 1%; Compliance Report: failure 2%/4%, infection 3%/6%", "Two different sets of limits; the looser one is used"],
        ["SV-04", "8 compliance types published", "Only 7 types are calculated; Dehiscence and “Sperm Granuloma” vs “Granuloma” have no calculation", "A row reports “Within benchmark” without evidence"],
        ["SV-05", "Transfer rows reflect the calculation", "All 8 rows are fixed text: Completed, Issue 10, Within benchmark", "Non-compliance would never reach the dashboard unless someone edits the text"],
        ["SV-06", "“There’s a lookup in the log… don’t know what that is used for” (00:03:55)", "Lookup 1 feeds All_Appts!S Notes", "Hidden dependency"],
        ["FD-01", "Next appointment lookup", "Hard-coded range A3:A$30221", "Silently wrong once the table passes 30,221 rows"],
        ["FD-02", "Notes lookup key", "All_Appts uses Appointment Date; the log key uses Op Date", "Notes only found when both dates match"],
        ["FD-03", "Infection detection", "Five Read codes tested; other infection-related codes in the export (antibiotic therapy, stitch abscess) may be ignored", "Under-counting [G-04]"],
        ["FD-04", "Data store refresh", "“UNABLE TO REFRESH – linked workbook”", "Data store may hold stale lookups"],
    ], [12, 50, 62, 56])]
    s += [H("4.4 Hidden failure modes", 1), table([
        ["ID", "Failure mode", "Severity"],
        ["FM-01", "<b>Patient-identifiable data</b> (NHS numbers, names, clinical notes) in a shared workbook used for a dashboard", "High (IG)"],
        ["FM-02", "<b>Manual counts</b> typed into the report break the link between records and the published result", "High"],
        ["FM-03", "<b>Hard-coded transfer rows</b> always say “Within benchmark”", "High"],
        ["FM-04", "<b>Stale result</b> (at 09/04/26) published as current", "High"],
        ["FM-05", "<b>Conflicting standards</b> between tabs", "Medium"],
        ["FM-06", "<b>Clinician name variants</b> split pivot columns and rates", "Medium"],
        ["FM-07", "<b>Row-limited formulas</b> (30221) and array formulas over ~30k rows make the workbook slow and fragile", "Medium"],
        ["FM-08", "<b>Duplicate month rows</b> in the data store if the paste is repeated", "Medium"],
        ["FM-09", "<b>Data store link errors</b> (UNABLE TO REFRESH)", "Medium"],
        ["FM-10", "<b>Single-person knowledge</b>: the operator could not explain several parts (“set up back in the mists of time by Matt”)", "Medium"],
    ], [12, 148, 20])]
    s.append(c["PageBreak"]())
    return s


# --------------------------------------------------------------------------------------------
def section5(c):
    para, H, table, bullets, code = c["para"], c["H"], c["table"], c["bullets"], c["code"]
    s = [H("5. Target Modern System Architecture Blueprint", 0),
         para("Complications run on the shared platform (spec 01 §5). Unlike the other two areas, the inputs are clinical events, so the design "
              "adds a governed clinical-data boundary: patient-level data is processed in a restricted zone and only aggregates reach the "
              "compliance store and dashboard.")]
    s += [H("5.1 Ingestion", 1)] + bullets([
        "<b>Appointments:</b> read directly from the appointments data store (scheduled extract or view), replacing the on-open Power Query.",
        "<b>Complications:</b> scheduled SystmOne report export to a secure drop folder (or API where licensed), with a header contract "
        "(NHS number, Read code, event date, service, event done by) and date parsing for dd-Mmm-yy.",
        "<b>Validation:</b> NHS number checksum, Read code in the approved code list, event date not in the future, service mapped.",
        "<b>Restricted zone:</b> patient-level tables live in a schema with tight role-based access; the compliance mart holds only counts and rates.",
    ])
    s += [H("5.2 Data model additions", 1), table([
        ["Table", "Key columns", "Replaces"],
        ["<b>clin.appointment</b>", "appointment_id, nhs_number (restricted), appointment_date, clinician_id, service_id, site_id, appt_type", "All_Appts"],
        ["<b>clin.complication_event</b>", "event_id, nhs_number (restricted), read_code, event_date, service_id, recorded_by, source_batch_id", "Complications_from Sys1"],
        ["<b>clin.complication_attribution</b>", "event_id, appointment_id, rule_version, reviewed_by, include_in_stats, notes (restricted)", "Complications Details log + INDEX/MATCH flags"],
        ["<b>ref.read_code_map</b> (versioned)", "read_code, complication_type (Infection, Pain, Haematoma, Swelling, Bleeding, Granuloma, Dehiscence, VAS Failure), valid_from/to", "Codes inside formulas"],
        ["<b>ref.clinician</b> + alias", "clinician_id, display_name, aliases (“Dr Hein Leonhardt”, “Hein Leonhardt”)", "Name variants in pivots"],
        ["<b>ref.complication_standard</b> (versioned)", "complication_type, service_group, window (3/6/12 m), avg_limit, spike_limit, valid_from/to, approved_by", "Compliance Report A2:E9 and Benchmarks"],
        ["<b>mart.complication_rate_monthly</b>", "month, complication_type, clinician_id, service_group, numerator, denominator, rate", "Pivots and rate grids"],
        ["<b>mart.complication_compliance</b>", "as_of_month, complication_type, avg_3m, avg_6m, avg_12m, spike_12m, is_compliant, standard_version", "Compliance Report result + Transfer table"],
    ], [42, 103, 35])]
    s += [H("5.3 Rules as SQL", 1), code(
        "-- Attribute each complication to the most recent prior appointment of the same patient\n"
        "CREATE VIEW clin.v_attribution AS\n"
        "SELECT e.event_id, a.appointment_id\n"
        "FROM clin.complication_event e\n"
        "JOIN LATERAL (\n"
        "  SELECT a.appointment_id FROM clin.appointment a\n"
        "  WHERE a.nhs_number = e.nhs_number AND a.appointment_date <= e.event_date\n"
        "  ORDER BY a.appointment_date DESC LIMIT 1) a ON true;\n\n"
        "-- Monthly rates; VAS failures use the denominator 12 months earlier (rule BR-03, to confirm)\n"
        "SELECT m.month, t.complication_type,\n"
        "       count(x.event_id)::numeric / NULLIF(CASE WHEN t.complication_type = 'VAS Failure'\n"
        "            THEN lag(ops.vas_ops, 12) OVER w ELSE ops.all_ops END, 0) AS rate\n"
        "FROM ...  WINDOW w AS (PARTITION BY t.complication_type ORDER BY m.month);")]
    s += bullets([
        "3/6/12-month averages and the 12-month spike are window functions (AVG / MAX over the last n months) evaluated for the publication’s as-of month; "
        "the result is computed, never typed (fixes FM-02, FM-03, FM-04).",
        "One approved standards table replaces both the Compliance Report limits and the Benchmarks tab (FM-05).",
        "Clinician aliases resolve to one id before aggregation (FM-06).",
    ])
    s += [H("5.4 Review and publication", 1)] + bullets([
        "<b>Clinical review queue:</b> new complication events are reviewed (include in statistics, attribution, note) by a clinical reviewer, replacing the manual copy into the log.",
        "<b>Publication:</b> one compliance record per type per month is generated from mart.complication_compliance inside the shared atomic publish, with the "
        "as-of month and standard version; Last Updated becomes the publish timestamp.",
        "<b>Idempotent:</b> republishing a month replaces that month’s rows; no duplicate rows (FM-08).",
    ])
    s.append(c["PageBreak"]())
    return s


# --------------------------------------------------------------------------------------------
def section6(c):
    H, table = c["H"], c["table"]
    s = [H("6. Gap &amp; Ambiguity Register", 0), table([
        ["ID", "Timestamp", "Gap / ambiguity", "Ask"],
        ["G-01", "00:01:40", "Whether any VBA exists (only ThisWorkbook was opened)", "Export the VBA project"],
        ["G-02", "00:03:04–00:03:33", "Which table is Table5 and how the two complications tabs relate (operator unsure)", "Confirm the data flow"],
        ["G-03", "00:02:08", "Source of the All_Appts query (database, file, filters)", "Share the M code"],
        ["G-04", "00:02:40", "Full list of Read codes per complication type; why five codes for infection", "Approve a Read-code map"],
        ["G-05", "00:05:26", "How the monthly counts in rows 22–28 are produced (typed from pivots? which filters?)", "Walk through one month"],
        ["G-06", "00:06:14", "Why the result is “at 09/04/26”; how the Mar-25…Jun-26 status columns are filled", "Explain the monthly routine"],
        ["G-07", "00:06:50", "Meaning of Issue = 10, Weighting = 1, and the 4-week due date", "Define fields"],
        ["G-08", "00:06:43", "Which limits are authoritative: Benchmarks or Compliance Report", "Clinical lead to decide"],
        ["G-09", "00:06:50", "How Dehiscence and Sperm Granuloma are assessed", "Define or remove"],
        ["G-10", "VBA list", "Purpose of Sheet1, Post-Op Reported Pain Rate and Comps Reported Pivot (not opened)", "Walk through or retire"],
        ["G-11", "00:07:15–00:07:41", "The “other document” that holds the original automated requirements and timeframes", "Share it"],
        ["G-12", "00:07:00", "Cause of “UNABLE TO REFRESH – linked workbook” in Compliance Data", "Share link list"],
        ["G-13", "00:05:23", "Why Dr Saad is excluded from one overall rate", "Confirm the rule"],
        ["G-14", "whole video", "Whether the dashboard shows rates or only the compliance rows", "Share dashboard measures"],
    ], [11, 25, 92, 52])]
    s.append(c["PageBreak"]())
    return s


# --------------------------------------------------------------------------------------------
def section7(c):
    para, H, table, figref = c["para"], c["H"], c["table"], c["figref"]
    W = [13, 52, 115]
    s = [H("7. What Is Required to Build the Modern System", 0),
         para("Requirements specific to complications, each with the reason. Shared platform requirements are in spec 01 §7. The full client "
              "checklist is in <b>Complications_PreBuild_Client_Requirements.pdf</b>.")]
    s += [H("7.1 Functional requirements", 1), table([
        ["ID", "Requirement (priority)", "Why it is required"],
        ["FR-C01", "Automated appointment and SystmOne complication ingestion with validation (M)", "Both are manual today (EX-01) and the source query is unknown (G-03)."],
        ["FR-C02", "Versioned Read-code map to complication types (M)", "Codes are buried in formulas and only five infection codes are tested (FD-03, " + figref("apP") + ")."],
        ["FR-C03", "Rule-based attribution of events to appointments, with clinical review (M)", "Replaces nested INDEX/MATCH and the hand-kept log (" + figref("cd1") + ")."],
        ["FR-C04", "Computed monthly rates per type, clinician and service, with the 12-month lag for VAS failure (M)", "Counts are typed today (FM-02, " + figref("cr1") + ")."],
        ["FR-C05", "One approved, versioned standards table (M)", "Two conflicting sets of limits (SV-03, " + figref("bench") + ")."],
        ["FR-C06", "Generated compliance rows with as-of month and real result (M)", "Transfer rows are fixed “Within benchmark” text (FM-03, " + figref("cdt") + ")."],
        ["FR-C07", "Clinician master with aliases (S)", "Name variants split figures (FM-06)."],
        ["FR-C08", "Clinician overview and rate views for clinical governance (S)", "Replaces Clinician Overview, rate tabs and pivots (" + figref("clin") + ")."],
    ], W)]
    s += [H("7.2 Non-functional requirements", 1), table([
        ["ID", "Requirement", "Why it is required"],
        ["NFR-C01", "Patient-level data in a restricted zone; dashboard sees aggregates only; small-number suppression where needed", "NHS numbers and notes are in the workbook today (FM-01)."],
        ["NFR-C02", "DPIA, Caldicott Guardian approval and access audit for clinical data", "Use of identifiable patient data for service monitoring."],
        ["NFR-C03", "Reproducible monthly results (as-of month, versioned rules)", "The current result is stale and not reproducible (FM-04)."],
    ], W)]
    s += [H("7.3 Testing", 1), table([
        ["ID", "Test", "Why it is required"],
        ["T-C01", "Recalculate one historical month and match the Compliance Report figures (e.g. 12-month spike failure 0.7%, pain 2.6%)", "Parity with the numbers seen on screen (" + figref("cr2") + ")."],
        ["T-C02", "Attribution edge cases: no next appointment, two appointments same day, event before any appointment", "The formulas handle these with sentinels (00/01/1900, 1000000)."],
        ["T-C03", "Standards boundary tests per type and window", "Decides Compliant / Non-compliant."],
    ], W)]
    s += [H("7.4 Traceability", 1), table([
        ["Observed problem", "Evidence", "Removed by"],
        ["FM-01 Patient data in workbook", figref("apS"), "NFR-C01, NFR-C02"],
        ["FM-02 Typed counts", figref("cr1"), "FR-C04"],
        ["FM-03 Fixed transfer rows", figref("cdt"), "FR-C06"],
        ["FM-04 Stale result (09/04/26)", figref("cr2"), "FR-C06, NFR-C03"],
        ["FM-05 Conflicting standards", figref("bench"), "FR-C05"],
        ["FM-06 Clinician name variants", figref("vfp"), "FR-C07"],
        ["FM-07 Hard-coded row range", figref("apO"), "FR-C03"],
        ["FM-09 UNABLE TO REFRESH", figref("req"), "Shared platform (spec 01 FR-14)"],
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
        ["00:00:06", "This will be the last video, at least for now. This video deals with complications compliance."],
        ["00:00:31", "This is the most manual, I would say, of our compliance processes."],
        ["00:00:46", "There was an intention to automate it… it wasn’t anywhere near finished before Matt left."],
        ["00:00:58", "Paul Harrison was quite keen for it to appear on the dashboard… cobble together something of our own."],
        ["00:01:55", "It has a Power Query which effectively refreshes on launch of the workbook… an extract from our appointments data store."],
        ["00:02:31", "Next appointment date — I don’t know why that’s required, but it’s in there."],
        ["00:03:36", "So we wait for the appointments to refresh. We upload from System 1."],
        ["00:03:44", "We copy any new complications into the log. There’s a lookup in the log; I don’t even know what that is specifically used for."],
        ["00:04:10", "There are various pivots which we refresh after the data has been loaded in."],
        ["00:05:26", "The compliance is really a manual process whereby we count how many complications of different types have occurred in the last 12 months."],
        ["00:05:58", "We have a set of standards here; if they’re within those, they’re compliant."],
        ["00:06:30", "We copy the data from a simple table… into the bottom of our compliance data."],
        ["00:07:10", "We update our last update date… we save it and we refresh twice."],
        ["00:07:15", "The compliance timeframes and the requirements pull from another document, which was the original automated version."],
    ], [18, 162])]
    return s
