import subprocess, sys
from PIL import Image, ImageFilter, ImageStat, ImageChops
sys.path.insert(0,'.'); from figures import FIGS
V="/home/user/Compliance_Reverse/first/Microsoft Teams meeting-20260811_131142-Meeting Recording (1).mp4"
CROPS={"xl":(0,95,1675,990),"top":(0,290,1675,700),"full":(0,0,1920,1080),"popup":(350,380,1350,1080)}
def grab(t,out):
    subprocess.run(["ffmpeg","-v","error","-y","-ss",t,"-i",V,"-frames:v","1","-q:v","1",out],check=True)
rep=[]
for fid,ts,wb,tab,cap,crop in FIGS:
    seek = "00:29:38.0" if fid=="tb" else ts
    grab(seek,f"figs/raw_{fid}.png")
    h,m,s=map(float,seek.split(":")); t2=h*3600+m*60+s+0.5
    grab(str(t2),"figs/_n.png")
    a=Image.open(f"figs/raw_{fid}.png").convert("RGB"); b=Image.open("figs/_n.png").convert("RGB")
    c=CROPS[crop]; im=a.crop(c); im.save(f"figs/{fid}.png")
    sharp=ImageStat.Stat(im.convert("L").filter(ImageFilter.FIND_EDGES)).var[0]
    stab=ImageStat.Stat(ImageChops.difference(im,b.crop(c))).mean[0]
    rep.append((fid,ts,round(sharp),round(stab,2),im.size))
Image.open("/tmp/claude-0/-home-user-Compliance-Reverse/8cdfedab-e5dd-5414-8a84-f69ce68208e2/scratchpad/work/full/f_0135.jpg").crop(CROPS["xl"]).save("figs/ct3.png")
for r in rep: print(*r)
