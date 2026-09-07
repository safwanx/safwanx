"""Create static figures from reported results; no synthetic model outputs.

Usage: python scripts/build_static_research.py PATH_TO_CROWD_PROJECT
Requires matplotlib and Pillow. Source case CSV and JHU image stay in the research project.
"""
import csv
from pathlib import Path
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image

OUT=Path(__file__).resolve().parents[1]/'assets'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'text.color':'#243a40','axes.labelcolor':'#243a40','xtick.color':'#53676c'})
PAPER='#f5f7f3'

# Final-model development-set results from Table 3 of the TWASEL manuscript.
fig=plt.figure(figsize=(10,3.3),dpi=160,facecolor=PAPER)
fig.text(.045,.88,'TWASEL: decoding makes a difference',fontsize=18,weight='bold')
fig.text(.045,.78,'Same final model · Isharah development set · word error rate (lower is better)',fontsize=10.5,color='#53676c')
ax=fig.add_axes([.24,.23,.64,.40],facecolor=PAPER)
ax.barh([1,0],[20.42,11.85],height=.43,color=['#91a7aa','#377c71'])
ax.set_yticks([1,0],['CTC greedy','AR beam search'])
ax.set_xlim(0,25); ax.set_xticks([0,5,10,15,20,25],['0%','5%','10%','15%','20%','25%'])
ax.tick_params(axis='both',length=0,pad=10)
ax.spines[['top','right','left','bottom']].set_visible(False)
for y,v in [(1,20.42),(0,11.85)]: ax.text(v+.45,y,f'{v:.2f}%',va='center',fontsize=12,weight='bold')
fig.text(.045,.07,'Held-out test result: 16.62% WER with AR beam search.',fontsize=11)
fig.savefig(OUT/'twasel-results.png',facecolor=PAPER); plt.close(fig)

root=Path(sys.argv[1])
source=root/'Are-Crowd-Counts-Reliable/findings/tables/visual_failure_cases.csv'
rows=list(csv.DictReader(source.open(encoding='utf-8')))
cases=[next(r for r in rows if r['image_id']=='0814' and r['model']==model) for model in ['steerer_jhu','mpcount_qnrf_on_jhu']]
keys=['image_id','dataset','split','model','gt_count','pred_count','abs_error','predicted_risk','risk_percentile']
with (OUT/'crowd-case-values.csv').open('w',newline='',encoding='utf-8') as f:
    writer=csv.DictWriter(f,fieldnames=keys); writer.writeheader(); writer.writerows({k:r[k] for k in keys} for r in cases)
fig=plt.figure(figsize=(10,4.3),dpi=160,facecolor=PAPER)
fig.text(.035,.90,'Same image. Two missed counts.',fontsize=18,weight='bold')
ax=fig.add_axes([.025,.06,.29,.75]); ax.imshow(Image.open(root/'JHU/test/images/0814.jpg')); ax.axis('off')
fig.text(.335,.77,'JHU-CROWD++ / image 0814 / snow',fontsize=10,color='#53676c')
fig.text(.335,.67,'8,994 people annotated',fontsize=17,weight='bold')
for x,r,title,subtitle in zip([.335,.655],cases,['STEERER','MPCount'],['JHU evaluation','QNRF → JHU transfer']):
    fig.text(x,.535,title,fontsize=14,weight='bold')
    fig.text(x,.475,subtitle,fontsize=10,color='#53676c')
    fig.text(x,.36,f"Predicted: {float(r['pred_count']):,.1f}",fontsize=12)
    fig.text(x,.285,f"Absolute error: {float(r['abs_error']):,.1f}",fontsize=11)
    fig.text(x,.21,f"Risk percentile: {100*float(r['risk_percentile']):.1f}%",fontsize=11,weight='bold',color='#377c71')
fig.text(.335,.075,'Risk percentiles are within each evaluation setting.',fontsize=9,color='#53676c')
fig.text(.335,.035,'Lower percentile = ranked as less risky. Not a confidence probability.',fontsize=9,color='#53676c')
fig.savefig(OUT/'crowd-snow-case.png',facecolor=PAPER); plt.close(fig)
print('Saved two static figures and the source case values.')
