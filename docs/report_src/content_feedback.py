# -*- coding: utf-8 -*-
"""Specification content for the Survey Feedback recording (meeting 20260814_111322)."""
import html


def F(t):
    return '<font name="DVM" size="6.8">%s</font>' % html.escape(t)


DOC_TITLE = "Survey Feedback Compliance Workflow – Reverse-Engineering Specification"
HEADER = "Survey Feedback Compliance Workflow — Technical Specification (Reverse-Engineered)"
SOURCE = "Source: Teams recording 20260814_111322 (7:07)"
TITLE = "Survey Feedback Compliance Datastore Update"
SUBTITLE = ("Survicate 24-hour patient surveys → cleaned Excel exports → Power Query → SPC (statistical process control) "
            "sheets → six compliance rows in the data store, reverse-engineered from an operator screen recording")

TITLE_BLOCK = [
    ["<b>Document</b>", "Technical Specification — reverse-engineered legacy workflow (as-is) and target architecture (to-be)"],
    ["<b>Subject workflow</b>", "Patient survey feedback compliance (People › Feedback): Survicate exports → <i>24 hr All Surveys.xlsx</i> and "
     "<i>Survey Management.xlsm</i> → <i>Compliance Data.xlsm</i> → dashboard"],
    ["<b>Primary evidence</b>", "Meeting with Andrew R. Biggins-20260814_111322-Meeting Recording.mp4 — 1920×1080, 16 fps, 7:07 (428 s); camera off. "
     "Recorded first of the 14 August videos, before Training (11:33) and Complications (12:05)"],
    ["<b>Secondary evidence</b>", "…111322….srt (matches this video) and …111322….txt (TurboScribe)"],
    ["<b>Timestamps</b>", "Video positions; every figure matched to a verified frame at 0.25 s steps (fractions shown rounded down)"],
    ["<b>Companion documents</b>", "Feedback_PreBuild_Client_Requirements.pdf (same folder); specs 01–04"],
    ["<b>Report date</b>", "16 October 2026"],
    ["<b>Status</b>", "Draft for business-owner review. Free-text patient comments are blurred in every screenshot"],
]

EXEC_SUMMARY_INTRO = ("<b>What the recording shows.</b> The operator downloads four 24-hour patient surveys from Survicate, removes "
                      "“spoilt” responses by hand, saves the files to a shared folder, refreshes a first workbook (24 hr All Surveys) and then "
                      "a second one (Survey Management) that computes SPC charts and six compliance rows, which are pasted into the data store. "
                      "“This was designed by Matt, so we just follow his process.”")

EXEC_SUMMARY = [
    "<b>Two overlapping workbooks.</b> Both have Requirements and Compliance Timeframes, and both build the same 24 hr All Surveys table. "
    "The operator says “I’m not even sure we need to complete the first one”. Their compliance type names differ (“SPC Flagged - All” vs "
    "“Feedback - SPC Flagged - All”), and the data store holds both sets.",
    "<b>The rule is statistical, not a fixed target.</b> Monthly averages of satisfaction (1–5) and Friends &amp; Family (1–5) per service are "
    "tested with SPC rules (outside 3σ limits, 7 points above/below the mean, 7-point trends, 2 of 3 near a limit). A type is compliant when no "
    "rule fires for last month: “Satisfaction and F&amp;F within SPC criteria”.",
    "<b>Spoken thresholds differ from the logic:</b> “four and five is acceptable” is said, but the sheets work on monthly averages and SPC limits; "
    "for Friends and Family the operator says “less than five is not” acceptable.",
    "<b>Fragile ingestion:</b> exports have hash-like file names, need manual cleaning, and the Self Pay query showed a warning and the combined "
    "query an error during refresh (“it’s having trouble finding something”).",
    "<b>Hidden cross-tool link:</b> the Compliance tab reads " + "<font name='DVM'>[Incident Management.xlsm]Estates</font>" + " by full path, so this "
    "tool depends on another tool being present and current.",
    "<b>Usual leftovers:</b> Every x months 0.5, Missing TRUE, Issue 10, “UNABLE TO REFRESH – linked workbook”, TODAY()-based month selection.",
]


