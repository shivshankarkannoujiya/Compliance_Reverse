# -*- coding: utf-8 -*-
"""00_Overview: how the seven reverse-engineered workflows relate to each other and to the data store."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reportlab.platypus import Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon
import build as B

mm = B.mm
para, H, table, bullets = B.para, B.H, B.table, B.bullets

INK = colors.HexColor("#1b2430"); MUTED = colors.HexColor("#5b6675")
SRC = colors.HexColor("#eef2f7"); TOOL = colors.HexColor("#e3edf9"); STORE = colors.HexColor("#fff1dc"); OUT = colors.HexColor("#e6f4ea")
EDGE = colors.HexColor("#8a96a6"); ACC = colors.HexColor("#1f5fa8")

FOLDERS = [
    ("01", "Staff Management", "01_Staff_Management", "first/ (131142, 11/08/2026)"),
    ("02", "Incident Management (partial)", "02_Incident_Management", "second/ (135933, 11/08/2026)"),
    ("03", "Complications", "03_Complications", "third/ (120551, 14/08/2026)"),
    ("04", "Mandatory Training", "04_Mandatory_Training", "fourth/ (113314, 14/08/2026)"),
    ("05", "Survey Feedback", "05_Survey_Feedback", "fifth/ (111322, 14/08/2026)"),
    ("06", "RTT Compliance", "06_RTT_Compliance", "sixth/ (MEDDAD~1, 14/08/2026)"),
    ("07", "Incident Management (full)", "07_Incident_Management_Full_Process", "seventh/ (102641, 14/08/2026)"),
]


def box(d, x, y, w, h, fill, title, sub=None, size=7.2):
    d.add(Rect(x, y, w, h, rx=3, ry=3, fillColor=fill, strokeColor=EDGE, strokeWidth=0.6))
    d.add(String(x + w / 2, y + h - 10, title, fontName="DVB", fontSize=size, fillColor=INK, textAnchor="middle"))
    if sub:
        for i, line in enumerate(sub if isinstance(sub, list) else [sub]):
            d.add(String(x + w / 2, y + h - 20 - i * 8.5, line, fontName="DV", fontSize=6.2, fillColor=MUTED, textAnchor="middle"))


def arrow(d, x1, y1, x2, y2, label=None, dashed=False):
    ln = Line(x1, y1, x2, y2, strokeColor=EDGE, strokeWidth=0.8)
    if dashed:
        ln.strokeDashArray = [2, 2]
    d.add(ln)
    import math
    a = math.atan2(y2 - y1, x2 - x1); L = 4.5
    p1 = (x2 - L * math.cos(a - 0.4), y2 - L * math.sin(a - 0.4)); p2 = (x2 - L * math.cos(a + 0.4), y2 - L * math.sin(a + 0.4))
    d.add(Polygon([x2, y2, p1[0], p1[1], p2[0], p2[1]], fillColor=EDGE, strokeColor=EDGE, strokeWidth=0.3))
    if label:
        d.add(String((x1 + x2) / 2, (y1 + y2) / 2 + 2.5, label, fontName="DV", fontSize=5.6, fillColor=MUTED, textAnchor="middle"))


def architecture():
    W, Hh = 180 * mm, 128 * mm
    d = Drawing(W, Hh)
    colw = [40 * mm, 56 * mm, 44 * mm, 24 * mm]
    xs = [0, 44 * mm, 106 * mm, 155 * mm]
    rows = [
        ("Typed by hand", "01 Staff Management.xlsm", "VBA write"),
        ("ESR · WFS · CIC L&D reports", "04 Training Matrix v3", "delete + paste all"),
        ("Survicate (4 surveys)", "05 24 hr All Surveys + Survey Mgmt", "paste"),
        ("RLDatix export", "02 / 07 Incident Management.xlsm", "paste"),
        ("SystmOne → breach report", "06 RTT Data", "paste"),
        ("SystmOne + appointments", "03 Complications Report.xlsm", "paste"),
    ]
    top = Hh - 9 * mm; step = 20 * mm; bh = 13 * mm
    d.add(String(xs[0] + colw[0] / 2, Hh - 6, "SOURCES", fontName="DVB", fontSize=7, fillColor=ACC, textAnchor="middle"))
    d.add(String(xs[1] + colw[1] / 2, Hh - 6, "USER-INPUT TOOLS (Z:\\…\\User input)", fontName="DVB", fontSize=7, fillColor=ACC, textAnchor="middle"))
    d.add(String(xs[2] + colw[2] / 2, Hh - 6, "DATA STORE (Z:\\…\\Data Store)", fontName="DVB", fontSize=7, fillColor=ACC, textAnchor="middle"))
    d.add(String(xs[3] + colw[3] / 2, Hh - 6, "OUTPUT", fontName="DVB", fontSize=7, fillColor=ACC, textAnchor="middle"))
    store_y = top - 5 * step - bh; store_h = 5 * step + bh
    box(d, xs[2], store_y, colw[2], store_h, STORE, "Compliance Data.xlsm",
        ["", "Compliance Data table", "(one row per evidence record,", "all areas, ~4,268 rows)", "",
         "requirements_Final / _Self_Ref", "compliance_Timeframes_Table", "(Power Query union of every", "tool’s Requirements and", "Timeframes tabs)", "",
         "Last Updated (edited by hand)", "", "Save → refresh twice", "“UNABLE TO REFRESH –", "linked workbook”"], size=8)
    box(d, xs[3], store_y + store_h / 2 - 15 * mm, colw[3], 30 * mm, OUT, "Compliance", ["Dashboard", "(gauges, filters", "Active = TRUE)", "", "read after", "refresh"], size=7.5)
    arrow(d, xs[2] + colw[2], store_y + store_h / 2, xs[3], store_y + store_h / 2)
    for i, (src, tool, how) in enumerate(rows):
        y = top - i * step - bh
        box(d, xs[0], y, colw[0], bh, SRC, src)
        box(d, xs[1], y, colw[1], bh, TOOL, tool, ["Requirements · Timeframes · output rows", "→ data store: " + how])
        arrow(d, xs[0] + colw[0], y + bh / 2, xs[1], y + bh / 2)
        arrow(d, xs[1] + colw[1], y + bh / 2, xs[2], y + bh / 2)
    # cross links
    y05 = top - 2 * step - bh; y02 = top - 3 * step - bh
    arrow(d, xs[1] + 4 * mm, y05, xs[1] + 4 * mm, y02 + bh, None, dashed=True)
    d.add(String(xs[1] + 6 * mm, (y05 + y02 + bh) / 2 - 2, "05 reads 02/07’s Estates tab", fontName="DV", fontSize=5.6, fillColor=MUTED))
    y01 = top - bh; y04 = top - step - bh
    d.add(Line(xs[1] + colw[1] - 6 * mm, y01, xs[1] + colw[1] - 6 * mm, y04 + bh, strokeColor=colors.HexColor("#c0504d"), strokeWidth=0.8, strokeDashArray=[2, 2]))
    d.add(String(xs[1] + colw[1] - 8 * mm, (y01 + y04 + bh) / 2 - 2, "same staff, two registers", fontName="DV", fontSize=5.6, fillColor=colors.HexColor("#c0504d"), textAnchor="end"))
    return d


def build(out):
    doc = B.Doc(out, title="Compliance Dashboard – How the Seven Workflows Relate",
                header="Compliance Dashboard — Overview of the Seven Reverse-Engineered Workflows")
    doc.SOURCE = "Synthesis of specs 01–07"
    s = [Spacer(1, 22 * mm), para("OVERVIEW · READ THIS FIRST", "small"), Spacer(1, 3 * mm),
         Paragraph("How the Seven Workflows Relate", B.ss["title"]),
         Paragraph("One dashboard, one data store, seven Excel tools: the shared pattern, the links between areas, the common defects and "
                   "what this means for the build", B.ss["sub"]),
         table([["<b>Covers</b>", "Folders 01–07 in this repository (each holds a specification and a pre-build client requirements PDF)"],
                ["<b>Organisation</b>", "Provide Wellbeing Ltd — Compliance Dashboard"],
                ["<b>Evidence</b>", "Seven Teams recordings, 11/08/2026 and 14/08/2026; figure and section references point into the folder specs"],
                ["<b>Report date</b>", "16 October 2026"]], [40, 140], head=False, zebra=False),
         Spacer(1, 8 * mm),
         para("<b>In one sentence:</b> every recording is one compliance area of the same Compliance Dashboard. Each area is prepared in its own Excel "
              "“user input tool”, and every tool ends by feeding the same data store, <i>Compliance Data.xlsm</i>, which the dashboard reads."),
         PageBreak()]
    toc = TableOfContents()
    toc.levelStyles = [ParagraphStyle("t0", fontName="DVB", fontSize=9.5, leading=14, textColor=INK),
                       ParagraphStyle("t1", fontName="DV", fontSize=8.4, leading=11.5, leftIndent=12, textColor=INK)]
    s += [Paragraph("Contents", B.ss["h1"]), toc, PageBreak()]

    s += [H("1. Document Map", 0),
          para("Start here, then open the folder for the area you need. Every folder has the same two documents."),
          table([["Folder", "Area", "Recording", "Contents"]] +
                [["<b>%s</b>" % f[2], f[1], f[3], "*_Compliance_Workflow_Specification.pdf · *_PreBuild_Client_Requirements.pdf"] for f in FOLDERS],
                [46, 30, 38, 66]),
          Spacer(1, 4),
          para("<b>02 and 07 are the same tool.</b> 02 stops at a #REF! error; 07 records the whole process and answers most of 02’s gaps (07 §0.3). Read them together."),
          para("<b>Data store logic.</b> Compliance_Data_Store_Logic.pdf (this folder) documents every table, Power Query step and formula of "
               "Compliance Data.xlsm from the client’s source template, with 17 findings (DS-01…DS-17). Items it adds to each pre-build checklist carry a -DS suffix."),
          PageBreak()]

    s += [H("2. System Architecture", 0),
          para("Data flows left to right. Every tool has Requirements and Compliance Timeframes tabs (pulled into the data store by Power Query) and an "
               "output table whose rows are added to the data store’s Compliance Data table."),
          architecture(),
          para("Dashed lines: cross-tool links found in the recordings (§4)."),
          PageBreak()]

    s += [H("3. The Shared Pattern", 0),
          H("3.1 What every tool has", 1), table([
              ["Element", "Purpose", "Seen in"],
              ["Requirements tab", "Who or what must comply with which compliance type (Name, Type, Required, Core, Unique Lookup, Active)", "All seven"],
              ["Compliance Timeframes tab", "Review frequency, Compliance Group 1–4, Unique Lookup, Missing, Threshold 1–5 for the gauge colours", "All seven"],
              ["Output rows", "Name, Compliance Type, Completion Date, Status, RAG/Issue, Notes, Managed By, Due Date, Groups 1–4, Weighting", "All seven"],
              ["Monthly close", "Add rows to Compliance Data → edit Last Updated → save → refresh Power Query twice", "All seven"],
          ], [40, 105, 35]),
          H("3.2 Areas by dashboard group", 1), table([
              ["Compliance Group 1", "Area (folder)", "Subject", "Main source", "How rows reach the store"],
              ["People", "Staff Management (01)", "Each staff member", "Typed by the operator", "VBA “Add New Compliance”"],
              ["People", "Mandatory Training (04)", "Each staff member", "ESR, WFS, Provide CIC L&amp;D reports; contractor certificates", "Delete all training rows, paste all"],
              ["People", "Survey Feedback (05)", "Provide Wellbeing", "Survicate 24-hour surveys", "Paste 6 rows"],
              ["Operational", "Incidents (02, 07)", "Provide Wellbeing", "RLDatix", "Paste 10 rows"],
              ["Operational", "RTT (06)", "Provide Wellbeing (10 services)", "SystmOne → weekly RTT breach report", "Paste 10 rows weekly"],
              ["Clinical", "Complications (03)", "Provide Wellbeing", "Appointments store + SystmOne complication codes", "Paste 8 fixed rows"],
          ], [24, 32, 30, 54, 40]),
          H("3.3 Recording timeline", 1), table([
              ["Date", "Time", "Folder", "Note"],
              ["11/08/2026", "13:11", "01 Staff Management", "The .srt in first/ belongs to 02"],
              ["11/08/2026", "13:59", "02 Incidents (partial)", "Stops at #REF!"],
              ["14/08/2026", "10:26", "07 Incidents (full)", "Full process"],
              ["14/08/2026", "≈11:00", "06 RTT", "8.3 file name MEDDAD~1"],
              ["14/08/2026", "11:13", "05 Survey Feedback", ""],
              ["14/08/2026", "11:33", "04 Mandatory Training", "“Only two to go now”"],
              ["14/08/2026", "12:05", "03 Complications", "“The last video, at least for now”"],
          ], [24, 18, 48, 90]),
          PageBreak()]

    s += [H("4. Direct Links Between Areas", 0), table([
        ["Link", "What it means", "Evidence"],
        ["02 ↔ 07 same tool", "Same Incident Management.xlsm; on 11/08 the review-panel column was missing (#REF!), on 14/08 it was present", "02 §4.3, 07 §0.3"],
        ["01 ↔ 04 same people", "Staff appear in Staff Management’s Names tab and in the Training Matrix’s All Staff List, both keyed by name text", "01 §2.1, 04 §2.1"],
        ["05 → 02/07", "A Survey Management formula reads [Incident Management.xlsm]Estates by full path", "05 §2.5"],
        ["02/07 ↔ 05 shared method", "Both use SPC (statistical process control) rules on monthly figures", "07 §2.3, 05 §2.4"],
        ["03 → “another document”", "Complications requirements and timeframes come from an earlier automated version not yet seen", "03 §1.1"],
        ["All → Compliance Data", "Data store tables hold rows from every area together (staff, Estates, RTT, Feedback, Incidents)", "03 §1.3, 05/06/07 data-store figures"],
        ["Other tools not recorded", "The User input folder also holds Audit, Contract, Estates, Hand Hygiene/IPC, Medical Devices, Policy and Procedure, Sickness/Leave/Vacancy", "02 Fig. 2, 05 Fig. 13"],
    ], [34, 102, 44]), PageBreak()]

    s += [H("5. Problems Common to All Areas", 0),
          para("These recur because one design was copied from tool to tool. Each folder’s §4 has the area-specific detail."),
          table([
              ["Problem", "Areas", "Effect"],
              ["Name text as the only key", "All", "Renames, spelling variants and duplicates break or merge records"],
              ["Missing column always TRUE (searches its own table)", "02/07, 03, 04, 05, 06", "Column carries no information"],
              ["Unique Lookup with a trailing dash", "02/07, 05, 06", "Keys differ between tools"],
              ["Unexplained constants (0.5 months, Issue 10, Weighting 1)", "All except 01", "“Only Matt knows”"],
              ["TODAY() in rules", "02/07, 04, 05, 06", "Results change with the day the file is opened"],
              ["Manual copy-paste into the store", "02–07", "Duplicates, missed periods, no audit trail"],
              ["Last Updated edited by hand", "All", "Stale publish dates (01’s macro crashes)"],
              ["“UNABLE TO REFRESH – linked workbook”", "Data store", "Stale lookups across tools"],
              ["Logic understood by one person who left", "All", "Rules reconstructed or edited live (06), undocumented"],
              ["Patient or personal data in shared workbooks", "02/07, 03, 05, 06", "IG risk; blurred in all specs"],
          ], [62, 38, 80]),
          PageBreak()]

    s += [H("6. What This Means for the Build", 0),
          para("Build one platform, not seven tools. The design in spec 01 §5 is the base; each folder’s §5 adds its area’s specifics."),
          table([
              ["Platform component", "Replaces", "Used by"],
              ["Subject register (staff, sites, organisation) with system IDs and aliases", "Names tab, All Staff List, name keys", "01, 04 (and all for the organisation)"],
              ["Requirements and compliance-type catalogue (versioned)", "Requirements and Compliance Timeframes tabs in every tool", "All"],
              ["Source connectors with header contracts", "Copy-paste of exports", "Datix (02/07), SystmOne (03, 06), Survicate (05), ESR/WFS/L&amp;D (04)"],
              ["Rules engine: expiry, harm timeframes, RTT dates, attribution", "Formulas in each tool", "01, 02/07, 03, 04, 06"],
              ["SPC engine with versioned parameters", "SPC sheets", "02/07, 05"],
              ["Append-only evidence ledger + current-state views", "Compliance Data table, delete-and-replace", "All"],
              ["Review gate and atomic publish with as-of date", "Save + refresh twice, Last Updated", "All"],
              ["Restricted zone for patient-level data", "Patient data in shared workbooks", "02/07, 03, 05, 06"],
          ], [62, 60, 58]),
          H("6.1 Suggested delivery order", 1), table([
              ["Order", "Area", "Why"],
              ["1", "Platform + 01 Staff Management", "Defines the subject register, catalogue and publish step everything else uses"],
              ["2", "04 Mandatory Training", "Same people as 01; removes the delete-and-replace"],
              ["3", "06 RTT", "Weekly, simple rule; fixes the live-edit risk"],
              ["4", "02/07 Incidents", "Adds the Datix connector and the SPC engine"],
              ["5", "05 Survey Feedback", "Reuses the SPC engine"],
              ["6", "03 Complications", "Most manual; needs clinical governance decisions first"],
          ], [14, 50, 116]),
          H("6.2 Blockers across all folders", 1)] + bullets([
              "VBA and Power Query code for every tool, and a copy of Compliance Data.xlsm with its queries.",
              "Business-owner decisions on core flags, thresholds and RAG rules (they differ between tools).",
              "Information-governance approval for patient-level data (Incidents, Complications, RTT, Feedback).",
              "Recordings or walkthroughs for the tools not yet recorded (Audit, Contract, Estates, Medical Devices and others).",
          ])
    doc.multiBuild(s)


if __name__ == "__main__":
    build(sys.argv[1])
