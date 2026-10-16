# -*- coding: utf-8 -*-
"""00_Overview appendix: the logic inside Compliance Data.xlsm, taken from the client's own source template.

Source: sources/Wellbeing Dashboard current data template.xlsx (tabs 01-04; Compliance rows 187-274 of tab 04).
Section numbers here are cited as "DSL §n" by the pre-build checklists (prereq_datastore.py).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reportlab.platypus import Paragraph, Spacer, PageBreak
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import ParagraphStyle
import build as B

mm = B.mm
para, H, table, bullets, code = B.para, B.H, B.table, B.bullets, B.code
T4 = "tab 04 row "


def build(out):
    doc = B.Doc(out, title="Compliance Data Store Logic – Appendix",
                header="Compliance Data.xlsm — Data Store Logic (from the client source template)")
    doc.SOURCE = "Source: Wellbeing Dashboard current data template.xlsx"
    s = [Spacer(1, 22 * mm), para("APPENDIX TO THE SYSTEM OVERVIEW", "small"), Spacer(1, 3 * mm),
         Paragraph("Compliance Data Store Logic", B.ss["title"]),
         Paragraph("Every table, Power Query step and formula column of Compliance Data.xlsm as documented by the client, "
                   "what each one does, where it breaks, and what it means for the build", B.ss["sub"]),
         table([["<b>Source</b>", "sources/Wellbeing Dashboard current data template.xlsx, filled in by the client. "
                                  "Tabs 01 Data Sources, 02 Data Size, 03 Checks You Do, 04 Changes You Make (Compliance rows 187–274, all nine columns read)"],
                ["<b>Covers</b>", "Z:\\Performance Dashboards and Data\\Data Store\\Compliance Data.xlsm and the 11 user-input tools that feed it"],
                ["<b>Related</b>", "Compliance_Dashboard_System_Overview.pdf (same folder) and the specification and pre-build PDFs in folders 01–07. "
                                   "Items added to the pre-build checklists cite this document as “DSL §n”"],
                ["<b>Report date</b>", "16 October 2026"],
                ["<b>VBA status</b>", "The template contains <b>no compliance VBA</b>. Its only macro (" + T4 + "49) belongs to the Self-Pay Customers tool; see §7"]],
               [32, 148], head=False, zebra=False),
         Spacer(1, 8 * mm),
         para("<b>Why this matters.</b> The recordings show people using the tools, but the data store itself was only glimpsed. "
              "This template is the client’s own written record of it, so it settles several rules the specs had to infer: what "
              "“Issue = 10” means, how Training is judged, what Thresholds 1–5 do and why the store needs “refresh twice”. "
              "The client also marks 17 of the 88 rows as “Unclear” or “Unknown”; those become keep-or-retire decisions."),
         PageBreak()]
    toc = TableOfContents()
    toc.levelStyles = [ParagraphStyle("t0", fontName="DVB", fontSize=9.5, leading=14, textColor=B.INK),
                       ParagraphStyle("t1", fontName="DV", fontSize=8.4, leading=11.5, leftIndent=12, textColor=B.INK)]
    s += [Paragraph("Contents", B.ss["h1"]), toc, PageBreak()]

    # 1 ------------------------------------------------------------------
    s += [H("1. What the Template Says About Compliance", 0), table([
        ["Tab", "Compliance content", "What it tells us"],
        ["01 Data Sources", "Compliance Data (PW &amp; MP): governance platforms (e.g. Datix) plus data requested from contractors, site managers and "
                            "departments (e.g. Estates); exports, reports and email; mostly monthly, some weekly; owner DPT, tasks rotate",
         "Several people run the same steps in turn, so the rules must live in the system, not in one person’s head"],
        ["01 Data Sources", "User Input Tools: 11 inherited tools in Z:\\Performance Dashboards and Data\\User input, each updated monthly. "
                            "Two tables per tool: Names → Compliance Timeframes → data store. Power Query updates the tools; "
                            "“information is copied into the Compliance Data data store via VBA. No transformation as such is performed”. "
                            "Knowledge of them is “anecdotal”",
         "Confirms the shared pattern in the Overview §3. The VBA claim conflicts with the recordings (mostly manual paste), see DS-12"],
        ["02 Data Size", "3,874 records; 5–20 new per week; kept 7 years; data back to 2019 with only a few early entries",
         "A small data set: one relational database is enough. 7-year retention becomes a requirement"],
        ["03 Checks You Do", "No automated checks. Errors are spotted by “perusing existing data via these tools”",
         "Every validation in the specs is new; nothing existing to preserve"],
        ["04 Changes You Make", "88 rows: Snapshot, Compliance Data, Last Updated, Requirements_Detailed, compliance_Timeframes_Table, "
                                "requirements_Final_Self_Ref, Requirements (§2–§6)",
         "The full calculation chain from raw records to the dashboard’s three reference tables"],
    ], [24, 92, 64]), PageBreak()]

    # 2 ------------------------------------------------------------------
    s += [H("2. Data Flow Inside Compliance Data.xlsm", 0),
          para("The client: the file “is its own data store. Data is written to it both manually and via semi-automated input tools… then transformed "
               "within the file and then transformed further by multiple Power Queries… to produce three reference tables which then drive the "
               "PW and MP Dashboards (format: Power BI Report)” (" + T4 + "187)."),
          table([
              ["Step", "Object", "Built by", "Feeds"],
              ["1", "<b>Compliance Data</b> table (compliance_Data_Store_Table): one row per completion record", "Rows pasted or written by each tool", "Requirements tables (Due Date, Status, Notes)"],
              ["2", "<b>compliance_Timeframes_Table</b>: one row per compliance type", "Power Query: Table.Combine of 12 tool timeframe tables", "Requirements tables; Core Requirement"],
              ["3", "<b>Requirements_Detailed</b>: one row per person/site × type", "Power Query (11 requirement tables + timeframes join) + formula columns", "Power BI"],
              ["4", "<b>Requirements</b>: same as 3 with Group 1/2 instead of 3/4", "Power Query (12 requirement tables) + formula columns", "Power BI; step 5"],
              ["5", "<b>requirements_Final_Self_Ref</b>: sub-group and group roll-ups", "Power Query reading this same file from Z:\\, + formula columns", "Power BI"],
              ["6", "<b>Last Updated</b>: one row per Group L1–L2", "Typed by hand or written by tool VBA", "Last Reviewed Date"],
              ["–", "<b>Snapshot</b>: weekly records by service, from September 2023", "Unknown", "Unknown (client: purpose unclear)"],
          ], [10, 70, 56, 44]),
          H("2.1 The twelve compliance areas", 1),
          para("The Power Query combine lists name the areas. Folder numbers show which ones have been recorded."),
          table([
              ["Area (table prefix)", "Timeframes", "Requirements", "Requirements_Detailed", "Recorded in"],
              ["estates", "✓", "✓", "✓", "—"], ["staff", "✓", "✓", "✓", "01"], ["organisation", "✓", "✓", "✓", "—"],
              ["audit_Programme", "✓", "✓", "✓", "—"], ["regular_Audit", "✓", "✓", "✓", "—"], ["policy", "✓", "✓", "✓", "—"],
              ["medical_Devices", "✓", "✓", "✓", "—"], ["incidents", "✓", "✓", "✓", "02, 07"],
              ["Sickness_and_Annual_Leave", "✓", "✓", "✓", "—"], ["Survey", "✓", "✓", "✓", "05"], ["training", "✓", "✓", "✓", "04"],
              ["complications", "✓", "✓", "<b>✗ missing</b>", "03"],
          ], [52, 26, 26, 40, 36]), Spacer(1, 4),
          para("RTT (folder 06) does not appear by name. Its rows must sit inside one of these areas (likely organisation or audit); see DS-11."),
          PageBreak()]

    # 3 ------------------------------------------------------------------
    s += [H("3. Compliance Data Table (the record store)", 0),
          para("Rows 191–200. Every column is a formula on top of the pasted record columns (Name, Compliance Type, Completion Date, Completion Status, "
               "Due Date, Issue, Compliance Group Level 1/2, Compliance Notes)."),
          table([
              ["Column", "Rule (plain words)", "Client’s reason", "Our note"],
              ["Most Recent Record", "TRUE when this row has the latest Completion Date for its Unique Lookup and Compliance Type; also TRUE when no row of that pair has a date",
               "Keep the full history while the tools read only the latest record", "With no dates every row is “most recent” (DS-01)"],
              ["<b>Compliant</b>", "Most recent rows only. By Compliance Group – Level 2:<br/>• Incidents, Feedback, HR Metrics, Complications: Issue = 10 → Compliant<br/>"
                                   "• Training: Completion Status not blank → Compliant<br/>• all others: Due Date after today, <b>or blank</b> → Compliant",
               "Required for reporting", "Explains Issue = 10. A blank due date counts as compliant (DS-02); Training ignores expiry (DS-03)"],
              ["Expires within 3 months", "Most recent rows with a due date: before EDATE(TODAY(),3) → “Expires within 3 months”; for <b>Ongoing Audit</b> before WORKDAY(TODAY(),10) → “Expires within 2-weeks”",
               "Required for reporting", "No lower bound, so already-expired items are labelled “expires” too (DS-04)"],
              ["Weeks Non Compliant", "ROUND((TODAY() − Due Date)/7, 0) when Non Compliant", "Required for reporting",
               "Blank due date gives ≈ 6,600 weeks; Issue-based failures with a future due date give negative weeks (DS-05)"],
              ["Core Requirement", "Looks up the type in compliance_Timeframes_Table → “Core” or blank", "Required for reporting", "Core flag is per type, not per person"],
              ["Unique Lookup", "Name-Compliance Type", "Assumed used later", "Name text as key (Overview §5)"],
              ["Unique Lookup 2", "Name-Type-Completion Status-Completion Date (most recent rows only)", "Assumed used later", "No consumer documented"],
              ["Unique Lookup 3", "Unique Lookup (most recent rows only)", "Assumed used later", "Seen in spec 01 lookups"],
              ["Unique Lookup 4", "Name-Type (most recent rows only)", "Assumed used later", "<b>The join key</b> used by every Requirements lookup"],
              ["Notes", "Looks up Unique Lookup 4 in requirements_Table[Notes]", "Required for reporting", "Notes live on the requirement, not the record"],
          ], [27, 66, 35, 52]),
          H("3.1 Snapshot and Last Updated", 1),
          table([
              ["Table", "Columns", "Client’s note"],
              ["Snapshot", "Most recent location record (MAXIFS on Date Week Commencing by Service-Completion Status); Most recent service record (by Service Group-Completion Status); the two Unique Lookups",
               "Data dates back to September 2023 (V1 of the tool). “It is unclear what function this data performs now”"],
              ["Last Updated", "Unique Lookup = Compliance Group Level 1-Level 2; one Updated date per group",
               "Written “manually or semi-automatically by each user input tool. Lookup may relate to the VBA contained in these tools”"],
          ], [24, 86, 70]), PageBreak()]

    # 4 ------------------------------------------------------------------
    s += [H("4. Requirements Tables (Power Query and formula columns)", 0),
          H("4.1 Requirements_Detailed query (rows 202–209)", 1),
          code("Source            = Table.Combine({estates_, staff_, organisation_, audit_Programme_, regular_Audit_, policy_,\n"
               "                      medical_Devices_, incidents_, Sickness_and_Annual_Leave_, Survey_, training_ ...requirements_Table})\n"
               "Merged Queries    = Table.NestedJoin(Source, {\"Compliance Type\"}, compliance_Timeframes_Table, ..., JoinKind.LeftOuter)\n"
               "Expanded          = Compliance Group 3, Compliance Group 4, Threshold 1..5\n"
               "Filtered Rows     = keep rows where Compliance Group 3 <> null\n"
               "Renamed Columns   = Group 3 -> Compliance Sub Groups, Group 4 -> Compliance Groups, Notes -> Requirements Notes\n"
               "Sorted Rows       = Compliance Groups desc, Required (T/F) desc\n"
               "Reordered Columns = Name, Compliance Type, Required (T/F), Core Requirement, Requirements Notes, Managed By,\n"
               "                    Unique Lookup, Compliance Timeframe, Onboarding, Groups, Sub Groups, Threshold 1..5"),
          H("4.2 Requirements query (rows 249–257)", 1),
          para("The same chain, with three differences: it also combines <b>complications_requirements_Table</b>; it expands <b>Compliance Group 1 and 2</b> "
               "(not 3 and 4); and both filter steps are <font name='DVM'>each true</font>, so they keep every row. There are therefore two group hierarchies "
               "(1/2 and 3/4) feeding different dashboard tables (DS-08)."),
          H("4.3 Formula columns added to both tables (rows 210–226 and 258–274)", 1),
          table([
              ["Column", "Rule", "Client’s reason"],
              ["Compliance Group and Sub Group; …, Sub Group and Type", "Text keys “Group-Sub Group” and “Group-Sub Group-Type”", "Next columns and Power BI visuals"],
              ["<b>Due Date</b>", "From the store by Unique Lookup 4. No record → text “No record”; date 0 → “No expiry date set”", "Monitor and chase; feeds Power BI"],
              ["<b>Compliance Status</b>", "From the store’s Compliant. <b>No record → “Non Compliant”</b>", "Monitor and chase; feeds Power BI"],
              ["Notes", "From the store’s Compliance Notes", "Monitor and chase"],
              ["Compliance Completion Status", "From the store’s Completion Status; no record → “Missing”", "Unclear whether the dashboard uses it"],
              ["<b>Compliance</b> / Compliance (Core)", "1 if Compliant, 0 if not; blank unless Required = TRUE <b>and Active = TRUE</b> (and Core = “Core” for the Core column)", "Used in the percentage"],
              ["% Compliant (and Core) per type", "AVERAGEIFS of Compliance for the Group-Sub Group-Type key, on its first row only", "Feeds Power BI"],
              ["<b>Type RAG Score</b> (and Core)", "% ≥ Threshold 1 → 1; ≥ T2 → 0.8; ≥ T3 → 0.6; ≥ T4 → 0.4; ≥ T5 → 0.2; else 0", "“Used later in a compliance rank – unclear on reporting purpose”"],
              ["Type Encoded", "Character codes of the type name joined by spaces", "Unclear"],
              ["Type Rank (Base / Base 2 / Base 3 / Final)", "Rank within sub group by Core RAG score, ascending (1 = worst); ties broken by adding encoded-name digits ÷ 10<super>16</super>; Final = MAX per type", "Unclear"],
          ], [44, 92, 44]), PageBreak()]

    # 5 ------------------------------------------------------------------
    s += [H("5. Scoring Model (RAG roll-up)", 0),
          para("Scores run from 0 to 1. The dashboard gauges are coloured from these scores against Thresholds 1–5 of each compliance type "
               "(set per type in the tools’ Compliance Timeframes tables)."),
          table([
              ["Level", "Percentage", "RAG score"],
              ["Type", "Average of 1/0 over required, active rows", "Threshold bands 1 / 0.8 / 0.6 / 0.4 / 0.2 / 0"],
              ["Sub group", "Average of type percentages (Onboarding excluded)", "Special rules for Incidents and HR Metrics; otherwise see 5.1 (Accreditation excluded)"],
              ["Group", "Average of sub-group percentages", "Threshold bands against the group’s average thresholds (Accreditation Prep excluded; Core version excludes “Accreditation”)"],
          ], [22, 70, 88]),
          H("5.1 Sub-group RAG (rows 243–244)", 1),
          table([
              ["Sub group", "Rule, checked in this order"],
              ["<b>Incidents</b>", "1. Any type at RAG 0 whose name contains neither “SPC” nor “Moderate” → <b>0</b><br/>"
                                   "2. Exactly one “Moderate Harm” at RAG 0 → <b>0.5</b><br/>3. Two or more “SPC” types at RAG 0 → <b>0.5</b><br/>"
                                   "4. One “SPC” type at RAG 0 → <b>0.8</b><br/>5. Otherwise → <b>1</b>"],
              ["<b>HR Metrics</b>", "Two or more SPC types at RAG 0 → 0.5; one → 0.8; otherwise 1"],
              ["All others", "Gate: average type RAG minus a penalty for types at 0 % (0.3 for one, 0.6 for two, 0.9 for three, 1 for four or more). "
                             "If the result is below 0 → <b>0</b>. Otherwise the sub group’s % against the average Thresholds 1–5 → 1 / 0.8 / 0.6 / 0.4 / 0.2 / 0"],
          ], [26, 154]),
          para("<b>Note.</b> The penalty only acts as a gate: it can force 0, but it never lowers a score that passes. "
               "Two failing Moderate Harm types fall through to the SPC rules and can score 1 (DS-07)."),
          H("5.2 Worked example", 1),
          para("A sub group with four types at 100 %, 100 %, 50 % and 0 %, all with thresholds 1 / 0.9 / 0.8 / 0.7 / 0.6:"),
          *bullets(["Type RAG scores: 1, 1, 0, 0 (50 % is below Threshold 5). Average 0.5.",
                   "One type at 0 % → penalty 0.3. 0.5 − 0.3 = 0.2, not below 0, so the gate passes.",
                   "Sub-group % = 62.5 %, which is ≥ Threshold 5 (0.6) but < Threshold 4 (0.7) → <b>RAG 0.2</b>.",
                   "With a second type at 0 % the penalty would be 0.6 and the gate would force 0."]),
          PageBreak()]

    # 6 ------------------------------------------------------------------
    s += [H("6. The Self-Referencing Query and “Refresh Twice”", 0),
          code("Source         = Excel.Workbook(File.Contents(\"Z:\\Performance Dashboards and Data\\Data Store\\Compliance Data.xlsm\"), null, true)\n"
               "Navigation     = Source{[Item=\"requirements_Table\",Kind=\"Table\"]}[Data]\n"
               "Changed Type   = 26 typed columns\n"
               "Removed Other  = keep 29 columns (incl. Active, Due Date, Compliance Type Rank (Final))\n"
               "Appended Query = Table.Combine({#\"Removed Other Columns\", requirements_Table_Self_Reference})\n"
               "Changed Type 1 = Compliance Type Rank (Final) as Int64"),
          *bullets([
              "The query reads <b>the saved copy of its own file</b> from Z:\\, so it sees the values from the last save, not what is on screen. "
              "The formulas must recalculate and the file be saved before the roll-ups are right: this is why the recordings refresh twice.",
              "If the file is open elsewhere or the path changes, the query fails, which matches the “UNABLE TO REFRESH – linked workbook” message.",
              "It then appends <font name='DVM'>requirements_Table_Self_Reference</font>, whose contents are not documented. If it holds the previous output, rows may be doubled (DS-09).",
              "In the new system all of this becomes one calculation step after load; no file reads itself.",
          ]),
          H("6.1 Roll-up columns on requirements_Final_Self_Ref (rows 234–248)", 1),
          table([
              ["Column", "Rule", "Client’s reason"],
              ["Sub Groups % Compliant (and Core)", "Average of type % per Group-Sub Group, first row only; Onboarding excluded", "Feeds Power BI"],
              ["Groups % Compliant (and Core)", "Average of sub-group % per group, first row only", "Feeds Power BI"],
              ["Sub Groups Encoded, Rank Base–Final", "Same tie-break ranking as types, within each group; Onboarding and Accreditation Prep excluded", "Unclear"],
              ["Sub Groups RAG (and Core)", "§5.1", "Unclear"],
              ["Groups RAG (and Core)", "Threshold bands on group %", "Unclear"],
              ["Last Reviewed Date", "Last Updated[Updated] for Group-Sub Group", "Data quality"],
              ["Column1", "Average of Threshold 3 per Group-Sub Group", "“Currently unknown what threshold references refer to”"],
          ], [48, 92, 40]), PageBreak()]

    # 7 ------------------------------------------------------------------
    s += [H("7. VBA", 0),
          para("<b>No compliance VBA is in the template.</b> The word appears in the Compliance rows only in the Last Updated note (" + T4 + "201). "
               "The one macro supplied (" + T4 + "49) belongs to the Self-Pay Customers tool. It is the only example of how the client’s tools write to a "
               "store, so it shows the likely pattern of the compliance tools."),
          code("Private Sub Workbook_Open()   ' opens the store workbook when the tool opens\n"
               "  Workbooks.Open \"Z:\\Invoices & Scorecards\\Main Data Store\\Self Pay Reporting\\Self Pay Customers Store.xlsx\"\n"
               "Sub copyData()\n"
               "  New_Referrals.Unprotect : New_Referrals.Calculate\n"
               "  PD_Customers.AutoFilter Field:=14, Criteria1:=\"Copy - new customer\"\n"
               "  copy visible A2:V  ->  PasteSpecial xlPasteValues below the last row of 'PowerDiary Customers'\n"
               "  clear filter : Protect : wb2.Save : Debug.Print \"Done\""),
          table([
              ["Pattern", "Risk in the compliance tools"],
              ["Append-only, chosen by a helper flag column", "No check against the store, so a wrong flag or a second run duplicates rows"],
              ["Fixed positions (A:V, field 14)", "Adding or moving a column silently copies the wrong data"],
              ["Hard-coded Z:\\ paths", "Breaks when a drive mapping or folder changes"],
              ["No log, no rollback, no user stamp", "No audit trail of who wrote what and when"],
          ], [60, 120]),
          para("<b>Still required:</b> a .bas export of every module in the 11 tools and in Compliance Data.xlsm, and a list of which tools use a macro "
               "and which are pasted by hand (DS-12)."),
          PageBreak()]

    # 8 ------------------------------------------------------------------
    s += [H("8. Findings", 0), table([
        ["ID", "Finding", "Evidence", "Effect"],
        ["DS-01", "Most Recent Record is TRUE for every row of a person/type when none has a Completion Date", "Row 191", "Several “latest” rows; XLOOKUP returns the first, which may not be right"],
        ["DS-02", "Default rule counts a blank Due Date as Compliant", "Row 192", "Missing data shows green"],
        ["DS-03", "Training is Compliant whenever Completion Status is filled, regardless of expiry", "Row 192", "Lapsed training may show green; confirm against spec 04"],
        ["DS-04", "“Expires within 3 months / 2 weeks” has no lower bound", "Row 193", "Overdue items are also labelled as expiring"],
        ["DS-05", "Weeks Non Compliant uses Due Date even where status comes from Issue", "Rows 192, 194", "≈ 6,600 or negative weeks"],
        ["DS-06", "Missing record → “Non Compliant”; Due Date column mixes dates with “No record” text", "Rows 212–213", "Correct for chasing, but the column type is mixed"],
        ["DS-07", "Incidents sub-group rule: two failing Moderate Harm types are not caught by rule 2", "Row 243", "Score may be 1 instead of 0.5 or 0"],
        ["DS-08", "Two group hierarchies: Requirements uses Group 1/2, Requirements_Detailed Group 3/4", "Rows 204, 251", "Same data, two groupings in the dashboard; ties to spec 01 decision D-02"],
        ["DS-09", "Self-referencing query plus an undocumented self-reference append", "Rows 228–233", "“Refresh twice”, refresh errors, possible doubled rows"],
        ["DS-10", "Complications missing from Requirements_Detailed but present in Requirements and Timeframes", "Rows 202, 227, 249", "Complications may be absent from one dashboard table"],
        ["DS-11", "RTT (folder 06) is not a named area", "Rows 202, 227", "Its group must be confirmed to know which rule applies"],
        ["DS-12", "Template says tools copy via VBA; recordings show mostly manual paste; no compliance VBA supplied", "01 B12, row 49", "Write logic still unknown"],
        ["DS-13", "Exclusion names differ: “Accreditation” vs “Accreditation Prep”", "Rows 239, 243–246", "One of them probably never matches"],
        ["DS-14", "Formula anchors differ between columns (Q$1:Q1, Q$1:Q2, J$1:J3)", "Rows 243–246", "If the range includes the current row, the first-row test always fails and the column is blank; check in the live file"],
        ["DS-15", "First-row tests use fixed column letters (J, Q, S)", "Rows 218, 234, 236", "Inserting a column breaks the roll-ups"],
        ["DS-16", "Rank tie-break adds 14 digits ÷ 10<super>16</super> to an integer rank", "Rows 224, 240", "Beyond double precision, so ties can survive"],
        ["DS-17", "17 rows marked Unclear/Unknown: Snapshot, Encoded, Rank columns, roll-up RAGs, Column1", "Column “Why You Do It”", "Keep-or-retire decision needed"],
    ], [13, 70, 27, 70]), PageBreak()]

    # 9 ------------------------------------------------------------------
    s += [H("9. What This Means for Each Area", 0), table([
        ["Folder", "Level 2 rule that applies", "Extra roll-up rule", "Ask added to the pre-build PDF"],
        ["01 Staff Management", "Default: Due Date after today or blank", "—", "Blank due date = compliant? (DS-02)"],
        ["02 / 07 Incidents", "Issue = 10", "Incidents sub-group rule (§5.1)", "Confirm the rule and the Moderate Harm gap (DS-07)"],
        ["03 Complications", "Issue = 10", "Default gate", "Add to Requirements_Detailed? (DS-10)"],
        ["04 Mandatory Training", "Completion Status not blank", "Default gate", "Should expiry count? (DS-03)"],
        ["05 Survey Feedback", "Issue = 10", "Default gate", "Confirm Issue = 10 for SPC results"],
        ["06 RTT", "Depends on its group (not named)", "Depends on its group", "Which area and Level 2 group? (DS-11)"],
    ], [30, 46, 40, 64]), Spacer(1, 4),
          para("Every folder also gets three shared asks: the tool’s VBA export, the missing-record and Active rules, and the keep-or-retire list."),
          H("9.1 Build implications", 1)] + bullets([
        "<b>Rules engine:</b> one table of compliance rules keyed by Level 2 group (Issue score, completion status or due date), versioned, replacing the SWITCH in row 192.",
        "<b>Scoring service:</b> type → sub group → group roll-up with thresholds per type, the Incidents and HR Metrics rules as named, tested rules, and the exclusions as configuration.",
        "<b>Explicit states:</b> “No record”, “No expiry date set” and “Missing” become status values, not text in a date column.",
        "<b>Latest-record view:</b> a database view replaces Most Recent Record and Unique Lookups 1–4; ties resolved by a record ID, not by position.",
        "<b>No self-reference:</b> calculations run once after each load, and the publish date replaces the Last Updated table.",
        "<b>Parity test:</b> recompute today’s scores from a copy of Compliance Data.xlsm and compare type, sub-group and group results before go-live.",
        "<b>Sizing:</b> about 4,000 records growing by up to 20 a week, kept for 7 years.",
    ]) + [PageBreak()]

    # 10 -----------------------------------------------------------------
    rows = [["✓", "ID", "Question for the client", "Owner"],
            ["☐", "DS-02", "Should a blank due date count as compliant?", "Business owner"],
            ["☐", "DS-03", "Should Training lapse at expiry, or stay compliant once completed?", "Business owner"],
            ["☐", "DS-04", "Should overdue items be excluded from “expires within”?", "Business owner"],
            ["☐", "DS-07", "What should two failing Moderate Harm types score?", "Incident governance lead"],
            ["☐", "DS-08", "Which group hierarchy (1/2 or 3/4) does each dashboard page use? Are both needed?", "BI owner"],
            ["☐", "DS-09", "What is requirements_Table_Self_Reference?", "Tool owner"],
            ["☐", "DS-10", "Should Complications be in Requirements_Detailed?", "Tool owner"],
            ["☐", "DS-11", "Which area and Level 2 group does RTT belong to?", "Tool owner"],
            ["☐", "DS-12", "Export all VBA modules; which tools use a macro to write to the store?", "IT / tool owner"],
            ["☐", "DS-13", "Is the exclusion “Accreditation” or “Accreditation Prep”?", "Business owner"],
            ["☐", "DS-14", "Are the Core sub-group and group RAG columns populated in the live file?", "Tool owner"],
            ["☐", "DS-17", "Keep or retire Snapshot, the Encoded and Rank columns, and Column1?", "Business owner + BI owner"]]
    s += [H("10. Questions for the Client", 0),
          para("These also appear, by area, in each folder’s pre-build checklist."),
          table(rows, [7, 14, 119, 40])]
    doc.multiBuild(s)


if __name__ == "__main__":
    build(sys.argv[1])