def section0(c):
    para, H, table, bullets = c["para"], c["H"], c["table"], c["bullets"]
    s = [H("0. Evidence Base, Method &amp; Reading Guide", 0)]
    s += [H("0.1 Source artefacts", 1), table([
        ["Artefact", "What it is", "Used for"],
        ["…20260814_111322-Meeting Recording.mp4", "Teams recording, 7:07, Git-LFS object 39 MB", "Screenshots, step timings"],
        ["…20260814 111322-Meeting Recording.srt / .txt", "Timed subtitles and transcript of the same meeting", "Timestamps and wording"],
    ], [52, 78, 50])]
    s += [H("0.2 Method and redaction", 1)] + bullets([
        "Frames matched to verified grid frames at 0.25 s steps; cropped to the Excel window, or full screen for browser and Explorer views.",
        "<b>Redaction:</b> the free-text feedback columns (raw export Q#4 onward; 24 hr All Surveys “Feedback”) and the formula bar when it shows a "
        "comment are blurred. Scores, dates and service codes are kept. Staff names appear in data-store screenshots, as in specs 01 and 04.",
    ])
    s.append(c["PageBreak"]())
    return s


def section1(c):
    para, H, table, figure, figref = c["para"], c["H"], c["table"], c["figure"], c["figref"]
    s = [H("1. Complete File, Workbook &amp; Sheet Inventory", 0)]
    s += [H("1.1 Files and systems", 1), table([
        ["#", "File / system", "Role", "Evidence"],
        ["S1", "<b>Survicate</b> (panel.survicate.com)", "Survey platform. Folders: NHS ASD, NHS CTS, NHS VAS &amp; POD, Self-Pay, Staff Feedback, Audits", figref("svl") + ", " + figref("srv")],
        ["F1", "Four exports (50f982bbbd00319b, 8f3115757b582202, a16d7414468e60c1, 92797e16bc759d36 .xlsx)", "Raw survey responses, one per survey, cleaned by hand", figref("exp") + ", " + figref("raw")],
        ["F2", "<b>24 hr All Surveys</b> (.xlsx) in Z:\\…\\Data Store\\Surveys", "First tool: Power Query combine + Requirements + Timeframes + SPC sheets", figref("all")],
        ["F3", "<b>Survey Management.xlsm</b> in Z:\\…\\User input", "Second tool: same data plus the Compliance output tab", figref("ui") + ", " + figref("cmp")],
        ["F4", "Incident Management.xlsm (Estates tab)", "Read by a Survey Management formula", figref("cmR")],
        ["F5", "<b>Compliance Data.xlsm</b>", "Data store", figref("cdR") + "–" + figref("lu")],
    ], [8, 55, 85, 32])]
    s += [H("1.2 Tabs", 1), table([
        ["Workbook", "Tabs (in order)"],
        ["24 hr All Surveys", "Sheet10 · 24 hr All Surveys · Requirements · Compliance Timeframes · SPC - ND - F&amp;F · SPC - CTS - F&amp;F · …"],
        ["Survey Management", "Compliance · 24 hr All Surveys · Requirements · Compliance Timeframes · SPC - ND/CTS/VAS/Self Pay/NHS/All - F&amp;F · "
                              "SPC - ND/CTS/VAS/Self Pay/NHS/All - CSAT · Self Pay Types"],
        ["Power Query (both)", "24 hr Self Pay Survey · 24 hr ND Survey · 24 hr VAS Survey · 24 hr CTS Survey · Self_Pay_Types · 24 hr All Surveys = Table.Combine(…)"],
    ], [40, 140])]
    s += [H("1.3 Overview screenshots", 1), figure("rec", 70 * c["mm"]), figure("svl"), figure("srv"), figure("exp"), figure("ui")]
    s.append(c["PageBreak"]())
    return s


