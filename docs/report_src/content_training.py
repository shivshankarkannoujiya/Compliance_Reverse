# -*- coding: utf-8 -*-
"""Specification content for the Mandatory Training recording (meeting 20260814_113314)."""
import html


def F(t):
    return '<font name="DVM" size="6.8">%s</font>' % html.escape(t)


WB = "Training Matrix v3"
DOC_TITLE = "Mandatory Training Compliance Workflow – Reverse-Engineering Specification"
HEADER = "Mandatory Training Compliance Workflow — Technical Specification (Reverse-Engineered)"
SOURCE = "Source: Teams recording 20260814_113314 (14:33)"
TITLE = "Mandatory Training Compliance Datastore Update"
SUBTITLE = ("Excel “training matrix” workflow that tracks every staff member’s mandatory courses and replaces the training rows in "
            "the compliance data store each month, reverse-engineered from an operator screen recording, with a target-state architecture")

TITLE_BLOCK = [
    ["<b>Document</b>", "Technical Specification — reverse-engineered legacy workflow (as-is) and target architecture (to-be)"],
    ["<b>Subject workflow</b>", "Mandatory training compliance (People › Training): staff register → completed-training history → role rules → "
     "Overview → <i>Compliance Transfer</i> rows that replace all training rows in <i>Compliance Data.xlsm</i>"],
    ["<b>Primary evidence</b>", "Meeting with Andrew R. Biggins-20260814_113314-Meeting Recording.mp4 — 1920×1080, 16 fps, 14:33 (873 s); camera off; "
     "audience: Dheeraj. Recorded about 30 minutes before the Complications video (“only two to go now”)"],
    ["<b>Secondary evidence</b>", "…113314….srt (timed subtitles, matches this video), …113314….txt (TurboScribe transcript), offline Whisper re-transcription"],
    ["<b>Timestamps</b>", "Video positions. Several formula-bar figures are taken at fractional seconds (shown rounded down) because the operator "
     "clicked through cells less than a second apart; each was matched to a verified frame"],
    ["<b>Companion documents</b>", "Training_PreBuild_Client_Requirements.pdf (same folder); specs 01–03"],
    ["<b>Report date</b>", "16 October 2026"],
    ["<b>Status</b>", "Draft for business-owner review. Staff names and training status are shown as recorded (they are the subject of the "
     "workflow, as in spec 01); personal email addresses are blurred"],
]

EXEC_SUMMARY_INTRO = ("<b>What the recording shows.</b> The operator walks through the <i>Training Matrix</i> workbook: orange “operational” "
                      "tabs used day to day and purple “compliance dashboard” tabs that feed the data store. A new contractor, "
                      "Dr Georgios Mousailidis, is set up live: staff list, training records, Requirements rows and Compliance Transfer rows. "
                      "The operator says the logic was rebuilt from scratch because Matt “couldn’t actually remember” how it worked.")

EXEC_SUMMARY = [
    "<b>The richest model of the four tools.</b> Training validity is computed per record: expiry vs TODAY(), a 45-day “Expiring” window, "
    "role-based requirements (Roles_Training12) and course supersession (e.g. Safeguarding Adults Level 3 supersedes lower levels).",
    "<b>The data store cannot hold training history.</b> The data store’s “Most Recent” MAXIFS formula “doesn’t seem to work for mandatory "
    "training”, so each month the operator <b>deletes every existing training row</b> in Compliance Data and pastes the full current set. "
    "History survives only inside the matrix.",
    "<b>Likely root cause [Inferred]:</b> the transfer’s Completion Date column mixes real dates with the text “Invalid - No Record” and “N/A”, "
    "and MAXIFS ignores text; together with one row per person per course every month, the most-recent test cannot work as intended.",
    "<b>Requirements are hand-copied.</b> For a new starter, 13 rows are pasted and Required TRUE/FALSE typed per course, although the "
    "Roles tab already defines what each role needs, so the two can disagree.",
    "<b>Thresholds disagree:</b> Overview targets are 90%/95% per course, while Compliance Timeframes thresholds are 1/0.99/0.95/0.9/0.8 and the "
    "operator says Information Governance “should really be 0.95”. Every x months is again 0.5 (“Only Matt knows”).",
    "<b>Leftovers:</b> Course Detail and Staff Filter tabs show #REF!; a Training Intervals table still has Medical Devices headers "
    "(“Equipment Type”, “Max permitted days between services”); several tabs are “never been used”.",
]


# --------------------------------------------------------------------------------------------
def section0(c):
    para, H, table, bullets = c["para"], c["H"], c["table"], c["bullets"]
    s = [H("0. Evidence Base, Method &amp; Reading Guide", 0)]
    s += [H("0.1 Source artefacts", 1), table([
        ["Artefact", "What it is", "Used for"],
        ["…20260814_113314-Meeting Recording.mp4", "Teams recording, 1920×1080, 16 fps, 14:33. Git-LFS object, 96 MB", "Screenshots, step timings"],
        ["…20260814 113314-Meeting Recording.srt", "Timed subtitles of the same meeting", "Timestamp anchors"],
        ["…20260814 113314-Meeting Recording.txt", "TurboScribe transcript", "Wording"],
        ["Author ASR (Whisper small.en)", "Independent re-transcription", "Cross-check"],
    ], [52, 78, 50])]
    s += [H("0.2 Method and redaction", 1)] + bullets([
        "Frames extracted with ffmpeg; the 1 fps grid ran about 1 s ahead and was corrected. Formula-bar figures were matched to verified frames at 0.25 s steps.",
        "Redaction: the Email Address column of the staff list is blurred. Staff names, roles and training status are left, as in spec 01, because they are "
        "the subject of the workflow; free-text HR comments appear in a few figures and should be treated as confidential when sharing.",
        "Confidence tags: <b>[Seen]</b>, <b>[Said]</b>, <b>[Inferred]</b>, <b>[Unknown]</b>.",
    ])
    s.append(c["PageBreak"]())
    return s


