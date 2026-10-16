# -*- coding: utf-8 -*-
"""Specification content for the RTT recording (sixth/MEDDAD~1.MP4)."""
import html


def F(t):
    return '<font name="DVM" size="6.8">%s</font>' % html.escape(t)


DOC_TITLE = "RTT Compliance Workflow – Reverse-Engineering Specification"
HEADER = "RTT (Referral to Treatment) Compliance Workflow — Technical Specification (Reverse-Engineered)"
SOURCE = "Source: Teams recording MEDDAD~1.MP4 (8:42)"
TITLE = "RTT Compliance Datastore Update"
SUBTITLE = ("Weekly referral-to-treatment (18-week) compliance per service: SystmOne download → RTT breach report → "
            "RTT Data workbook → ten compliance rows in the data store, reverse-engineered from an operator screen recording")

TITLE_BLOCK = [
    ["<b>Document</b>", "Technical Specification — reverse-engineered legacy workflow (as-is) and target architecture (to-be)"],
    ["<b>Subject workflow</b>", "RTT compliance (Operational › RTT Compliance) for ten NHS services of Provide Wellbeing, updated weekly"],
    ["<b>Primary evidence</b>", "sixth/MEDDAD~1.MP4 — 1920×1080, 16 fps, 8:42 (523 s); camera off; recorded 14/08/2026 (clock 11:00–11:06 on screen). "
     "The short 8.3 file name means the original title was lost when the file was copied"],
    ["<b>Secondary evidence</b>", "MEDDAD~1.srt (matches this video) and MEDDAD~1.txt (TurboScribe)"],
    ["<b>Timestamps</b>", "Video positions; every figure matched to a verified frame at 0.25 s steps (fractions shown rounded down)"],
    ["<b>Companion documents</b>", "RTT_PreBuild_Client_Requirements.pdf (same folder); specs 01–05"],
    ["<b>Report date</b>", "16 October 2026"],
    ["<b>Status</b>", "Draft for business-owner review. NHS numbers are blurred in every screenshot. <b>The operator changed a live formula during the "
     "recording</b>; see §4.3"],
]

EXEC_SUMMARY_INTRO = ("<b>What the recording shows.</b> The operator explains the RTT Data workbook: one subject (Provide Wellbeing), ten services, "
                      "a Power Query that loads the weekly RTT breach report (itself built from a SystmOne download), a patient-level RTT List and a "
                      "Manage Compliance tab whose ten rows are pasted into the data store each week.")

EXEC_SUMMARY = [
    "<b>Rule:</b> each patient on the list has an RTT week " + "<font name='DVM'>18-((Breach Date-TODAY())/7)</font>" + "; a service’s compliance is the share of its "
    "patients marked Compliant. RAG 10 if that share is above 92%, otherwise 2. Notes give the count of non-compliant patients.",
    "<b>Live edit to production logic (most important finding).</b> During the recording the operator deleted the <i>Breach Date 2</i> column "
    "(“we don’t need a breach date”), which held service-specific adjustments (ECC Autism in Schools +70 days, Norfolk and Waveney ASD +42 days), "
    "producing #REF! errors. The RTT Week formula was then rewritten, first with ROUNDUP and then with <b>ROUNDDOWN</b>. With ROUNDDOWN the first "
    "patient, two days past their breach date, changed from <b>Not Compliant to Compliant</b>.",
    "<b>Thresholds disagree with the RAG formula:</b> the dashboard bands are 1 / 0.98 / 0.96 / 0.94 / 0.92, but " +
    "<font name='DVM'>IF(N2&gt;0.92,10,2)</font>" + " marks exactly 92% as non-compliant, and the spoken rule is “less than 92 will be red”.",
    "<b>Unexplained data:</b> “What’s column 43? Can’t actually remember”; weighting is always 1 (“Only Matt knows”); Every x months is 0.25 (weekly).",
    "<b>Usual leftovers:</b> Missing always TRUE, Unique Lookup with a trailing dash, TODAY()-based dates, hand-edited Last Updated (still 07/08/2026), "
    "“UNABLE TO REFRESH – linked workbook” in the data store.",
]