def section2(c):
    para, H, table, figure, figref = c["para"], c["H"], c["table"], c["figure"], c["figref"]
    W = [9, 34, 22, 15, 100]
    hdr = ["Col", "Header", "Type", "Origin", "Lineage, rule and evidence"]
    s = [H("2. Exhaustive Column-Level Schema &amp; Data Lineage Catalogue", 0)]
    s += [H("2.1 Raw Survicate export (“Survey report”)", 1), table([hdr,
        ["A", "Date &amp; Time", "Text datetime", "RAW", "e.g. 2022-08-03 1… (ISO text)"],
        ["B–C", "Response ID, Respondent", "Text", "RAW", "Survicate identifiers"],
        ["D–E", "Device, Platform", "Text", "RAW", "Desktop/Mobile; Win32, iPhone, Linux…"],
        ["F", "Page", "URL", "RAW", "survey link; service name embedded (Ear Care, ASD and ADHD, No Scalpel Vasectomy…)"],
        ["G", "Q#1: What Provide Wellbeing service did you use?", "Text", "RAW", "Self Pay survey only; mapped through Self Pay Types"],
        ["H", "Q#2: How … satisfied (1–5)", "Number", "RAW", "Overall satisfaction"],
        ["I", "Q#3: How likely to recommend (1–5)", "Number", "RAW", "Friends and Family"],
        ["J", "Q#4: free text", "Text", "RAW · <b>sensitive</b>", "Patient comment (blurred)"],
        ["K–N", "Q#5/Q#6 Action, “you for cor…”, “amp;”", "Text", "RAW", "Action fields; a stray HTML-entity column “amp;” survives into the combined table"],
    ], W), para("Row 2 is empty and “some of them clearly don’t… they click on the survey which registers a response but don’t fill it in”; these are removed by hand (00:01:18–00:01:49)."),
          figure("raw")]
    s += [H("2.2 24 hr All Surveys (combined table, both tools)", 1), table([hdr,
        ["A", "Date &amp; Time (UTC)", "Datetime", "PQ", "Parsed from export"],
        ["B", "Overall Satisfaction", "1–5", "PQ", "From Q#2"],
        ["C", "Feedback", "Text", "PQ · <b>sensitive</b>", "Comment (blurred)"],
        ["D", "Friends and Family", "1–5", "PQ", "From Q#3"],
        ["E", "amp;", "Text", "PQ", "Artefact column"],
        ["F", "Service Level 2", "Code", "PQ", "CTS, VAS, ND, or the Self Pay Types code"],
        ["G", "Service Level 1", "Text", "PQ", "NHS / Self Pay"],
    ], W), figure("all"), figure("pq1"), figure("pq2")]
    s += [H("2.3 Requirements and Compliance Timeframes", 1),
          para("Both tools carry six compliance types for the single subject Provide Wellbeing: All, NHS, Self Pay, VAS, CTS, ND; Required TRUE, Core, "
               "Active TRUE. Timeframes: Every x months 0.5, People › Feedback, Unique Lookup " + F('=CONCAT(Group 1,"-",Group 2,"-",Group 3)') +
               " → “People-Feedback-” (trailing dash), Missing TRUE. Type names differ between the tools (“SPC Flagged - All” vs “Feedback - SPC Flagged - All”)."),
          figure("req"), figure("ct"), figure("smct")]
    s += [H("2.4 SPC sheets (F&amp;F and CSAT, per service)", 1), table([
        ["Column(s)", "Content", "Rule"],
        ["B", "Month (1st of month)", "From 01/09/2024 (first tool) / earlier (second tool) to last month"],
        ["C", "Monthly average score", "Average of Friends and Family (F&amp;F sheets) or Overall Satisfaction (CSAT sheets) for the service"],
        ["F, G, H", "Mean, LCL, UCL (repeated per row)", "AC3 mean, AC4 standard deviation, " + F("AC5 LCL =AC3-(AC4*3)") + ", AC6 UCL = mean + 3σ"],
        ["I, J", "Moving range, cumulative moving average", "For the σ estimate [Inferred]"],
        ["K–Z", "Count &gt; 3, Count &lt; 3, Under/Over Mean, 7 points &lt;/&gt; mean, Under LCL, Over UCL, Trend Up/Down, 7-point trends, 2 out of 3 low/high", "Each 1 when the rule fires; e.g. " + F("N19 =IF(AND(N18=1,M19=1),IF(SUM(M19:M25)>=7,1,0),0)")],
    ], [24, 70, 86]), figure("st1"), figure("spc"), figure("spch"), figure("csat"), figure("spt")]
    s += [H("2.5 Survey Management › Compliance (output rows)", 1), table([hdr,
        ["A", "Name", "Text", "MAN", "Provide Wellbeing"],
        ["B", "Compliance Type", "Text", "MAN", "Feedback - SPC Flagged - All / NHS / Self Pay / VAS / CTS / ND"],
        ["C", "Completion Date", "Date", "MAN/CALC", "14/08/2026 (update day)"],
        ["D", "Completion Status", "Text", "MAN", "Completed"],
        ["E", "RAG Rating", "Number", "MAN", "10"],
        ["F", "Notes", "Text", "CALC", "Lists flagged measures with month, else “Satisfaction and F&amp;F within SPC criteria”. " + figref("cmF")],
        ["G–H", "Managed By, Due Date", "Text, Date", "MAN", "Provide Wellbeing; 24/08/2026"],
        ["I–M", "Compliance Group 1–4, Weighting", "Text", "MAN", "People › Feedback; 1"],
        ["N–O", "SPC Count CSAT, SPC Count F&amp;F", "Integer", "CALC", "Rule hits for last month"],
        ["P–Q", "Avg CSAT, Avg F&amp;F", "Number", "CALC", F("=XLOOKUP(EDATE(DATE(YEAR(TODAY()),MONTH(TODAY()),1),-1),'SPC - Self Pay - CSAT'!B:B,…C:C,\"\")") + ". " + figref("cmP")],
        ["R…", "(cross-tool)", "Number", "CALC", "Reads Incident Management.xlsm Estates by full path. " + figref("cmR")],
    ], W), figure("cmp"), figure("cmF"), figure("cmP"), figure("cmR")]
    s += [H("2.6 Compliance Data.xlsm", 1), figure("cdR"), figure("cdD"), figure("lu")]
    s.append(c["PageBreak"]())
    return s