# --------------------------------------------------------------------------------------------
def section1(c):
    para, H, table, figure, figref = c["para"], c["H"], c["table"], c["figure"], c["figref"]
    s = [H("1. Complete File, Workbook &amp; Sheet Inventory", 0)]
    s += [H("1.1 Files and external systems", 1), table([
        ["#", "File / system", "Role", "Evidence"],
        ["F1", "<b>Training Matrix v3</b> (Excel; extension not shown, AutoSave off)", "Training register, history, rules, overview and transfer table", figref("asl")],
        ["F2", "<b>Compliance Data.xlsm</b>", "Data store: training rows replaced monthly; Last Updated", figref("cdM") + ", " + figref("lu")],
        ["S1", "ESR (Wellbeing staff)", "Monthly compliance report for substantive staff [Said]", "00:04:26"],
        ["S2", "Workforce Solutions (WFS)", "Monthly report for workers engaged through WFS [Said]", "00:04:26"],
        ["S3", "Provide CIC L&amp;D", "Monthly report for staff with a substantive Provide CIC post [Said]", "00:04:26"],
        ["S4", "Direct contractors", "No report: the team emails each contractor for certificates [Said]", "00:04:25"],
    ], [8, 50, 92, 30])]
    s += [H("1.2 Worksheet tabs in Training Matrix v3", 1), table([
        ["Tab", "Colour / role", "Opened"],
        ["<b>All Staff List_Comments</b> (Table1)", "Orange, operational: staff register", "00:00:32–00:02:52"],
        ["<b>Completed Training</b> (Training_History4)", "Orange: every training record ever (about 4,229)", "00:02:07–00:02:40, 00:13:21"],
        ["<b>Overview</b>", "Orange: current-staff compliance grid", "00:03:13–00:05:05"],
        ["<b>Overview (Onboarding)</b>", "Orange: onboarding staff grid (not sent to the data store)", "00:02:55–00:03:12"],
        ["OMcGOW", "Orange: Oliver McGowan training tracker [Inferred]", "Tab only"],
        ["<b>Requirements</b>", "Purple, dashboard: person × course requirements", "00:05:16–00:08:58"],
        ["<b>Compliance Timeframes</b>", "Purple: catalogue and thresholds", "00:10:29–00:11:20"],
        ["<b>Compliance Transfer</b>", "Purple: rows to paste into the data store", "00:00:40, 00:08:58–00:10:29, 00:12:35"],
        ["<b>Roles</b> (Roles_Training12)", "Reference: role × training × required", "00:11:24"],
        ["<b>Training Details</b>", "Reference: course intervals and supersession", "00:11:36"],
        ["Training Intervals", "Reference with Medical Devices headers (cloned)", "00:11:43"],
        ["Dropdowns", "Lists for the Overview pickers", "00:11:44"],
        ["Course Detail · Nurses · Staff Filter", "“Never been used”; #REF! errors seen", "00:11:50–00:11:56"],
        ["Transfer from v… · Role Rules", "Partly visible names; Role / Training / Required / Role Lookup table", "00:12:00"],
    ], [60, 85, 35])]
    s += [H("1.3 Overview screenshots", 1), figure("rec", 70 * c["mm"]), figure("ctr0")]
    s.append(c["PageBreak"]())
    return s


