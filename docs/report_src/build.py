import sys, os, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
                                Image as RLImage, PageBreak, KeepTogether, CondPageBreak)
from reportlab.platypus.tableofcontents import TableOfContents
import importlib

HERE = os.path.dirname(os.path.abspath(__file__))
# One generator, several recordings: REPORT_PROFILE picks the figure manifest, content module and figure folder.
PROFILE = os.environ.get("REPORT_PROFILE", "staff")
PROFILES = {"staff": ("figures", "content", "figs"),
            "incidents": ("figures_incidents", "content_incidents", "figs_incidents"),
            "complications": ("figures_complications", "content_complications", "figs_complications"),
            "training": ("figures_training", "content_training", "figs_training"),
            "feedback": ("figures_feedback", "content_feedback", "figs_feedback"),
            "rtt": ("figures_rtt", "content_rtt", "figs_rtt")}
_FIG_MOD, _CONTENT_MOD, FIG_DIR = PROFILES[PROFILE]
FIGS = importlib.import_module(_FIG_MOD).FIGS
C = importlib.import_module(_CONTENT_MOD)
F = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DV", F + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", F + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVI", "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"))
pdfmetrics.registerFont(TTFont("DVM", F + "DejaVuSansMono.ttf"))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily("DV", normal="DV", bold="DVB", italic="DVI", boldItalic="DVB")

INK = colors.HexColor("#1b2430"); MUTED = colors.HexColor("#5b6675"); ACC = colors.HexColor("#1f5fa8")
RULE = colors.HexColor("#c9d1db"); HEAD = colors.HexColor("#e8eef6"); ZEBRA = colors.HexColor("#f6f8fb")
WARN = colors.HexColor("#fff4e5")

ss = {}
ss["body"] = ParagraphStyle("body", fontName="DV", fontSize=9, leading=12.6, textColor=INK, spaceAfter=4)
ss["small"] = ParagraphStyle("small", parent=ss["body"], fontSize=7.4, leading=9.6, spaceAfter=0)
ss["cell"] = ParagraphStyle("cell", parent=ss["body"], fontSize=7.2, leading=9.2, spaceAfter=0)
ss["cellh"] = ParagraphStyle("cellh", parent=ss["cell"], fontName="DVB")
ss["code"] = ParagraphStyle("code", parent=ss["body"], fontName="DVM", fontSize=6.6, leading=8.4, backColor=colors.HexColor("#f3f5f8"),
                            borderPadding=4, spaceBefore=3, spaceAfter=7)
ss["cap"] = ParagraphStyle("cap", parent=ss["body"], fontSize=7.8, leading=10.2, textColor=MUTED, spaceBefore=3, spaceAfter=10)
ss["h1"] = ParagraphStyle("h1", fontName="DVB", fontSize=16, leading=20, textColor=ACC, spaceBefore=4, spaceAfter=8)
ss["h2"] = ParagraphStyle("h2", fontName="DVB", fontSize=11.5, leading=15, textColor=INK, spaceBefore=10, spaceAfter=5)
ss["h3"] = ParagraphStyle("h3", fontName="DVB", fontSize=9.6, leading=13, textColor=INK, spaceBefore=8, spaceAfter=3)
ss["title"] = ParagraphStyle("title", fontName="DVB", fontSize=24, leading=30, textColor=INK, spaceAfter=6)
ss["sub"] = ParagraphStyle("sub", fontName="DV", fontSize=12, leading=17, textColor=MUTED, spaceAfter=18)
ss["bullet"] = ParagraphStyle("bullet", parent=ss["body"], leftIndent=11, bulletIndent=2, spaceAfter=2)
ss["callout"] = ParagraphStyle("callout", parent=ss["body"], backColor=WARN, borderPadding=6, spaceBefore=4, spaceAfter=10)


class Doc(BaseDocTemplate):
    HEADER = getattr(C, "HEADER", "Staff Management Compliance Workflow — Technical Specification (Reverse-Engineered)")
    SOURCE = getattr(C, "SOURCE", "Source: Teams recording 20260811_131142 (30:54)")

    def __init__(self, fn, title=getattr(C, "DOC_TITLE", "Staff Management Compliance Workflow – Reverse-Engineering Specification"),
                 header=None, **kw):
        super().__init__(fn, pagesize=A4, leftMargin=15 * mm, rightMargin=15 * mm, topMargin=17 * mm, bottomMargin=16 * mm,
                         title=title, author="Reverse-engineering specification (generated)", **kw)
        if header:
            self.HEADER = header
        fr = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="f")
        self.addPageTemplates([PageTemplate(id="p", frames=[fr], onPage=self.deco)])

    def deco(self, c, d):
        if d.page == 1:
            return
        c.saveState(); c.setFont("DV", 7); c.setFillColor(MUTED)
        c.drawString(15 * mm, A4[1] - 10 * mm, self.HEADER)
        c.drawRightString(A4[0] - 15 * mm, A4[1] - 10 * mm, self.SOURCE)
        c.setStrokeColor(RULE); c.line(15 * mm, A4[1] - 11.5 * mm, A4[0] - 15 * mm, A4[1] - 11.5 * mm)
        c.drawRightString(A4[0] - 15 * mm, 9 * mm, "Page %d" % d.page)
        c.restoreState()

    def afterFlowable(self, f):
        if isinstance(f, Paragraph) and getattr(f, "_toc", None) is not None:
            lvl, txt = f._toc
            key = "h%s_%d" % (txt[:20], self.page)
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(txt, key, level=lvl, closed=lvl > 0)
            self.notify("TOCEntry", (lvl, txt, self.page, key))