STEPS = [
    (1, "00:00:00", "00:00:23", "Introduce survey feedback compliance", "Camera off; starts screen share.", "—", "—", ["rec"]),
    (2, "00:00:23", "00:01:11", "Open Survicate and explain the four surveys", "From the intranet bookmark opens Survicate; four 24-hour surveys; satisfaction and F&amp;F out of five; “four and five is acceptable”.", "—", "—", ["svl", "srv"]),
    (3, "00:01:11", "00:01:57", "Download and clean the exports (described)", "Shows last month’s exports in Data Store\\Surveys and one raw file; spoilt responses removed by hand.", "Survicate → .xlsx exports → manual clean → Surveys folder", "Not performed live", ["exp", "raw"]),
    (4, "00:01:57", "00:03:50", "Open the first tool and refresh", "Opens a workbook (Survey Management shown first, then 24 hr All Surveys); Data › Refresh All runs a background query; Power Query editor shows the Self Pay query warning and the combined query error.", "Exports → 24 hr All Surveys (Power Query)", "Table refreshed; one query failing", ["cmp", "all", "st1", "pq1", "pq2"]),
    (5, "00:03:50", "00:04:25", "Requirements and Compliance Timeframes (first tool)", "“We have our usual requirements and compliance timeframes. This is a bit confusing.”", "—", "—", ["req", "ct"]),
    (6, "00:04:25", "00:05:08", "Second tool: Survey Management", "Opens Survey Management.xlsm from User input: “also has requirements and compliance timeframes… I’m not even sure we need to complete the first one.”", "Exports → Survey Management (Power Query)", "—", ["ui", "smct"]),
    (7, "00:05:08", "00:06:03", "SPC tables for F&amp;F and CSAT", "Flicks through SPC sheets per service: “pulling a date down, pulling the formulas down”.", "24 hr All Surveys → SPC sheets", "New month row added by hand (described)", ["spc", "spch", "csat", "spt"]),
    (8, "00:06:03", "00:06:20", "Compliance table", "“It builds up a compliance table here based on the statistical data.” Selects F6, P5, R8.", "SPC sheets → Compliance", "—", ["cmF", "cmP", "cmR"]),
    (9, "00:06:20", "00:07:07", "Paste into the data store, last updated, save, refresh twice (described)", "Opens Compliance Data (UNABLE TO REFRESH), bottom of Compliance Data, Last Updated (People-Feedback 28/07/2026). “Bob’s your uncle.”", "Compliance → Compliance Data (paste); Last Updated", "Not performed", ["cdR", "cdD", "lu", "end"]),
]