# --------------------------------------------------------------------------------------------
def section2(c):
    para, H, table, figure, figref = c["para"], c["H"], c["table"], c["figure"], c["figref"]
    mm = c["mm"]
    W = [9, 34, 22, 15, 100]
    hdr = ["Col", "Header", "Type", "Origin", "Lineage, rule and evidence"]
    s = [H("2. Exhaustive Column-Level Schema &amp; Data Lineage Catalogue", 0),
         para("Origin: <b>MAN</b> = typed by the operator (often from an ESR / WFS / L&amp;D report or a contractor’s certificate); <b>CALC</b> = formula.")]
    s += [H("2.1 All Staff List_Comments (Table1)", 1), table([hdr,
        ["A", "Staff Name", "Text · key", "MAN", "Natural key for every lookup (e.g. “Dr Georgios Mousailidis”, with or without “Dr”)"],
        ["B", "Email Address", "Text", "MAN", "Free text, sometimes several addresses (blurred)"],
        ["C", "Employer", "List", "MAN", "Wellbeing · Contractor (Direct) · Workforce Solutions · Provide CIC: decides how training evidence is obtained"],
        ["D", "Service", "Text", "MAN", "SURGICAL, ND, CORPORATE SERVICES …"],
        ["E", "Training System", "Text", "MAN", "ESR, Direct, WFS, Provide L&amp;D"],
        ["F", "Works With", "Text", "MAN", "Adult / Children / Both"],
        ["G", "Role", "Text", "MAN", "e.g. Registered Practitioner, Neurodevelopmental, Business Admin (Virtual)"],
        ["H", "Role Lookup", "Text", "CALC", F('=CONCAT([@Role]," - ",[@[Works With]])') + " → key into Roles. " + figref("asH")],
        ["I–J", "Start Date, End Date", "Date / text", "MAN", "Mixed formats: “22-Oct”, “01-Dec”, “20-Jan” stored as text"],
        ["K", "Current Staff", "Y/N", "CALC", F('=IF([@[Staff Name]]<>"",IF([@Status]<>"Onboarding",IF(AND([@[Start Date]]<=TODAY(),OR([@[End Date]]>TODAY(),[@[End Date]]="")),"Y","N"),"N"))') + ". " + figref("asK")],
        ["L", "Role2", "Text", "MAN", "Short role (GPwSI, Nurse, OSALT …)"],
        ["M", "Status", "List", "MAN", "Live / Inactive / Onboarding / blank"],
        ["N", "Last Review", "Date", "MAN", "Date of last check"],
        ["O", "Notes", "Text", "MAN", "Running commentary (“SG Children L3 booked 1/2 Sept 26 …”), pulled into Requirements and the data store"],
    ], W), figure("asl"), figure("asH"), figure("asK")]
    s += [H("2.2 Completed Training (Training_History4)", 1), table([hdr,
        ["A", "Name", "Text", "MAN", "Staff name"],
        ["B", "Training", "Text", "MAN", "Course name as recorded"],
        ["C", "Completed Date", "Date", "MAN", "From the report or certificate"],
        ["D", "Expiry Date", "Date", "MAN/CALC", "Completion + interval [Inferred]"],
        ["E", "Valid/Expired", "Text", "CALC", "“One Off” → Valid; expiry &gt; TODAY()+45 → Valid; within 45 days → “Expiring - date”; blank → “Invalid - No Record”; Not Required → “Valid - Not Required - Expiry Date …”; else “Invalid - date”. " + figref("ctE")],
        ["F", "Is Superseded", "Boolean", "CALC", "TRUE when a higher course (Superseded By 1/2) exists for the person. " + figref("ctF")],
        ["G", "Supersedes", "Boolean", "CALC", "TRUE when this course replaces a lower one"],
        ["H–K", "Superseded By 1/2, Supersedes 1/2", "Text", "CALC", "From Training Details"],
        ["L", "Valid For (Days)", "Integer", "CALC", F('=XLOOKUP([@Training],Training_Details[Training],Training_Details[Interval],"")') + " (365, 730, 1095)"],
        ["M", "Lookup 1", "Text", "CALC", F('=CONCAT([@Training],"-",[@Name])')],
        ["N", "Most Recent Training Session Lookup", "Text", "CALC", "Most recent record per course and person [Inferred]"],
        ["O", "Course Name", "Text", "CALC", "Course group when the record counts. " + figref("ctO")],
        ["P", "Final Lookup", "Text", "CALC", F('=IF([@[Course Name]]<>"",CONCAT([@[Course Name]],"-",[@Name]),"")')],
        ["Q", "Final Lookup 2", "Text", "CALC", F('=IF([@[Final Lookup]]<>"",IF(MAXIFS([Completed Date],[Final Lookup],[@[Final Lookup]])=[@[Completed Date]],[@[Final Lookup]],""),"")') + ": only the newest completion keeps a key. " + figref("ctQ")],
        ["R", "Requirement", "Text", "CALC", "Required if the role needs this course or the course it supersedes. " + figref("ctR")],
        ["S", "Role", "Text", "CALC", F('=XLOOKUP([@Name],Table1[Staff Name],Table1[Role Lookup],"")')],
    ], W), figure("ctg"), figure("ctE"), figure("ctR"), figure("ctQ"), figure("ctO"), figure("ctF")]
    s += [H("2.3 Overview and Overview (Onboarding)", 1),
          para("Both use " + F('=FILTER(Table1[Staff Name],(Table1[Current Staff]="Y")*IF(A3="All",…,(Table1[Role]=A3))*IF(B3="All",…,(Table1[Employer]=B3))*IF(C3="All",…,(Table1[Service]=C3)))') +
               " (Onboarding: Status = \"Onboarding\"). Each course cell looks up the person’s Final Lookup 2 record and shows its Valid/Expired text; "
               "row 4 holds per-course targets (90% or 95%); row 6 “Overall” is the share of Valid cells. " + figref("ovF")),
          figure("ovo"), figure("ovF"), figure("ovw"), figure("ove")]
    s += [H("2.4 Requirements", 1), table([hdr,
        ["A", "Name", "Text", "MAN", "Pasted"],
        ["B", "Compliance Type", "Text", "MAN", "Course (13 per person for the new starter)"],
        ["C", "Required (T/F)", "Boolean", "MAN", "Typed per course, e.g. Equality and Diversity FALSE for a contractor"],
        ["D", "Core Requirement", "Text", "MAN", "Core (“anything required is core”)"],
        ["E", "Notes", "Text", "CALC", F('=XLOOKUP([@Name],Table1[Staff Name],Table1[Notes],"")') + ". " + figref("reqE")],
        ["F", "Managed By", "Text", "MAN", "Provide Wellbeing"],
        ["G", "Unique Lookup", "Text", "CALC", F('=CONCAT([@Name],"-",[@[Compliance Type]])')],
        ["H", "Compliance Timeframe", "Number", "MAN", "0.5 (constant)"],
        ["I", "Active", "Text TRUE/FALSE", "CALC", F('=IF(OR(XLOOKUP([@Name],Table1[Staff Name],Table1[Current Staff],"")="N",XLOOKUP(…)=""),"FALSE","TRUE")') + " — returns <b>text</b> “TRUE”/“FALSE”, not booleans. " + figref("reqI")],
    ], W), figure("reqI"), figure("reqE")]
    s += [H("2.5 Compliance Transfer (rows copied to the data store)", 1), table([hdr,
        ["A", "(status helper)", "Text", "CALC", "Valid/Expired text for the person and course [Inferred from F]"],
        ["B", "(role)", "Text", "CALC", "Role Lookup, used for the Required test"],
        ["C", "Name", "Text", "MAN", "Pasted"],
        ["D", "Compliance Type", "Text", "MAN", "Pasted"],
        ["E", "Completion Date", "<b>Date or text</b>", "CALC", "Final Lookup 2 → Completed Date, else “Invalid - No Record” or “N/A”. " + figref("trE")],
        ["F", "Completion Status", "Text", "CALC", F('=IF(OR(A="Valid",LEFT(A,3)="Exp"),"Completed",IF(A="N/A","Not Required",""))') + ". " + figref("trF")],
        ["G", "Issue", "Number", "MAN", "10, filled down (“that’s our RAG rating, I think, which clearly makes no difference”)"],
        ["H", "Compliance Notes", "Text", "CALC", "From Table1 Notes"],
        ["I", "Managed By", "Text", "MAN", "Provide Wellbeing"],
        ["J", "Due Date", "Date or text", "CALC", "Final Lookup 2 → Expiry Date, else text; 00/01/1900 seen for empty values. " + figref("trJ")],
        ["K–N", "Compliance Group Level 1–4", "Text", "CALC", "People, Training, plus " + F('=SUBSTITUTE(XLOOKUP(D,Compliance_Timeframe_Table[Compliance Type],Compliance_Timeframe_Table[Compliance Group 3],""),0,"")') + " for levels 3–4"],
        ["O", "Weighting", "Number", "MAN", "1"],
    ], W), figure("trN"), figure("trE"), figure("trF"), figure("trJ")]
    s += [H("2.6 Reference tabs", 1), table([
        ["Tab", "Content", "Notes"],
        ["Compliance Timeframes", "Course, Every x months 0.5, Core, People › Training, Groups 3/4 (Safeguarding, Clinical), Unique Lookup, Missing TRUE, Threshold 1–5 = 1/0.99/0.95/0.9/0.8", "Thresholds differ from Overview targets"],
        ["Roles (Roles_Training12)", "Role (e.g. Head of Service - Adult), Training, Required Y/N, Superseded By 1/2, Course Name, Lookup 1/2", "Defines what each role needs"],
        ["Training Details", "Training, Superseded By 1/2, Supersedes 1/2, Interval (days), Course Group", "Interval drives expiry"],
        ["Training Intervals", "Headers “Equipment Type”, “Max permitted days between services”, Required", "Copied from the Medical Devices tool"],
        ["Role Rules / Course Detail / Staff Filter / Nurses", "Role × Training × Required; per-group grids", "#REF! errors; “never been used”"],
    ], [38, 100, 42]), figure("ctt"), figure("rol"), figure("trd"), figure("ddn")]
    s += [H("2.7 Compliance Data.xlsm", 1),
          para("The data store’s Compliance Data table adds calculated columns: " + F('Most Recent =IF(MAXIFS([Completion Date],[Unique Lookup],[@[Unique Lookup]],[Compliance Type],[@[Compliance Type]])=0,TRUE,MAXIFS(…)=[@[Completion Date]])') +
               ", Compliant, Expires within 3 months, Weeks Non Compliant, Core Requirement, Unique Lookup. Training rows break this test (see §4.3)."),
          figure("cdM"), figure("lu")]
    s.append(c["PageBreak"]())
    return s