def section0(c):
    para, H, table, bullets = c["para"], c["H"], c["table"], c["bullets"]
    s = [H("0. Evidence Base, Method &amp; Reading Guide", 0)]
    s += [H("0.1 Source artefacts", 1), table([
        ["Artefact", "What it is", "Used for"],
        ["sixth/MEDDAD~1.MP4", "Teams recording, 8:42, Git-LFS object 39 MB (8.3 short file name)", "Screenshots, step timings"],
        ["sixth/MEDDAD~1.srt / .txt", "Timed subtitles and transcript of the same meeting", "Timestamps and wording"],
    ], [52, 78, 50])]
    s += [H("0.2 Method and redaction", 1)] + bullets([
        "Frames matched to verified grid frames at 0.25 s steps; formula strips read across every formula-bar change.",
        "<b>Redaction:</b> the NHS Number column of the RTT List and of the Power Query preview is blurred in every screenshot. Breach dates and services "
        "are kept (no direct identifier). Staff names appear in data-store screenshots, as in earlier specs.",
    ])
    s.append(c["PageBreak"]())
    return s


def section1(c):
    para, H, table, figure, figref = c["para"], c["H"], c["table"], c["figure"], c["figref"]
    s = [H("1. Complete File, Workbook &amp; Sheet Inventory", 0)]
    s += [H("1.1 Files and systems", 1), table([
        ["#", "File / system", "Role", "Evidence"],
        ["S1", "<b>SystmOne</b>", "Source of the RTT waiting-list download", "Said 00:02:51–00:03:10"],
        ["F1", "<b>RTT breach report</b> (weekly; file name not shown)", "Built by the operational team each week from the SystmOne download; analysed for breach prevention; source of the RTT List query", "Said 00:02:26–00:03:19; " + figref("pq")],
        ["F2", "<b>RTT Data</b> (.xlsx, User input folder)", "Compliance tool: Manage Compliance, Requirements, Compliance Timeframes, RTT List (2)", figref("mc0")],
        ["F3", "<b>Compliance Data.xlsm</b> (Z:\\Performance Dashboards and Data\\Data Store)", "Data store", figref("exp") + ", " + figref("cdd") + ", " + figref("lu")],
    ], [8, 55, 85, 32])]
    s += [H("1.2 Tabs and query", 1), table([
        ["Object", "Role"],
        ["Manage Compliance", "Output: ten compliance rows (one per service) with Compliance % and NC Patients helper columns"],
        ["Requirements", "Provide Wellbeing × 10 services"],
        ["Compliance Timeframes", "Catalogue, 0.25 months, thresholds"],
        ["RTT List (2) / table RTT_List", "Patient-level list loaded by the query, plus calculated RTT Week and Compliance"],
        ["Query “RTT List”", "Single query; last step Table.SelectRows(#\"Filtered Rows\", each [NHS Number] &lt;&gt; 0); preview “may be up to 7 days old”"],
    ], [50, 130])]
    s += [H("1.3 Overview screenshots", 1), figure("rec", 70 * c["mm"]), figure("exp")]
    s.append(c["PageBreak"]())
    return s