def section3(c):
    para, H, table, figure = c["para"], c["H"], c["table"], c["figure"]
    s = [H("3. Chronological Step-by-Step Operator Workflow", 0),
         para("Nine steps cover the 7:07 recording. The download, cleaning, month roll-forward and paste are described, not performed."),
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
    s = [H("4. Data Quality Checks, Manual Exceptions &amp; Edge Cases", 0)]
    s += [H("4.1 Business rules", 1), table([
        ["ID", "Rule", "Evidence"],
        ["BR-01", "Responses without answers (“spoilt”) are excluded", "Said 00:01:38"],
        ["BR-02", "Scores are aggregated to monthly averages per service (ND, CTS, VAS, Self Pay, NHS, All)", figref("spc")],
        ["BR-03", "A month is flagged when any SPC rule fires (3σ limits, 7-point runs and trends, 2 of 3 near a limit)", figref("spch")],
        ["BR-04", "Compliant = no flag last month for both CSAT and F&amp;F", figref("cmF")],
        ["BR-05", "Self Pay responses are classified by service via Self Pay Types", figref("spt")],
    ], [12, 128, 40])]
    s += [H("4.2 Spoken vs visual discrepancies and defects", 1), table([
        ["ID", "Said / intended", "Seen", "Impact"],
        ["SV-01", "“Four and five is acceptable, lower than four is not”", "Sheets use monthly averages and SPC limits, not a per-response threshold", "Acceptance rule unclear"],
        ["SV-02", "F&amp;F: “less than five is not” acceptable", "Same SPC logic as CSAT", "Possibly mis-spoken; must be confirmed"],
        ["SV-03", "Two tools both needed?", "Both build the same table; type names differ; both sets in the data store", "Duplicate requirements in the store"],
        ["SV-04", "Refresh pulls the surveys", "Self Pay query warning; combined query error during refresh", "Silent partial data"],
        ["FD-01", "Last month", "EDATE(…TODAY()…,-1)", "Results depend on the day the file is opened"],
        ["FD-02", "Independent tool", "Formula reads Incident Management.xlsm by path", "Breaks if that file moves or is open/locked"],
        ["FD-03", "Clean column set", "Stray “amp;” column from the export", "Header drift in source files"],
        ["FD-04", "Usual constants", "0.5 months, Missing TRUE, Issue 10, Unique Lookup with trailing dash", "As in specs 01–04"],
    ], [12, 50, 62, 56])]
    s += [H("4.3 Hidden failure modes", 1), table([
        ["ID", "Failure mode", "Severity"],
        ["FM-01", "<b>Manual export and cleaning</b>: wrong date range or deleted valid responses", "High"],
        ["FM-02", "<b>Hash-named files</b>: easy to save the wrong export over another", "Medium"],
        ["FM-03", "<b>Power Query errors</b> after Survicate column changes", "High"],
        ["FM-04", "<b>Duplicate tools and type names</b>", "Medium"],
        ["FM-05", "<b>Hand-extended SPC ranges</b> (“pulling formulas down”)", "Medium"],
        ["FM-06", "<b>Cross-workbook dependency</b> on Incident Management", "Medium"],
        ["FM-07", "<b>Patient comments in shared spreadsheets</b>", "High (IG)"],
    ], [12, 148, 20])]
    s.append(c["PageBreak"]())
    return s


def section5(c):
    para, H, table, bullets, code = c["para"], c["H"], c["table"], c["bullets"], c["code"]
    s = [H("5. Target Modern System Architecture Blueprint", 0),
         para("Feedback runs on the shared platform (spec 01 §5) with a survey connector and an SPC rules engine.")]
    s += [H("5.1 Ingestion", 1)] + bullets([
        "<b>Survicate API</b> (or scheduled export) per survey; responses stored once by Response ID (idempotent).",
        "<b>Spoilt-response rule</b> as code (e.g. no score answered), with counts shown for review instead of manual deletion.",
        "Comments stored in a restricted table, or not at all if the dashboard does not need them.",
    ])
    s += [H("5.2 Data model", 1), table([
        ["Table", "Key columns"],
        ["survey", "survey_id, name, service_group (NHS / Self Pay), survicate_id"],
        ["survey_response", "response_id (PK), survey_id, responded_at, csat, ff, service_code, comment (restricted), is_spoilt"],
        ["ref.self_pay_service_map", "description → service_code (versioned)"],
        ["ref.spc_rule (versioned)", "rule_code, parameters (σ multiple, run length, window), applies_to"],
        ["mart.feedback_monthly", "month, service_code, measure (CSAT/FF), n, mean"],
        ["mart.feedback_spc_signal", "month, service_code, measure, rule_code, fired"],
    ], [50, 130])]
    s += [H("5.3 SPC as SQL", 1), code(
        "WITH m AS (SELECT service_code, measure, month, avg(score) AS mean_score\n"
        "           FROM mart.feedback_long GROUP BY 1,2,3),\n"
        "lim AS (SELECT service_code, measure, avg(mean_score) AS cl, stddev_samp(mean_score) AS sd\n"
        "        FROM m WHERE month < :as_of_month GROUP BY 1,2)\n"
        "SELECT m.*, (m.mean_score < l.cl - 3*l.sd) AS under_lcl,\n"
        "       (m.mean_score > l.cl + 3*l.sd) AS over_ucl,\n"
        "       bool_and(m.mean_score < l.cl) OVER w7 AS seven_below_mean\n"
        "FROM m JOIN lim l USING (service_code, measure)\n"
        "WINDOW w7 AS (PARTITION BY m.service_code, m.measure ORDER BY m.month ROWS 6 PRECEDING);")]
    s += bullets([
        "Baseline period, σ method and rule list are versioned parameters approved by the business.",
        "The compliance row per service is generated for the as-of month; Notes list fired rules, exactly like the current F6 text.",
        "One tool, one set of type names (resolves SV-03); no cross-workbook links (FD-02).",
    ])
    s.append(c["PageBreak"]())
    return s


def section6(c):
    H, table = c["H"], c["table"]
    s = [H("6. Gap &amp; Ambiguity Register", 0), table([
        ["ID", "Timestamp", "Gap / ambiguity", "Ask"],
        ["G-01", "00:04:45", "Is the first tool (24 hr All Surveys) still needed?", "Decide; retire one"],
        ["G-02", "00:01:18", "Exact rule for a “spoilt” response", "Define"],
        ["G-03", "00:00:59–00:01:09", "Acceptance threshold per response vs SPC on averages; F&amp;F “less than five”", "Confirm the rule"],
        ["G-04", "00:05:19", "SPC baseline period, σ method, which rules count", "Share Matt’s design or approve defaults"],
        ["G-05", "00:06:17", "Why Compliance reads Incident Management Estates", "Explain or remove"],
        ["G-06", "00:03:19", "Cause of the Power Query warning/error", "Share M code"],
        ["G-07", "00:00:47", "Which Survicate surveys count (NHS VAS &amp; POD includes podiatry?)", "Confirm scope"],
        ["G-08", "whole video", "Whether the dashboard shows comments or only compliance", "Share measures"],
    ], [11, 26, 91, 52])]
    s.append(c["PageBreak"]())
    return s


def section7(c):
    para, H, table, figref = c["para"], c["H"], c["table"], c["figref"]
    W = [13, 52, 115]
    s = [H("7. What Is Required to Build the Modern System", 0),
         para("Feedback-specific requirements with reasons; shared platform items are in spec 01 §7. Client checklist: "
              "<b>Feedback_PreBuild_Client_Requirements.pdf</b>.")]
    s += [H("7.1 Functional requirements", 1), table([
        ["ID", "Requirement (priority)", "Why it is required"],
        ["FR-F01", "Survicate connector with idempotent response load (M)", "Manual export and hash-named files (FM-01, FM-02, " + figref("exp") + ")."],
        ["FR-F02", "Coded spoilt-response rule with review counts (M)", "Manual deletion today (BR-01)."],
        ["FR-F03", "Versioned self-pay service map (M)", figref("spt") + "."],
        ["FR-F04", "SPC engine with versioned parameters (M)", "Replaces hand-extended SPC sheets (FM-05, " + figref("spch") + ")."],
        ["FR-F05", "Generated compliance rows with rule-hit notes (M)", "Replaces the Compliance tab (" + figref("cmF") + ")."],
        ["FR-F06", "Single tool and naming (M)", "Two overlapping tools (SV-03)."],
        ["FR-F07", "SPC charts for review (S)", "The SPC sheets are the operator’s evidence."],
    ], W)]
    s += [H("7.2 Non-functional and testing", 1), table([
        ["ID", "Requirement", "Why it is required"],
        ["NFR-F01", "Comments restricted or not stored", "Patient free text (FM-07)."],
        ["NFR-F02", "Schema-drift alerts on survey exports", "Query errors after column changes (FM-03, " + figref("pq2") + ")."],
        ["T-F01", "Recompute one month and match the Compliance tab rows (all six “within SPC criteria” on 14/08/2026)", "Parity."],
        ["T-F02", "Rule unit tests for each SPC rule", "Core logic."],
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
        ["00:00:05", "This video is how we update our survey feedback compliance."],
        ["00:00:23", "The first thing we do is download our surveys from the survey platform."],
        ["00:00:47", "There are four surveys… 24-hour surveys."],
        ["00:00:59", "Four and five is acceptable, lower than four is not."],
        ["00:01:06", "Four and five is acceptable, less than five is not."],
        ["00:01:18", "We usually do a bit of a cleanup of the data."],
        ["00:01:46", "We get rid of any spoilt ones."],
        ["00:02:16", "This was designed by Matt, so we just follow his process."],
        ["00:03:19", "It’s having trouble finding something with that one."],
        ["00:04:09", "This is a bit confusing."],
        ["00:04:52", "I’m not even sure we need to complete the first one."],
        ["00:05:47", "It’s a case of pulling a date down, pulling the formulas down."],
        ["00:06:26", "We copy that into the compliance data, into the bottom here."],
        ["00:06:50", "We save it, refresh it twice."],
    ], [18, 162])]
    return s