# --------------------------------------------------------------------------------------------
STEPS = [
    (1, "00:00:00", "00:00:30", "Introduce mandatory training compliance", "Camera off; screen share starts via the Teams share picker.", "—", "—", ["rec"]),
    (2, "00:00:30", "00:01:19", "Tour the tabs", "“These orange tabs are operational… these ones are compliance dashboard tabs.” Shows Compliance Transfer and the staff list.", "—", "—", ["ctr0", "asl"]),
    (3, "00:01:19", "00:01:44", "Current staff, last review and notes", "Explains Current Staff (people on hold or leaving), Last Review and Notes.", "—", "—", ["asH", "asK"]),
    (4, "00:01:44", "00:02:07", "Add the new starter to the staff list", "Dr Georgios Mousailidis typed into row 42 with employer Contractor (Direct), service ND, role.", "Manual → Table1 row 42", "Row 42 added", []),
    (5, "00:02:07", "00:02:45", "Record his training in Completed Training", "13 course rows with completed dates; operator clicks through the calculated columns.", "Certificates → Training_History4", "13 rows; Valid/Expired computed", ["ctg", "ctE", "ctR", "ctQ", "ctO", "ctF"]),
    (6, "00:02:45", "00:03:13", "Mark as Onboarding", "Status M42 = Onboarding, so he appears only in Overview (Onboarding), “not included in the compliance data”.", "Status → Current Staff N", "Current Staff = N", ["new1", "ovo"]),
    (7, "00:03:13", "00:05:16", "Use the Overview and the four employer groups", "Filters by Employer. Wellbeing (ESR), Workforce Solutions and Provide CIC staff come with monthly reports; Contractor (Direct) staff are chased directly. “Over the month we build up our table.”", "Reports / emails → Completed Training", "Updated during the month", ["ovF", "ovw", "ove"]),
    (8, "00:05:16", "00:06:58", "Explain the Requirements table", "Name, course, required, core, notes (“from Table1”), managed by, timeframe 0.5 (“does it mean twice a month? Only Matt knows”), Active (“if I can see the person on this list, that person’s active”).", "—", "—", ["reqI", "reqE"]),
    (9, "00:06:58", "00:08:58", "Add Requirements rows for the new starter", "Copies a block of course rows, pastes the name, types Required per course (E&amp;D no, Fire Safety yes, Learning Disabilities no, Moving and Handling yes, SG Adults/Children yes, BLS yes, Conflict Resolution no, H&amp;S yes, Oliver McGowan no, DSE yes), Core, managed by. Active shows FALSE (onboarding).", "Manual copy-paste → Requirements", "13 rows added", ["reqA"]),
    (10, "00:08:58", "00:10:29", "Add Compliance Transfer rows", "Copies rows, pastes the name; formulas fill. Moving and Handling shows Not Required (“he hasn’t got the correct moving and handling as yet”). Issue filled down.", "Manual copy-paste → Compliance Transfer", "Rows added", ["trN", "trE", "trF", "trJ"]),
    (11, "00:10:29", "00:11:24", "Compliance Timeframes and thresholds", "0.5 months, core, People › Training; Missing TRUE (“I don’t know what that means”); thresholds (“IG should really be 0.95”).", "—", "—", ["ctt"]),
    (12, "00:11:24", "00:12:35", "Reference and unused tabs", "Roles, Training Details, Training Intervals, Dropdowns; Course Detail, Nurses, Staff Filter “never been used”. Matt “couldn’t remember… so I basically figured it out from scratch”.", "—", "—", ["rol", "trd", "ddn"]),
    (13, "00:12:35", "00:13:21", "Monthly publish: replace training rows in the data store (described)", "“We go to compliance transfer, we copy this in… the most recent formula doesn’t seem to work for mandatory training, so I delete the existing training data in this table and copy in the latest one.” Rows are selected; the delete and paste are not performed on screen.", "Compliance Transfer → Compliance Data (delete + paste)", "Not performed", ["cpy", "cdM"]),
    (14, "00:13:21", "00:14:10", "History lives in the matrix", "Shows Adele Brignell’s Information Governance history 2022→2027: “if someone says, were they compliant in August 23? We can say yes.”", "—", "—", ["hist"]),
    (15, "00:14:10", "00:14:33", "Last updated, save, refresh twice", "“We update our last updated date. We save, refresh twice.” Last Updated shown (People-Training 23/07/2026). End.", "Manual → Last Updated", "Not performed", ["lu"]),
]


