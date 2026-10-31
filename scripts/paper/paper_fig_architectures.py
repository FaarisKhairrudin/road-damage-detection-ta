"""Draw grouped architecture schematics from the two local YAML configurations.

Groups omit internal repeats/channels; arrows preserve the feature routes between
shown groups. RD fusion is the local concatenation-based adaptation, not Eq. 4.
"""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont("Diagram", "/usr/share/fonts/liberation-sans-fonts/LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("DiagramBold", "/usr/share/fonts/liberation-sans-fonts/LiberationSans-Bold.ttf"))
import math
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'latex/IEEE-Conference/gambar/paper_fig_architectures.pdf'
C = canvas.Canvas(str(OUT), pagesize=(1000, 440))
C.setTitle('Compact YOLOv8-PD and YOLO-RD reimplementations')
colors = dict(conv='#f9e6ae', feat='#bfe0e8', att='#cde6bc', head='#f7d2a9', bg='#fafafa')
def text(x,y,s,size=11,bold=False):
    C.setFillColor(HexColor('#222222')); C.setFont('DiagramBold' if bold else 'Diagram',size)
    C.drawCentredString(x,y,s,mode=0)
def box(x,y,w,h,lines,kind='feat'):
    C.setStrokeColor(HexColor('#555555'));C.setLineWidth(.65);C.setFillColor(HexColor(colors[kind]));C.roundRect(x-w/2,y-h/2,w,h,3,stroke=1,fill=1)
    for i,line in enumerate(lines.split('\n')):text(x,y+(len(lines.split('\n'))-1)*6-i*12-3,line)
def arrow(points):
    C.setStrokeColor(HexColor('#555555'));C.setFillColor(HexColor('#555555'));C.setLineWidth(.8)
    p=C.beginPath();p.moveTo(*points[0])
    for pt in points[1:]:p.lineTo(*pt)
    C.drawPath(p)
    x,y=points[-1];a=math.atan2(y-points[-2][1],x-points[-2][0]);p=C.beginPath();p.moveTo(x,y)
    for d in [-.45,.45]:p.lineTo(x-5*math.cos(a+d),y-5*math.sin(a+d))
    p.close();C.drawPath(p,stroke=0,fill=1)
def frame(x,title,labels):
    text(x+245,421,title,15,True)
    for cx,w,label in labels:
        C.setStrokeColor(HexColor('#aaaaaa'));C.setLineWidth(.6);C.setDash(3,2);C.roundRect(x+cx-w/2,48,w,347,4,stroke=1);C.setDash()
        text(x+cx,379,label,12,True)
# Panel A: YAML layers 0:4 / 5:6 / 7:11 grouped in backbone.
frame(0,'(a) YOLOv8-PD reimplementation',[(65,112,'Backbone'),(248,234,'Neck'),(425,100,'Head')])
box(65,350,98,25,'640 x 640 input','conv')
box(65,292,98,40,'Conv / C2f\nP3 (stride 8)')
box(65,210,98,40,'Conv / C2f\nP4 (stride 16)')
box(65,117,98,64,'Conv / C2f\nSPPF / BOT\nLSKA (stride 32)','att')
for a,b in [(337,312),(272,230),(190,149)]:arrow([(65,a),(65,b)])
# Neck top-down outputs at 210 and 292; local groups include upsample+concat.
box(191,210,98,52,'Upsample / Concat\nC2fGhost / LSKA')
box(191,292,98,52,'Upsample / Concat\nC2fGhost / LSKA')
arrow([(114,117),(191,117),(191,184)])
arrow([(114,210),(142,210)])
arrow([(191,236),(191,266)])
arrow([(114,292),(142,292)])
box(305,210,98,52,'Stride-2 Conv\nConcat\nC2fGhost / LSKA')
box(305,117,98,52,'Stride-2 Conv\nConcat\nC2fGhost / LSKA')
arrow([(240,292),(305,292),(305,236)])
arrow([(240,210),(256,210)])
arrow([(305,184),(305,143)])
arrow([(114,100),(128,100),(128,70),(305,70),(305,91)])
for y,label,start in [(292,'P3 / stride 8',240),(210,'P4 / stride 16',354),(117,'P5 / stride 32',354)]:
    box(425,y,88,42,'LSCD-Head\n'+label,'head');arrow([(start,y),(381,y)])
text(245,27,'LSCD convolutions are shared across the three scales.',11)
# Panel B: preserve ARM taps, adapted top-down fusion, PAN group and WT outputs.
x=510
frame(x,'(b) YOLO-RD reimplementation',[(57,104,'Backbone'),(194,142,'Fusion'),(319,82,'PAN'),(425,100,'Head')])
box(x+57,350,92,25,'640 x 640 input','conv')
box(x+57,292,92,40,'Conv / C2f\nP3 (stride 8)')
box(x+57,210,92,52,'Conv / SOM\nC2f\nP4 (stride 16)','att')
box(x+57,117,92,64,'Conv / SOM\nC2f / SPPF\nP5 (stride 32)','att')
for a,b in [(337,312),(272,236),(184,149)]:arrow([(x+57,a),(x+57,b)])
for y,label in [(292,'M2'),(210,'M3'),(117,'M5')]:
    lines='ARM\n'+('Upsample / Concat\n1 x 1 Conv / '+label if y!=117 else label)
    box(x+194,y,124,60 if y!=117 else 38,lines,'att');arrow([(x+103,y),(x+132,y)])
arrow([(x+194,136),(x+194,180)])
arrow([(x+194,240),(x+194,262)])
box(x+319,210,68,230,'Top-down\nand\nbottom-up\nfeature\nfusion','feat')
for y in [292,210,117]:
    arrow([(x+256,y),(x+285,y)])
    box(x+425,y,88,42,'WT-Head\nP'+str({292:3,210:4,117:5}[y]),'head');arrow([(x+353,y),(x+381,y)])
text(x+245,27,'Fusion uses Upsample / Concat / 1 x 1 Conv in this study.',11)
C.save()
print(OUT)