def section2(c):
    para, H, table, figure, figref = c["para"], c["H"], c["table"], c["figure"], c["figref"]
    W = [9, 32, 22, 15, 102]
    hdr = ["Col", "Header", "Type", "Origin", "Lineage, rule and evidence"]
    s = [H("2. Exhaustive Column-Level Schema &amp; Data Lineage Catalogue", 0)]
    s += [H("2.1 Requirements and Compliance Timeframes", 1), table([hdr,
        ["A–B", "Name, Compliance Type", "Text", "MAN", "Provide Wellbeing × 10 services (" + figref("req") + ")"],
        ["C–E", "Required, Core, Notes", "", "MAN", "TRUE, Core, empty"],
        ["F", "Unique Lookup", "Text", "CALC", F('=CONCAT([@Name],"-",[@[Compliance Type]])')],
        ["G", "Active", "Boolean", "MAN", "TRUE typed; “we can switch off services here”"],
        ["TF B", "Every x months", "Decimal", "REF", "0.25 (weekly) (" + figref("ct") + ")"],
        ["TF D–E", "Compliance Group 1–2", "Text", "REF", "Operational › RTT Compliance"],
        ["TF H", "Unique Lookup", "Text", "CALC", "Group1-Group2-Group3 → “Operational-RTT Compliance-” (" + figref("ctH") + ")"],
        ["TF I", "Missing", "Boolean", "CALC", "Always TRUE (searches its own table) (" + figref("ctI") + ")"],
        ["TF J–N", "Threshold 1–5", "Decimal", "REF", "1, 0.98, 0.96, 0.94, 0.92 (" + figref("thr") + ")"],
    ], W), figure("req"), figure("ct"), figure("ctH"), figure("ctI"), figure("thr")]
    s += [H("2.2 RTT List (RTT_List table)", 1), table([hdr,
        ["A", "NHS Number", "Text", "PQ · <b>PID</b>", "Patient identifier (blurred); rows with 0 removed by the query"],
        ["B", "Breach Date", "Date", "PQ", "Date the 18-week limit is reached, from the breach report"],
        ["C", "Service", "Text", "PQ", "Matches Requirements compliance types"],
        ["D", "Column43", "Decimal", "PQ", "e.g. 26.857, 11.857: “can’t actually remember” (" + figref("col43") + ")"],
        ["E (before)", "Breach Date 2", "Date", "CALC", F('=IF([@Service]="ECC Autism in Schools",[@[Breach Date]]+70,IF([@Service]="Norfolk and Waveney - ASD Assessment Service",[@[Breach Date]]+42,[@[Breach Date]]))') + " — deleted live (" + figref("bd2") + ")"],
        ["F→E", "RTT Week", "Number", "CALC", "Before: " + F("=18-(([@[Breach Date 2]]-TODAY())/7)") + "; after: " + F("=ROUNDDOWN(18-(([@[Breach Date]]-TODAY())/7),0)") + " (" + figref("rw") + ", " + figref("rdn") + ")"],
        ["G→F", "Compliance", "Text", "CALC", "Compliant / Not Compliant from RTT Week; formula not shown [Inferred: Not Compliant when RTT Week &gt; 18]"],
    ], W), figure("pq"), figure("rtt0"), figure("col43"), figure("bd2"), figure("rw")]
    s += [H("2.3 Manage Compliance (output rows)", 1), table([hdr,
        ["A–B", "Name, Compliance Type", "Text", "MAN", "Provide Wellbeing; service"],
        ["C", "Completion Date", "Date", "CALC", F("=TODAY()") + " (" + figref("c4") + ")"],
        ["D", "Completion Status", "Text", "MAN", "Completed (“all the time”)"],
        ["E", "RAG Rating", "Number", "CALC", F("=IF(N2>0.92,10,2)") + " (" + figref("e2") + ")"],
        ["F", "Notes", "Text", "CALC", F('=IF(N2=1,"All Patients Currently Compliant",CONCAT(O2," Patient(s) Not Compliant"))') + " (" + figref("f2") + ")"],
        ["G", "Managed By", "Text", "MAN", "Provide Wellbeing"],
        ["H", "Due Date", "Date", "CALC", F("=C2+7") + " (" + figref("h2") + ")"],
        ["I–L", "Compliance Group 1–4", "Text", "MAN", "Operational, RTT Compliance"],
        ["M", "Weighting", "Number", "MAN", "1 (" + figref("m2") + ")"],
        ["N", "Compliance", "%", "CALC", F('=COUNTIFS(RTT_List[Service],B2,RTT_List[Compliance],"Compliant")/COUNTIF(RTT_List[Service],B2)') + " (" + figref("n2") + "); #DIV/0! if a service has no patients"],
        ["O", "NC Patients", "Integer", "CALC", F('=COUNTIFS(RTT_List[Service],B2,RTT_List[Compliance],"Not Compliant")') + " (" + figref("o2") + ")"],
    ], W), figure("mc0"), figure("n2"), figure("c4"), figure("e2"), figure("o2"), figure("f2"), figure("h2"), figure("m2")]
    s += [H("2.4 Compliance Data.xlsm", 1), figure("cdd"), figure("lu")]
    s.append(c["PageBreak"]())
    return s