def section3(c):
    para, H, table, figure = c["para"], c["H"], c["table"], c["figure"]
    s = [H("3. Chronological Step-by-Step Operator Workflow", 0),
         para("Fifteen steps cover the 14:33 recording. Steps 4–10 are performed live for the new starter; the monthly publish (steps 13 and 15) is described only."),
         table([["Step", "Window", "Action"]] + [[str(x[0]), x[1] + "–" + x[2], x[3]] for x in STEPS], [10, 34, 136]), c["PageBreak"]()]
    for n, a, b, title, act, mp, mut, figs in STEPS:
        s += [H("Step %d [%s – %s]: %s" % (n, a, b, title), 1),
              table([["<b>Action performed</b>", act], ["<b>Source → target</b>", mp], ["<b>State mutation</b>", mut]], [38, 142], head=False, zebra=False)]
        s += [figure(f) for f in figs]
        s.append(c["Spacer"](1, 6))
    s.append(c["PageBreak"]())
    return s


# --------------------------------------------------------------------------------------------
def section4(c):
    para, H, table, figref = c["para"], c["H"], c["table"], c["figref"]
    s = [H("4. Data Quality Checks, Manual Exceptions &amp; Edge Cases", 0)]
    s += [H("4.1 Business rules", 1), table([
        ["ID", "Rule", "Evidence"],
        ["BR-01", "A training record is valid until Completed Date + course interval; “Expiring” in the last 45 days; “One Off” courses never expire", figref("ctE")],
        ["BR-02", "Which courses a person needs depends on Role + Works With (Roles table)", figref("rol")],
        ["BR-03", "A higher course supersedes lower ones (Superseded By / Supersedes)", figref("ctF")],
        ["BR-04", "Only the most recent completion of a course counts (MAXIFS)", figref("ctQ")],
        ["BR-05", "Current staff = started, not ended, not onboarding; onboarding staff are excluded from compliance data", figref("asK")],
        ["BR-06", "Anything required is core", "Said 00:08:32"],
        ["BR-07", "Evidence route depends on employer: ESR / WFS / Provide CIC monthly reports; direct contractors chased by email", "Said 00:03:28–00:04:35"],
        ["BR-08", "Per-course targets 90%/95% on the Overview", figref("ovw")],
    ], [12, 128, 40])]
    s += [H("4.2 Manual steps", 1), table([
        ["ID", "Manual step", "Risk"],
        ["EX-01", "Training dates typed from monthly reports and certificates", "Typing errors; no link to the source report"],
        ["EX-02", "New starter set up in three places by copy-paste (Completed Training, Requirements, Compliance Transfer)", "Rows missing or inconsistent between tabs"],
        ["EX-03", "Required TRUE/FALSE typed per course on Requirements", "Can disagree with the Roles table"],
        ["EX-04", "Monthly: delete all training rows in Compliance Data, paste the full transfer set", "Deleting the wrong rows; partial paste; history lost in the store"],
        ["EX-05", "Last Updated edited by hand; save; refresh twice", "Forgotten step"],
    ], [12, 90, 78])]
    s += [H("4.3 Spoken vs visual discrepancies and defects", 1), table([
        ["ID", "Said / intended", "Seen", "Impact"],
        ["SV-01", "Store keeps the most recent record (“with everything else you can just put it on the bottom”)", "Most Recent MAXIFS fails for training; rows deleted and replaced", "No training history in the data store; dashboard can’t show trends"],
        ["SV-02", "Completion Date is a date", "Transfer column E mixes dates with “Invalid - No Record” and “N/A” text; Due Date shows 00/01/1900", "MAXIFS ignores text → probable cause of SV-01 [Inferred]"],
        ["SV-03", "Required = what the role needs", "Typed by hand per person while Roles_Training12 already holds it", "Requirements and Overview can disagree"],
        ["SV-04", "“IG should really be 0.95” (00:11:09)", "Threshold 2 = 0.99; Overview target IG = 95%", "Two thresholds for the same course"],
        ["SV-05", "Timeframe 0.5 (“Only Matt knows”, 00:06:34)", "0.5 in Requirements and Timeframes", "Meaning unknown"],
        ["SV-06", "Issue = “our RAG rating… makes no difference”", "Constant 10", "Field without meaning in the store"],
        ["SV-07", "Active flag", "Requirements!I returns text “TRUE”/“FALSE”", "Type mismatch with other tools’ boolean Active"],
        ["SV-08", "Moving and Handling required for the new starter", "Transfer shows Not Required until the correct course is recorded (00:09:20)", "Requirement depends on what was completed, not only on role"],
        ["FD-01", "Unused tabs", "Course Detail and Staff Filter show #REF!; Training Intervals has Medical Devices headers", "Dead logic in the workbook"],
        ["FD-02", "Dates", "End Date values such as “22-Oct”, “01-Dec” stored as text", "Current Staff can be wrong for those people"],
        ["FD-03", "Data store refresh", "“UNABLE TO REFRESH – linked workbook”", "Stale lookups"],
    ], [12, 50, 62, 56])]
    s += [H("4.4 Hidden failure modes", 1), table([
        ["ID", "Failure mode", "Severity"],
        ["FM-01", "<b>Destructive monthly replace</b> of all training rows in the data store", "High"],
        ["FM-02", "<b>Mixed-type date columns</b> passed into the store", "High"],
        ["FM-03", "<b>Name as key</b> across four tables (“Dr” prefix variations)", "High"],
        ["FM-04", "<b>Triple manual set-up</b> per new starter", "Medium"],
        ["FM-05", "<b>Requirements not derived from role rules</b>", "Medium"],
        ["FM-06", "<b>TODAY()-based validity</b>: results change daily and past months cannot be reproduced", "Medium"],
        ["FM-07", "<b>Text dates</b> in staff list", "Medium"],
        ["FM-08", "<b>Knowledge loss</b>: logic reconstructed after the author left", "Medium"],
        ["FM-09", "<b>Personal data spread</b>: emails and HR notes copied into requirements and the data store", "Medium (IG)"],
    ], [12, 148, 20])]
    s.append(c["PageBreak"]())
    return s


