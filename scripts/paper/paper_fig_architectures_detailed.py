"""Detailed layer-level diagrams of local nano-scale YAMLs (no model inference).

Layer IDs, edges, channels and depth-scaled repeats are derived from YAML and
local parse_model rules. Multi-scale detection is drawn as three branches of one
head. Internal module operations remain encapsulated as in source Fig. 2.
"""
from pathlib import Path
import math
import yaml
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
ROOT=Path(__file__).resolve().parents[2]
for name,file in [('Diagram','LiberationSans-Regular.ttf'),('DiagramBold','LiberationSans-Bold.ttf')]:
 pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/liberation-sans-fonts/'+file))
PALETTE={'Conv':'#fae4ad','C2f':'#b9dce8','C2fGhost':'#92c7df','BoT':'#a6d8eb','LSKA':'#c1e2ae','SOM':'#efc2d2','ARM':'#c2d7f1','Concat':'#f4c5a2','nn.Upsample':'#f5efaa','SPPF':'#d6c9e8'}
def draw(model):
 data=yaml.safe_load((ROOT/'code/models'/model).read_text());rd='yolo-rd' in model
 name='YOLO-RD' if rd else 'YOLOv8-PD';layers=data['backbone']+data['head'];depth,width,cap=data['scales']['n'];N=len(layers)-1
 if rd:
  W,H=1240,1250;coords={i:(95,1110-70*i) for i in range(12)}
  coords.update({12:(300,830),13:(300,620),14:(300,340)})
  coords.update({i:(490,410+70*(i-15)) for i in range(15,21)})
  coords.update({i:(700,410+70*(i-21)) for i in range(21,27)})
  coords.update({i:(910,690-70*(i-27)) for i in range(27,33)})
  groups=[(15,175,'SOM-Backbone'),(215,385,'ARM'),(405,575,'Fusion adaptation'),(615,995,'PAN neck'),(1030,1220,'WT-Head')]
  heads=[(26,750),(29,540),(32,330)];hx=1125
 else:
  W,H=960,1220;coords={i:(95,1080-70*i) for i in range(12)}
  coords.update({i:(365,380+70*(i-12)) for i in range(12,20)})
  coords.update({i:(615,800-70*(i-20)) for i in range(20,28)})
  groups=[(15,175,'Backbone'),(270,710,'Neck'),(755,945,'LSCD-Head')]
  heads=[(19,870),(23,590),(27,310)];hx=850
 out=ROOT/'latex/IEEE-Conference/gambar'/('architecture_rd_detailed.pdf' if rd else 'architecture_pd_detailed.pdf')
 c=canvas.Canvas(str(out),pagesize=(W,H-150));c.setTitle(name+' - implemented architecture');c.translate(0,-95)
 def txt(x,y,t,size=12,bold=False):
  c.setFillColor(HexColor('#222222'));c.setFont('DiagramBold' if bold else 'Diagram',size);c.drawCentredString(x,y,t,mode=0)
 for a,b,label in groups:
  c.setStrokeColor(HexColor('#aaaaaa'));c.setLineWidth(.8);c.setDash(4,3);c.roundRect(a,105,b-a,H-178,5,stroke=1,fill=0);c.setDash();c.setFillColor(HexColor('#ffffff')); c.rect((a+b)/2-pdfmetrics.stringWidth(label,'DiagramBold',14)/2-5,H-83,pdfmetrics.stringWidth(label,'DiagramBold',14)+10,18,stroke=0,fill=1); txt((a+b)/2,H-80,label,14,True)
 chans=[];sizes=[];reps=[];edges=[]
 for i,(f,n,m,args) in enumerate(layers):
  src=[i-1 if j==-1 else j for j in (f if isinstance(f,list) else [f])];edges.extend((j,i) for j in src if j>=0)
  r=max(round(n*depth),1) if n>1 else n;reps.append(r)
  if m in PALETTE and m not in ['Concat','nn.Upsample']:
   ch=math.ceil(min(args[0],cap)*width/8)*8
  elif m=='Concat':ch=sum(chans[j] for j in src)
  elif m=='nn.Upsample':ch=chans[src[0]]
  else:ch=0
  if m=='Concat':
   assert len({sizes[j] for j in src}) == 1, (i, src)
  side=640 if i==0 else sizes[src[0]]
  if m=='Conv' and len(args)>2:side//=args[2]
  if m=='nn.Upsample':side*=2
  chans.append(ch);sizes.append(side)
 def path(points):
  # White casing makes crossing routes distinct, without junction symbols.
  for color,lw in [('#ffffff',3.6),('#555555',1.05)]:
   c.setStrokeColor(HexColor(color));c.setLineWidth(lw);p=c.beginPath();p.moveTo(*points[0])
   for pt in points[1:]:p.lineTo(*pt)
   c.drawPath(p)
  x,y=points[-1];px,py=points[-2];a=math.atan2(y-py,x-px);p=c.beginPath();p.moveTo(x,y)
  for d in [-.45,.45]:p.lineTo(x-6*math.cos(a+d),y-6*math.sin(a+d))
  p.close();c.setFillColor(HexColor('#555555'));c.drawPath(p,stroke=0,fill=1)
 bw,bh=134,40
 def connect(a,b):
  x,y=coords[a];X,Y=coords[b]
  if x==X:
   sign=1 if Y>y else -1
   if abs(Y-y)<=75:path([(x,y+sign*20),(X,Y-sign*20)])
   else:
    lane=x+83+(a%3)*8;path([(x+67,y),(lane,y),(lane,Y),(X+67,Y)])
  else:
   mid=(x+X)/2
   if abs(Y-y)<1:path([(x+67,y),(X-67,Y)])
   else:path([(x+67,y),(mid,y),(mid,Y),(X-67,Y)])
 for a,b in edges:
  if b!=N:connect(a,b)
 for a,y in heads:
  coords[N]=(hx,y);connect(a,N)
 for i,(x,y) in coords.items():
  if i==N:continue
  f,n,m,args=layers[i];c.setStrokeColor(HexColor('#555555'));c.setLineWidth(.8);c.setFillColor(HexColor(PALETTE.get(m,'#eeeeee')));c.roundRect(x-67,y-20,134,40,4,stroke=1,fill=1)
  title=m.replace('nn.','')
  if m=='Conv':title+=f' {args[1] if len(args)>1 else 1}x{args[1] if len(args)>1 else 1}'
  if reps[i]>1:title+=f' x{reps[i]}'
  txt(x,y+3,title,13,True);txt(x,y-13,f'[{i}]  {sizes[i]} x {sizes[i]} x {chans[i]}',10)
 # Input is separate from layer 0.
 x,y=coords[0];txt(x,y+42,'640 x 640 x 3',11);path([(x,y+36),(x,y+20)])
 for k,(a,y) in enumerate(heads):
  c.setStrokeColor(HexColor('#555555'));c.setFillColor(HexColor('#f4c5a2'));c.roundRect(hx-77,y-26,154,52,4,stroke=1,fill=1)
  txt(hx,y+8,'WT-Head' if rd else 'LSCD-Head',13,True);txt(hx,y-8,f'P{k+3}: stride {8*2**k}',11);txt(hx,y-21,'box regression + classes',10)
 c.save();print(out)
for model in ['yolov8-pd.yaml','yolo-rd.yaml']:draw(model)