STEPS = [
    (1, "00:00:00", "00:00:40", "Introduce RTT compliance", "“RTT compliance for the whole of Provide Wellbeing… no need for names, one entity.” Manage Compliance on screen.", "—", "—", ["rec", "mc0"]),
    (2, "00:00:40", "00:01:19", "Requirements", "Ten services, required, core, unique lookup, active.", "—", "—", ["req"]),
    (3, "00:01:19", "00:02:24", "Compliance Timeframes and thresholds", "0.25 months (“every week, four times a month”), Operational › RTT Compliance, lookups “copied from the previous sheet”, thresholds (green 100%, red below 92%).", "—", "—", ["ct", "ctH", "ctI", "thr"]),
    (4, "00:02:24", "00:03:24", "Source: RTT breach report via Power Query", "Explains the weekly breach report built from SystmOne; opens the query editor (RTT List).", "SystmOne → breach report → query → RTT_List", "Refresh not shown", ["rtt0", "pq"]),
    (5, "00:03:24", "00:04:07", "Columns of the RTT List", "NHS number, breach date, service, RTT week; “What’s column 43? Can’t actually remember.”", "—", "—", ["col43"]),
    (6, "00:04:07", "00:05:41", "<b>Live edit</b>: delete Breach Date 2 and rewrite RTT Week", "“The breach date is artificially calculated… we don’t need a breach date… we’ll delete that.” Column deleted → #REF!; formula retyped with ROUNDUP (19, Not Compliant), then ROUNDDOWN (18, Compliant). “Sorry about these running repairs.”", "Formula change in production workbook", "First patient: Not Compliant → Compliant; service adjustments for ECC Autism and Norfolk &amp; Waveney ASD removed", ["bd2", "rw", "ref", "rup", "rdn"]),
    (7, "00:05:41", "00:07:10", "Explain the Manage Compliance rows", "Completion date today, status Completed, RAG (&gt;92% → 10 else 2), notes from the NC count, due date +7, Operational › RTT Compliance, weighting 1 (“Only Matt knows”).", "RTT_List → Manage Compliance", "—", ["n2", "c4", "e2", "o2", "f2", "h2", "m2"]),
    (8, "00:07:10", "00:08:42", "Copy into the data store; last updated; save; refresh twice (described)", "Selects the rows, reopens Compliance Data (“accidentally closed”), shows the bottom row and Last Updated (Operational-RTT Compliance 07/08/2026). Paste and edit not performed.", "Manage Compliance → Compliance Data", "Not performed", ["exp", "cdd", "lu", "end"]),
]


def section3(c):
    para, H, table, figure = c["para"], c["H"], c["table"], c["figure"]
    s = [H("3. Chronological Step-by-Step Operator Workflow", 0),
         para("Eight steps cover the 8:42 recording. Step 6 changed the production workbook; the weekly paste and refresh are described only."),
         table([["Step", "Window", "Action"]] + [[str(x[0]), x[1] + "–" + x[2], x[3]] for x in STEPS], [10, 34, 136]), c["PageBreak"]()]
    for n, a, b, title, act, mp, mut, figs in STEPS:
        s += [H("Step %d [%s – %s]: %s" % (n, a, b, title.replace("<b>", "").replace("</b>", "")), 1),
              table([["<b>Action performed</b>", act], ["<b>Source → target</b>", mp], ["<b>State mutation</b>", mut]], [38, 142], head=False, zebra=False)]
        s += [figure(f) for f in figs]
        s.append(c["Spacer"](1, 6))
    s.append(c["PageBreak"]())
    return s