# --------------------------------------------------------------------------------------------
def section5(c):
    para, H, table, bullets, code = c["para"], c["H"], c["table"], c["bullets"], c["code"]
    s = [H("5. Target Modern System Architecture Blueprint", 0),
         para("Training runs on the shared platform (spec 01 §5). It needs the most domain logic of the four areas: course catalogue with "
              "intervals and supersession, role rules, and per-person training events from several sources.")]
    s += [H("5.1 Ingestion", 1)] + bullets([
        "<b>ESR, WFS and Provide CIC L&amp;D reports:</b> monthly files uploaded (or fetched) with a header contract per source; rows matched to staff by "
        "employee number / alias, not by name.",
        "<b>Direct contractors:</b> certificate upload in the web form (or a contractor self-service link) with the completion date checked by a reviewer.",
        "<b>Validation:</b> known course (or mapped alias), completion date not in the future, staff exists.",
    ])
    s += [H("5.2 Data model additions", 1), table([
        ["Table", "Key columns", "Replaces"],
        ["<b>ref.course</b> (versioned)", "course_id, name, interval_days (NULL = one-off), course_group, valid_from/to", "Training Details"],
        ["<b>ref.course_supersession</b>", "course_id, supersedes_course_id", "Superseded By / Supersedes columns"],
        ["<b>ref.role_course_rule</b> (versioned)", "role_id, works_with, course_id, required, valid_from/to, approved_by", "Roles_Training12"],
        ["<b>core.staff</b> (shared subject)", "staff_id, employer_id, service_id, role_id, works_with, start_date, end_date, status", "All Staff List"],
        ["<b>core.training_event</b> (append-only)", "event_id, staff_id, course_id, completed_on, source (ESR/WFS/L&amp;D/certificate), evidence_file_id, batch_id", "Completed Training"],
        ["<b>mart.training_status</b> (view)", "staff_id, course_id, required, latest_completed_on, expires_on, status (Valid/Expiring/Expired/Missing/Not required), as_of_date", "Overview, Compliance Transfer"],
    ], [42, 103, 35])]
    s += [H("5.3 Rules as SQL", 1), code(
        "-- Requirement is derived from role rules, never typed per person\n"
        "CREATE VIEW mart.v_training_requirement AS\n"
        "SELECT s.staff_id, r.course_id, r.required\n"
        "FROM core.staff s JOIN ref.role_course_rule r\n"
        "  ON r.role_id = s.role_id AND r.works_with IN (s.works_with, 'Both');\n\n"
        "-- Latest event per course, counting superseding courses (BR-03, BR-04)\n"
        "SELECT q.staff_id, q.course_id, max(e.completed_on) AS latest_completed_on\n"
        "FROM mart.v_training_requirement q\n"
        "JOIN core.training_event e ON e.staff_id = q.staff_id\n"
        " AND (e.course_id = q.course_id OR e.course_id IN\n"
        "      (SELECT course_id FROM ref.course_supersession WHERE supersedes_course_id = q.course_id))\n"
        "GROUP BY q.staff_id, q.course_id;\n\n"
        "-- Status at the publication's as-of date (BR-01): Expiring within 45 days\n"
        "CASE WHEN c.interval_days IS NULL THEN 'Valid'\n"
        "     WHEN latest + c.interval_days > as_of + 45 THEN 'Valid'\n"
        "     WHEN latest + c.interval_days > as_of THEN 'Expiring'\n"
        "     WHEN latest IS NULL THEN 'Missing' ELSE 'Expired' END")]
    s += bullets([
        "Completion and expiry dates stay typed dates; “missing” and “not required” are statuses, not text in a date column (fixes FM-02).",
        "History is kept as events, so the store never needs a delete-and-replace (fixes FM-01) and “were they compliant in August 23?” is a query.",
        "Onboarding staff are a status; the onboarding view is the same query filtered on status.",
    ])
    s += [H("5.4 Review and publication", 1)] + bullets([
        "New-starter wizard creates the staff record once; requirements follow from the role (fixes FM-04, FM-05).",
        "Monthly report import shows a diff (new completions, newly expiring, still missing) for review before publishing.",
        "Publication writes one status row per staff × required course for the as-of month inside the shared atomic publish; Last Updated is automatic.",
    ])
    s.append(c["PageBreak"]())
    return s


