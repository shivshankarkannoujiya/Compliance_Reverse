# -*- coding: utf-8 -*-
"""Companion PDF: everything the client must supply or decide before the modern system can be built.

Reuses the styles, table and figure helpers of build.py so figure numbers match the main specification.
The item tables live in prereq_<profile>.py; REPORT_PROFILE selects which recording.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reportlab.platypus import Paragraph, Spacer, PageBreak
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import ParagraphStyle
import build as B

mm = B.mm
para, H, table, bullets, figure, figref = B.para, B.H, B.table, B.bullets, B.figure, B.figref
COLS = ["ID", "What is required", "Why it is required (evidence)", "Who", "Blocks", "Spec ref"]
W = [11, 40, 74, 18, 20, 17]


def sref(t):
    return "Spec " + figref(t)


def build(out):
    import importlib
    D = importlib.import_module({"staff": "prereq_staff", "incidents": "prereq_incidents", "complications": "prereq_complications", "training": "prereq_training", "feedback": "prereq_feedback"}[B.PROFILE])
    M = D.META
    tables = (D.FILES, D.SHEETS, D.VBA, D.RULES, D.DECISIONS)
    blockers = M["blockers"]

    def blk(prefix):
        ids = sorted(b for b in blockers if b.startswith(prefix))
        return ", ".join(ids) if ids else "—"

    doc = B.Doc(out, title=M["title"], header=M["header"])
    s = [Spacer(1, 22 * mm), para("COMPANION TO THE TECHNICAL SPECIFICATION", "small"), Spacer(1, 3 * mm),
         Paragraph("Pre-Build Client Requirements", B.ss["title"]),
         Paragraph(M["subtitle"], B.ss["sub"]),
         table([["<b>Applies to</b>", M["applies"]],
                ["<b>Companion of</b>", M["spec"] + " (same folder). “Spec Figure N” and IDs such as P-xx, G-xx, FM-xx, FR-xx refer to that document"],
                ["<b>Evidence</b>", M["evidence"]],
                ["<b>Report date</b>", "16 October 2026"],
                ["<b>Status</b>", "Open: awaiting client inputs. Build Phase 1 cannot start until every <b>Blocker</b> item in §6 is ticked"]],
               [40, 140], head=False, zebra=False),
         Spacer(1, 8 * mm),
         para("<b>Why this document exists.</b> " + M["why"] + " This list turns them into <b>%d concrete asks</b>, "
              "each with a reason, the evidence, who should answer it and what it blocks." % sum(len(t) - 1 for t in tables)),
         para("<b>How to use it:</b> work through §1–§5, attach files or answers against each ID, then sign the checklist in §6. "
              "Anything marked <i>Blocker</i> stops the build; the rest can be answered during Phase 1.")]
    s.append(PageBreak())
    toc = TableOfContents()
    toc.levelStyles = [ParagraphStyle("t0", fontName="DVB", fontSize=9.5, leading=14, textColor=B.INK),
                       ParagraphStyle("t1", fontName="DV", fontSize=8.4, leading=11.5, leftIndent=12, textColor=B.INK)]
    cats = ["1. Files to supply", "2. Sheets, tabs and columns to explain", "3. VBA macros to explain", "4. Business rules to confirm", "5. Client decisions"]
    s += [Paragraph("Contents", B.ss["h1"]), toc, Spacer(1, 6 * mm),
          H("Summary", 0),
          table([["Category", "Items", "Blockers", "Main owner"]] +
                [[cat, str(len(t) - 1), blk(pre), own] for cat, t, pre, own in zip(cats, tables, ("F-", "S-", "V-", "R-", "D-"), M["owners"])],
                [60, 18, 60, 42]),
          PageBreak()]

    intros = ["Read-only copies are enough. Without these files the main logic and the target data shapes stay unknown.",
              "These are parts of the workbook that were hidden, never opened, or behaved unexpectedly in the recording.",
              "For each macro we need either the source code (F-01) or a short written description from someone who knows it. "
              "The questions below are the minimum answers needed.",
              "The new system calculates these instead of relying on people. The rule must be written down and agreed, "
              "because once automated it applies to every record.",
              M["decisions_intro"]]
    heads = ["1. Files to Supply", "2. Sheets, Tabs and Columns to Explain", "3. VBA Macros to Explain",
             "4. Business Rules to Confirm", "5. Client Decisions Required"]
    for hd, intro, t, figs in zip(heads, intros, tables, M["figs"]):
        s += [H(hd, 0), para(intro), table(t, W), Spacer(1, 4)]
        s += [figure(f, h * mm) if h else figure(f) for f, h in figs]
        s.append(PageBreak())

    import re
    rows = [["✓", "ID", "Item", "Owner", "Priority", "Received / decided (date, by)"]]
    for r in (r for t in tables for r in t[1:]):
        title = re.sub(r"<[^>]+>", "", r[1]).split(":")[0].split("(")[0].strip()
        rows.append(["☐", r[0], title[:70], r[3], "<b>Blocker</b>" if r[0] in blockers else "Phase 1", ""])
    s += [H("6. Sign-off Checklist", 0),
          para("Tick each item when the file is received or the decision is recorded. Phase 1 (Foundation) starts when every "
               "<b>Blocker</b> is ticked."),
          table(rows, [7, 11, 76, 28, 17, 41]), Spacer(1, 10 * mm),
          H("Signatures", 1), para("Signing confirms that every Blocker above has been supplied or decided and that the build can start."),
          table([["<b>Business owner</b>", "Name: ____________________", "Signature: ____________________", "Date: __________"],
                 ["<b>IG lead / DPO</b>", "Name: ____________________", "Signature: ____________________", "Date: __________"],
                 ["<b>Delivery lead</b>", "Name: ____________________", "Signature: ____________________", "Date: __________"]],
                [32, 52, 60, 36], head=False, zebra=False)]
    doc.multiBuild(s)
    B.EMBEDDED.clear()


if __name__ == "__main__":
    build(sys.argv[1])