def section4(c):
    para, H, table, figref = c["para"], c["H"], c["table"], c["figref"]
    s = [H("4. Data Quality Checks, Manual Exceptions &amp; Edge Cases", 0)]
    s += [H("4.1 Business rules", 1), table([
        ["ID", "Rule", "Evidence"],
        ["BR-01", "RTT standard: patients should start treatment within 18 weeks of referral; RTT Week = 18 − weeks remaining to the breach date", figref("rw")],
        ["BR-02", "Some services have a different breach date (ECC Autism in Schools +70 days, Norfolk and Waveney ASD +42 days) — removed during the recording", figref("bd2")],
        ["BR-03", "Service compliance % = Compliant patients ÷ all patients on the list for the service", figref("n2")],
        ["BR-04", "RAG 10 if compliance % &gt; 92%, else 2", figref("e2")],
        ["BR-05", "Weekly cadence; due date = today + 7", figref("h2")],
    ], [12, 128, 40])]
    s += [H("4.2 Manual steps", 1), table([
        ["ID", "Manual step", "Risk"],
        ["EX-01", "Weekly SystmOne download and breach report built by the operational team", "Upstream errors flow straight in"],
        ["EX-02", "Rows copied to the bottom of Compliance Data each week", "Duplicates or missed weeks"],
        ["EX-03", "Last Updated edited by hand (still 07/08/2026 on 14/08)", "Stale timestamp"],
        ["EX-04", "Formulas edited ad hoc in the production file", "Unreviewed rule changes (see SV-01)"],
    ], [12, 90, 78])]
    s += [H("4.3 Spoken vs visual discrepancies and defects", 1), table([
        ["ID", "Said / intended", "Seen", "Impact"],
        ["SV-01", "“The breach date is artificially calculated… we don’t need it” (00:04:17–00:04:47)", "Breach Date 2 held service-specific +70 / +42 day rules; deleting it removed them", "ECC Autism and Norfolk &amp; Waveney ASD patients now measured against the wrong breach date"],
        ["SV-02", "“We’ll have it to round down, I think” (00:05:28)", "ROUNDDOWN turns 18.29 weeks into 18; the patient 2 days past breach becomes Compliant", "Breaches up to 6 days late are hidden; compliance overstated"],
        ["SV-03", "“If it’s less than 92 it will be red” (00:02:17)", "RAG =IF(N2&gt;0.92,10,2): exactly 92% is red", "Boundary disagrees"],
        ["SV-04", "Column 43 (“can’t actually remember”)", "Decimal weeks value carried from the report", "Unused or misunderstood data"],
        ["SV-05", "Weighting “always one… only Matt knows”", "Constant 1", "Meaning unknown"],
        ["FD-01", "Stable weekly result", "TODAY() in RTT Week and Completion Date", "Re-opening on another day changes results"],
        ["FD-02", "Compliance % per service", "Division by COUNTIF; a service with no patients gives #DIV/0!", "Error rows in the store"],
        ["FD-03", "Usual constants", "Missing TRUE, trailing-dash lookup, UNABLE TO REFRESH", "As in specs 01–05"],
    ], [12, 50, 62, 56])]
    s += [H("4.4 Hidden failure modes", 1), table([
        ["ID", "Failure mode", "Severity"],
        ["FM-01", "<b>Uncontrolled rule changes</b> in a live file, with no review or version history", "High"],
        ["FM-02", "<b>Lost service-specific breach rules</b>", "High"],
        ["FM-03", "<b>Rounding hides breaches</b>", "High"],
        ["FM-04", "<b>Patient identifiers</b> (NHS numbers) in a reporting workbook", "High (IG)"],
        ["FM-05", "<b>Dependency on a manually built weekly report</b>", "Medium"],
        ["FM-06", "<b>Non-reproducible weekly results</b> (TODAY())", "Medium"],
    ], [12, 148, 20])]
    s.append(c["PageBreak"]())
    return s