# --------------------------------------------------------------------------------------------
def section6(c):
    H, table = c["H"], c["table"]
    s = [H("6. Gap &amp; Ambiguity Register", 0), table([
        ["ID", "Timestamp", "Gap / ambiguity", "Ask"],
        ["G-01", "00:12:51", "Exactly why Most Recent fails for training (text dates assumed)", "Confirm with a copy of Compliance Data"],
        ["G-02", "00:06:34", "Meaning of Compliance Timeframe 0.5", "Define cadence"],
        ["G-03", "00:09:55", "Meaning of Issue = 10", "Define or drop"],
        ["G-04", "00:11:09", "Authoritative targets/thresholds per course", "Business owner to decide"],
        ["G-05", "00:04:26", "Format and frequency of ESR, WFS and Provide CIC reports", "Share samples"],
        ["G-06", "00:02:07", "How Expiry Date is filled (typed or calculated)", "Confirm"],
        ["G-07", "00:11:50", "Whether Course Detail, Nurses, Staff Filter, Transfer from v…, Role Rules, OMcGOW are needed", "Walk through or retire"],
        ["G-08", "00:12:13", "Whether the dashboard uses the transfer rows as-is (“not sure if these are used in the dashboard”)", "Share dashboard measures"],
        ["G-09", "00:09:20", "Why Moving and Handling becomes Not Required before the correct course is recorded", "Confirm role rule"],
        ["G-10", "00:01:00", "Whether Contract/Status/Last Review values follow a defined list", "Share lists"],
        ["G-11", "whole video", "File name and extension of the matrix (.xlsx or .xlsm) and any VBA", "Share the workbook"],
    ], [11, 22, 95, 52])]
    s.append(c["PageBreak"]())
    return s