def para(t, st="body"):
    return Paragraph(t, ss[st])


def H(t, lvl):
    p = Paragraph(t, ss["h%d" % (lvl + 1)]); p._toc = (lvl, html.unescape(t.replace("<b>", "").replace("</b>", ""))); return p


FIGNUM = {}
for i, f in enumerate(FIGS, 1):
    FIGNUM[f[0]] = i


def figref(fid):
    f = FIGS[FIGNUM[fid] - 1]
    return "Figure %d [%s]" % (FIGNUM[fid], f[1][:8])


EMBEDDED = set()


def figure(fid, maxh=118 * mm):
    i = FIGNUM[fid]; f = FIGS[i - 1]
    if fid in EMBEDDED:
        return Paragraph("<i>Shown above: %s — %s</i>" % (figref(fid), html.escape(f[4][:110]) + ("…" if len(f[4]) > 110 else "")), ss["cap"])
    EMBEDDED.add(fid)
    path = os.path.join(HERE, FIG_DIR, fid + ".png")
    jpg = os.path.join(HERE, FIG_DIR, fid + "_e.jpg")
    if not os.path.exists(jpg):
        Image.open(path).convert("RGB").save(jpg, quality=90, optimize=True)
    w, h = Image.open(path).size
    W = 180 * mm; Hh = W * h / w
    if Hh > maxh:
        Hh = maxh; W = Hh * w / h
    img = RLImage(jpg, width=W, height=Hh); img.hAlign = "CENTER"
    tab = f[3]
    cap = "<b>Figure %d [%s] — %s › %s:</b> %s" % (i, f[1][:8], html.escape(f[2]), html.escape(tab), html.escape(f[4]))
    box = Table([[img]], colWidths=[W + 2]); box.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.5, RULE), ("LEFTPADDING", (0, 0), (-1, -1), 1),
                                                                      ("RIGHTPADDING", (0, 0), (-1, -1), 1), ("TOPPADDING", (0, 0), (-1, -1), 1), ("BOTTOMPADDING", (0, 0), (-1, -1), 1)]))
    return KeepTogether([box, Paragraph(cap, ss["cap"])])


def table(rows, widths, head=True, zebra=True, fs=None):
    data = []
    for r_i, r in enumerate(rows):
        st = ss["cellh"] if (head and r_i == 0) else ss["cell"]
        data.append([c if not isinstance(c, str) else Paragraph(c, st) for c in r])
    tw = sum(widths); scale = 180 * mm / tw
    t = Table(data, colWidths=[w * scale for w in widths], repeatRows=1 if head else 0)
    style = [("GRID", (0, 0), (-1, -1), 0.35, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
             ("TOPPADDING", (0, 0), (-1, -1), 2.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2)]
    if head:
        style.append(("BACKGROUND", (0, 0), (-1, 0), HEAD))
    if zebra:
        for k in range(1 if head else 0, len(rows)):
            if k % 2 == 0:
                style.append(("BACKGROUND", (0, k), (-1, k), ZEBRA))
    t.setStyle(TableStyle(style))
    return t


def bullets(items):
    return [Paragraph(x, ss["bullet"], bulletText="•") for x in items]


def code(t):
    from reportlab.platypus import Preformatted
    return Preformatted(t, ss["code"])


ctx = dict(para=para, H=H, figure=figure, figref=figref, table=table, bullets=bullets, code=code, ss=ss, mm=mm,
           PageBreak=PageBreak, CondPageBreak=CondPageBreak, Spacer=Spacer, FIGS=FIGS, FIGNUM=FIGNUM)


def build(out):
    doc = Doc(out)
    story = []
    # Title block
    story += [Spacer(1, 22 * mm), para("TECHNICAL SPECIFICATION · REVERSE-ENGINEERING REPORT", "small"), Spacer(1, 3 * mm),
              Paragraph(getattr(C, "TITLE", "Staff Management Compliance Datastore Update"), ss["title"]),
              Paragraph(getattr(C, "SUBTITLE", "Legacy Excel / VBA / Power Query workflow, reverse-engineered from an operator screen recording, "
                                               "with a target-state architecture for its replacement"), ss["sub"])]
    story.append(table(C.TITLE_BLOCK, [45, 135], head=False, zebra=False))
    story += [Spacer(1, 8 * mm), para(C.EXEC_SUMMARY_INTRO)] + bullets(C.EXEC_SUMMARY)
    story.append(PageBreak())
    toc = TableOfContents(); toc.dotsMinLevel = 0
    toc.levelStyles = [ParagraphStyle("t0", fontName="DVB", fontSize=9.5, leading=14, leftIndent=0, textColor=INK),
                       ParagraphStyle("t1", fontName="DV", fontSize=8.4, leading=11.5, leftIndent=12, textColor=INK)]
    story += [Paragraph("Table of Contents", ss["h1"]), toc, PageBreak()]
    for name in ("section0", "section1", "section2", "section3", "section4", "section5", "section6", "section7", "appendix"):
        story += getattr(C, name)(ctx)
    doc.multiBuild(story)
    EMBEDDED.clear()


if __name__ == "__main__":
    build(sys.argv[1])