def section5(c):
    para, H, table, bullets, code = c["para"], c["H"], c["table"], c["bullets"], c["code"]
    s = [H("5. Target Modern System Architecture Blueprint", 0),
         para("RTT runs on the shared platform (spec 01 §5). Patient-level data stays in a restricted zone; only service-level counts are published.")]
    s += [H("5.1 Ingestion", 1)] + bullets([
        "Scheduled SystmOne waiting-list extract (or the breach report file) with a header contract; NHS number validated (checksum) and kept restricted.",
        "Each weekly load is a snapshot with an as-of date, so past weeks can be recomputed.",
    ])
    s += [H("5.2 Data model", 1), table([
        ["Table", "Key columns"],
        ["clin.rtt_pathway_snapshot", "as_of_date, pathway_id, nhs_number (restricted), service_id, clock_start or breach_date"],
        ["ref.rtt_service_rule (versioned)", "service_id, breach_offset_days (e.g. +70, +42), standard_weeks (18), valid_from/to, approved_by"],
        ["ref.rtt_threshold (versioned)", "rag rule (&gt; or ≥ 92%), dashboard bands"],
        ["mart.rtt_service_week", "as_of_date, service_id, patients, compliant, not_compliant, pct, rag"],
    ], [55, 125])]
    s += [H("5.3 Rules as SQL", 1), code(
        "SELECT s.as_of_date, s.service_id,\n"
        "       count(*) AS patients,\n"
        "       count(*) FILTER (WHERE s.as_of_date <= s.breach_date + r.breach_offset_days) AS compliant\n"
        "FROM clin.rtt_pathway_snapshot s\n"
        "JOIN ref.rtt_service_rule r ON r.service_id = s.service_id\n"
        " AND s.as_of_date BETWEEN r.valid_from AND coalesce(r.valid_to,'infinity')\n"
        "GROUP BY 1,2;\n"
        "-- breach compared on dates, so no rounding can hide a late patient")]
    s += bullets([
        "Rule changes (offsets, thresholds, rounding) are versioned reference data with an approver, never edits to a live formula (fixes FM-01, FM-02).",
        "Compliance is decided on dates, not rounded weeks (fixes FM-03); a service with no patients publishes “no patients” rather than #DIV/0!.",
        "Weekly publish writes ten rows with the as-of date inside the shared atomic publish; Last Updated is automatic.",
    ])
    s.append(c["PageBreak"]())
    return s


def section6(c):
    H, table = c["H"], c["table"]
    s = [H("6. Gap &amp; Ambiguity Register", 0), table([
        ["ID", "Timestamp", "Gap / ambiguity", "Ask"],
        ["G-01", "00:04:17–00:05:34", "Was the live change (Breach Date 2 removed, ROUNDDOWN) kept and saved?", "Confirm and, if needed, restore the previous version"],
        ["G-02", "00:03:57", "Why ECC Autism in Schools (+70) and Norfolk and Waveney ASD (+42) had adjusted breach dates; are these services still in scope?", "Clinical/operational lead to confirm"],
        ["G-03", "00:05:04–00:05:28", "Round up, round down or compare dates?", "Business owner to decide"],
        ["G-04", "00:03:43", "Meaning of Column43", "Explain or drop"],
        ["G-05", "00:02:26", "Name, location and build steps of the RTT breach report", "Share the file and process"],
        ["G-06", "00:06:07", "RAG boundary at exactly 92%", "Confirm"],
        ["G-07", "00:07:04", "Meaning of Weighting = 1", "Define"],
        ["G-08", "whole video", "Compliance column formula on RTT List (not shown)", "Share the workbook"],
        ["G-09", "file name", "Original title and date of the recording (MEDDAD~1)", "Confirm"],
    ], [11, 26, 91, 52])]
    s.append(c["PageBreak"]())
    return s