# --------------------------------------------------------------------------------------------
def section7(c):
    para, H, table, figref = c["para"], c["H"], c["table"], c["figref"]
    W = [13, 52, 115]
    s = [H("7. What Is Required to Build the Modern System", 0),
         para("Training-specific requirements with reasons. Shared platform requirements are in spec 01 §7. The client checklist is "
              "<b>Training_PreBuild_Client_Requirements.pdf</b>.")]
    s += [H("7.1 Functional requirements", 1), table([
        ["ID", "Requirement (priority)", "Why it is required"],
        ["FR-T01", "Course catalogue with intervals, groups and supersession (M)", "Validity and supersession are the core rules (" + figref("ctE") + ", " + figref("ctF") + ")."],
        ["FR-T02", "Role rules that generate requirements (M)", "Requirements are typed by hand today (SV-03, " + figref("reqA") + ")."],
        ["FR-T03", "Append-only training events with source and evidence (M)", "History only exists in the matrix; the store is wiped monthly (FM-01)."],
        ["FR-T04", "Report import for ESR, WFS and Provide CIC with staff matching by ID (M)", "Dates are typed from reports (EX-01)."],
        ["FR-T05", "Contractor certificate upload and reviewer check (S)", "Direct contractors are chased by email (BR-07)."],
        ["FR-T06", "Status view (Valid / Expiring / Expired / Missing / Not required) at an as-of date (M)", "Replaces TODAY()-based text (FM-06)."],
        ["FR-T07", "New-starter wizard and onboarding status (M)", "Three manual copy-pastes per starter (FM-04)."],
        ["FR-T08", "One target table per course for overview and dashboard (S)", "Targets and thresholds disagree (SV-04)."],
        ["FR-T09", "Expiry reminders to staff and managers (S)", "The team chases expiries by hand."],
    ], W)]
    s += [H("7.2 Non-functional requirements", 1), table([
        ["ID", "Requirement", "Why it is required"],
        ["NFR-T01", "Contact details and HR notes restricted; dashboard shows status only", "Emails and comments are copied into several tables (FM-09)."],
        ["NFR-T02", "Typed date columns end to end", "Mixed date/text columns break the store (FM-02)."],
        ["NFR-T03", "Reproducible monthly snapshots", "Past compliance must be answerable (“were they compliant in August 23?”)."],
    ], W)]
    s += [H("7.3 Testing", 1), table([
        ["ID", "Test", "Why it is required"],
        ["T-T01", "Golden case: Dr Georgios Mousailidis (13 courses, onboarding) and Adele Brignell’s Information Governance history 2022–2027", "Two fully visible cases."],
        ["T-T02", "Supersession: Safeguarding Adults Level 3 satisfies lower levels", "BR-03."],
        ["T-T03", "Boundary: 45-day expiring window, one-off courses, missing record, not required", "BR-01."],
        ["T-T04", "Parity: one month’s Overview percentages vs the new view", "Proves the logic matches."],
    ], W)]
    s += [H("7.4 Traceability", 1), table([
        ["Observed problem", "Evidence", "Removed by"],
        ["FM-01 Delete-and-replace in the store", figref("cdM"), "FR-T03"],
        ["FM-02 Mixed date/text", figref("trE"), "NFR-T02, FR-T06"],
        ["FM-03 Name as key", figref("asl"), "FR-T04 (staff IDs)"],
        ["FM-04 Triple set-up", figref("reqA"), "FR-T07"],
        ["FM-05 Requirements typed", figref("reqA"), "FR-T02"],
        ["FM-06 TODAY()", figref("ctE"), "FR-T06, NFR-T03"],
        ["SV-04 Conflicting thresholds", figref("ctt"), "FR-T08"],
        ["FD-01 Dead tabs with #REF!", figref("ddn"), "Not migrated"],
    ], [62, 58, 60])]
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
        ["00:00:05", "Only two to go now. This one is mandatory training compliance."],
        ["00:00:33", "These orange tabs here are operational tabs. These ones are compliance dashboard tabs."],
        ["00:01:19", "There’s a formula there to say whether the staff is current or not."],
        ["00:01:44", "We’re just engaging Dr Georgios Mousailidis."],
        ["00:02:45", "We would then usually stipulate him to be onboarding… which is obviously not included in the compliance data."],
        ["00:03:28", "Our workers and contractors fall into four categories."],
        ["00:05:24", "We will add that member of staff to the requirements table."],
        ["00:06:34", "Does it mean it should be done twice a month? Only Matt knows."],
        ["00:08:58", "We also need to set him up on our compliance transfer."],
        ["00:11:09", "That should really be 0.95."],
        ["00:11:50", "Course detail, never been used. Nurses, never been used. Staff filter, never been used."],
        ["00:12:22", "So I basically figured it out from scratch."],
        ["00:12:51", "The most recent record formula… doesn’t seem to work for mandatory training."],
        ["00:13:09", "I delete the existing training data in this table and then copy in the latest one."],
        ["00:13:58", "If someone says, were they compliant in August 23? We can say yes."],
        ["00:14:16", "We save, refresh twice. It builds the table, which then informs the dashboard."],
    ], [18, 162])]
    return s
