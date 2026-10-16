import subprocess, sys
from PIL import Image, ImageFilter, ImageStat, ImageChops
import os, importlib
sys.path.insert(0,'.')
# REPORT_PROFILE selects the recording, figure manifest and output folder (see build.py).
PROFILE=os.environ.get("REPORT_PROFILE","staff")
FIG_MOD,FIG_DIR,V={"staff":("figures","figs","/home/user/Compliance_Reverse/first/Microsoft Teams meeting-20260811_131142-Meeting Recording (1).mp4"),
                   "incidents":("figures_incidents","figs_incidents","/home/user/Compliance_Reverse/second/Microsoft Teams meeting-20260811_135933-Meeting Recording.mp4")}[PROFILE]
FIGS=importlib.import_module(FIG_MOD).FIGS
os.makedirs(FIG_DIR,exist_ok=True)
CROPS={"xl":(0,95,1675,990),"top":(0,290,1675,700),"full":(0,0,1920,1080),"popup":(350,380,1350,1080),
       "explorer":(0,0,1675,1065),"refzoom":(1000,490,1675,990)}
def grab(t,out):
    subprocess.run(["ffmpeg","-v","error","-y","-ss",t,"-i",V,"-frames:v","1","-q:v","1",out],check=True)
rep=[]
from PIL import ImageFilter, ImageDraw
# Boxes (in cropped-image pixels) blurred to keep patient/staff details out of the report: Datix Name (B) and Description (G) cells.
REDACT={"redact_wide":[(77,345,163,835),(1051,345,1167,835)],
        "redact_narrow":[(71,322,160,835),(1012,322,1162,835)]}
def redact(im,boxes):
    for b in boxes:
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(9)),b[:2])
        ImageDraw.Draw(im).rectangle(b,outline=(200,60,60),width=2)
    return im
for fig in FIGS:
    fid,ts,wb,tab,cap,crop=fig[:6]
    seek = "00:29:38.0" if fid=="tb" else ts
    grab(seek,f"{FIG_DIR}/raw_{fid}.png")
    h,m,s=map(float,seek.split(":")); t2=h*3600+m*60+s+0.5
    grab(str(t2),f"{FIG_DIR}/_n.png")
    a=Image.open(f"{FIG_DIR}/raw_{fid}.png").convert("RGB"); b=Image.open(f"{FIG_DIR}/_n.png").convert("RGB")
    c=CROPS[crop]; im=a.crop(c)
    if len(fig)>6: im=redact(im,REDACT[fig[6]])
    im.save(f"{FIG_DIR}/{fid}.png")
    sharp=ImageStat.Stat(im.convert("L").filter(ImageFilter.FIND_EDGES)).var[0]
    stab=ImageStat.Stat(ImageChops.difference(im,b.crop(c))).mean[0]
    rep.append((fid,ts,round(sharp),round(stab,2),im.size))
if PROFILE=="staff":  # ct3 was taken from a verified 5 s grid frame (see README)
    Image.open("/tmp/claude-0/-home-user-Compliance-Reverse/8cdfedab-e5dd-5414-8a84-f69ce68208e2/scratchpad/work/full/f_0135.jpg").crop(CROPS["xl"]).save("figs/ct3.png")
for r in rep: print(*r)