def section7(c):
    para, H, table, figref = c["para"], c["H"], c["table"], c["figref"]
    W = [13, 52, 115]
    s = [H("7. What Is Required to Build the Modern System", 0),
         para("RTT-specific requirements with reasons; shared platform items are in spec 01 §7. Client checklist: <b>RTT_PreBuild_Client_Requirements.pdf</b>.")]
    s += [H("7.1 Functional requirements", 1), table([
        ["ID", "Requirement (priority)", "Why it is required"],
        ["FR-R01", "Scheduled SystmOne RTT extract with weekly snapshots (M)", "Manual download and report build today (EX-01)."],
        ["FR-R02", "Versioned per-service breach rules (M)", "The +70/+42 rules were deleted live (" + figref("bd2") + ")."],
        ["FR-R03", "Date-based breach test, no rounding (M)", "ROUNDDOWN hid a breach (" + figref("rdn") + ")."],
        ["FR-R04", "Generated weekly compliance rows with counts (M)", "Replaces Manage Compliance (" + figref("mc0") + ")."],
        ["FR-R05", "Change control for rule changes (approval, history) (M)", "Live edits in the production file (FM-01)."],
        ["FR-R06", "Patient drill-down for operational teams, restricted (S)", "The breach report is also used to prevent breaches."],
    ], W)]
    s += [H("7.2 Non-functional and testing", 1), table([
        ["ID", "Requirement", "Why it is required"],
        ["NFR-R01", "NHS numbers restricted; dashboard sees service counts only", "Patient identifiers in the workbook (FM-04)."],
        ["NFR-R02", "Reproducible weekly snapshots", "TODAY() makes results day-dependent (FD-01)."],
        ["T-R01", "Golden case: patient with breach 12/08/2026 on 14/08/2026 must be Not Compliant", "The exact case the live edit flipped."],
        ["T-R02", "Service offsets: ECC Autism +70, Norfolk and Waveney ASD +42 (if confirmed)", "BR-02."],
        ["T-R03", "Boundary at 92% and empty services", "SV-03, FD-02."],
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
        ["00:00:03", "This is another video to show you how we update compliance data for RTT."],
        ["00:00:26", "As with incidents management, there’s no need for names… one entity, Provide Wellbeing."],
        ["00:01:36", "We update this every week, so it’s four times a month."],
        ["00:02:04", "I just copied that from the previous sheet."],
        ["00:02:15", "It will be green if it’s 100%. If it’s less than 92, it will be red."],
        ["00:02:26", "It pulls in data from another file, which is our RTT breach report… downloaded from SystmOne."],
        ["00:03:43", "What’s column 43? Can’t actually remember."],
        ["00:04:17", "The breach date, sorry, is artificially calculated."],
        ["00:04:42", "We don’t need a breach date… so we’ll delete that."],
        ["00:04:50", "Sorry about these running repairs."],
        ["00:05:04", "We probably want that to round up… or do we want it to round down? We’ll have it to round down, I think."],
        ["00:06:07", "If it’s less than 92% it’s going to give us a RAG rating of two, which is not compliant."],
        ["00:06:47", "Due date is the completion date plus seven days."],
        ["00:07:01", "Every weighting seems to be one… Only Matt knows."],
        ["00:07:54", "We’ll copy it and paste it into the bottom of our compliance data."],
        ["00:08:14", "We would save, refresh the tables twice."],
    ], [18, 162])]
    return s
