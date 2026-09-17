"""Editable FAR graphical abstract: measured evidence and a checked toy example.

The two supplied Visio documents inform the three-column, layered composition.
Every datum is from this project; all geometry is native Visio geometry.
"""
import json
from pathlib import Path
import numpy as np
import pandas as pd
import fitz
from analyze_final import ROOT, RES, INDEX

W,H=16.,9.0
INK='#302A32'; BORDER='#AFA6AA'; GRAY='#F3F0EE'
WINE='#973B59'; ROSE='#F7E8ED'; ROSE_HEAD='#EBC5D2'
INDIGO='#414B87'; LILAC='#EDF0FA'; LILAC_HEAD='#CDD3ED'
GOLD='#A27722'; SAND='#FBF4E3'; SAND_HEAD='#EDDAA8'
WHITE='#FFFFFF'

def build_overview():
    shapes=[]
    fonts={b:fitz.Font(fontfile=str(Path('C:/Windows/Fonts')/('timesbd.ttf' if b else 'times.ttf')))
           for b in [False,True]}
    def box(x,y,w,h,t='',fill=WHITE,line=BORDER,size=20,bold=False,color=INK,kind='box',align=1):
        # Visio text boxes do not clip overflowing text. Fit each intended line
        # with the actual Times font metrics, retaining native editable text.
        if t:
            rows=t.split('\n');font=fonts[bool(bold)]
            widest=max(font.text_length(row,fontsize=1) for row in rows)
            size=min(size,(w*72-4)/max(widest,.1),(h*72-2.2)/(1.18*len(rows)))
        shapes.append(dict(kind=kind,x=x,y=H-y-h,w=w,h=h,text=t,fill=fill,line=line,
                           size=size,bold=bool(bold),color=color,align=align))
    def text(x,y,w,h,t,size=20,bold=False,color=INK,align=1):
        box(x,y,w,h,t,size=size,bold=bold,color=color,kind='text',align=align)
    def line(x,y,x2,y2,color=INK,arrow=True,weight=1.3,dash=False):
        shapes.append(dict(kind='line',x=x,y=H-y,x2=x2,y2=H-y2,color=color,arrow=arrow,weight=weight,dash=dash))
    def poly(points,fill,linecolor=None,transparency=0):
        shapes.append(dict(kind='poly',points=[[x,H-y] for x,y in points],fill=fill,line=linecolor or fill,stroke=linecolor is not None,transparency=transparency))
    def panel(x,y,w,h,title,fill,head):
        box(x,y,w,h,fill=fill,line=WHITE)
        box(x,y,w,.35,title,fill=head,line=head,size=22,bold=True)
    def cellrow(x,y,vals,colors=None,width=.69,height=.38):
        for i,v in enumerate(vals):
            box(x+i*width,y,width-.025,height,str(v),fill=(colors[i] if colors else WHITE),line=WHITE,size=20)
    # Verified worked example: zero-based ranks, timestamps in arbitrary units.
    q=np.array([8,12,15,19,24,28]);old=np.array([4,10,10,18,18,27]);delta=np.array([11,13,14,23,26])
    idx=np.searchsorted(delta,q,side='right')-1
    result=np.maximum(old,np.where(idx>=0,delta[np.maximum(idx,0)],-999))
    assert result.tolist()==[4,11,14,18,23,27]
    assert np.searchsorted(q,11)==1 and np.searchsorted(old,26)==5
    data=pd.read_json(RES/'maintenance_full.jsonl',lines=True)
    p=data.groupby(INDEX+['method']).seconds.median().unstack()

    # Three-column frame and paired central title bands match the references.
    box(.04,.04,15.92,8.9,line=BORDER)
    box(3.49,.14,8.78,.39,'Fixed probes + late insertions: exact ASOF maintenance',fill=INK,line=INK,color=WHITE,size=24,bold=True)
    box(3.49,.59,8.78,.34,'FAR: use ordered answers to bound and route repair',fill=LILAC_HEAD,line=LILAC_HEAD,size=23,bold=True)

    panel(.16,3.35,3.12,1.38,'One equality-key group',GRAY,SAND_HEAD)
    text(.3,3.81,2.83,.23,'q = [8, 12, 15, 19, 24, 28]',18)
    text(.3,4.09,2.83,.23,'y = [4, 10, 10, 18, 18, 27]',18)
    text(.3,4.40,2.83,.23,'D = [11, 13, 14, 23, 26]',17,color=WINE)
    # Arrow from input state into the first method stage.
    line(3.29,3.73,3.48,3.73,INDIGO)

    # Main layer 1: exact conservative cover, with index and state rows.
    panel(3.49,1.08,5.94,3.07,'1  Bound repair using the cached answers',LILAC,LILAC_HEAD)
    text(3.70,1.55,5.52,.29,'a = min D = 11       z = max D = 26',21,True,color=INDIGO)
    text(3.62,1.98,.47,.31,'q',22,True)
    text(3.62,2.46,.47,.31,'y',22,True)
    active=[GRAY,ROSE,ROSE,ROSE,ROSE,GRAY]
    cellrow(4.23,1.94,q,active);cellrow(4.23,2.42,old,active)
    for i in range(6):text(4.23+i*.69,1.78,.66,.14,str(i),13,color=INDIGO)
    line(4.90,2.91,7.66,2.91,WINE,False,2.0)
    line(4.90,2.80,4.90,2.92,WINE,False,2.0);line(7.66,2.80,7.66,2.92,WINE,False,2.0)
    text(4.20,3.08,4.77,.34,'L = lb(q, a) = 1     H = lb(y, z) = 5',21,True)
    text(3.69,3.58,5.54,.35,'Only [L, H) can change; ranks are zero-based',19,color=INDIGO)

    # Main layer 2: show reduction and the two separate stopping certificates.
    panel(3.49,4.32,5.94,2.73,'Sparse branch: compact events at probe frontiers',ROSE,ROSE_HEAD)
    for j,t in enumerate([11,13,14,23,26]):box(3.76+j*1.06,4.90,.82,.39,str(t),fill=WHITE,line=ROSE_HEAD,size=21)
    text(4.79,5.34,1.90,.24,'same first probe: 15',17,color=WINE)
    line(5.23,5.63,5.73,5.91,WINE);line(6.29,5.63,5.83,5.91,WINE)
    box(5.36,5.95,.90,.41,'14',fill=WINE,line=WINE,size=22,color=WHITE,bold=True)
    text(3.72,5.64,1.37,.28,'Keep latest',19,True,color=WINE)
    text(6.63,5.61,2.50,.38,'Skip 26: its frontier\nlies beyond the cover',17,color=INDIGO)
    text(3.69,6.54,5.52,.29,'Stop at the next frontier or a dominating old answer',18,True)

    # Tall companion column: mechanism work and precise update algebra.
    panel(9.59,1.08,2.68,5.97,'Exact repair',SAND,SAND_HEAD)
    text(9.76,1.61,2.34,.35,'New answer at q',21,True)
    text(9.74,2.08,2.38,.59,'max{y(q),\npred(D, q)}',24,True,color=WINE)
    line(10.93,2.84,10.93,3.07,GOLD)
    text(9.78,3.18,2.3,.57,'Ordered answers\nsummarize old history',20,True)
    box(9.82,4.03,2.22,.70,'No retained\nreference-history index',fill=WHITE,line=SAND_HEAD,size=19)
    text(9.78,5.04,2.30,.65,'One write per\nchanged answer',23,True,color=INDIGO)
    text(9.79,6.03,2.29,.29,'c changes ⇒ c writes',20)
    text(9.76,6.52,2.34,.29,'Fixed probes; insertions only',17)

    # Bottom central band: split and rejoin, with both branches named explicitly.
    panel(3.49,7.23,8.78,1.22,'2  Route by candidate span: s = H − L, b = |D|',GRAY,SAND_HEAD)
    box(3.71,7.80,1.56,.41,'s ≤ 8b ?',fill=WHITE,line=GOLD,size=21,bold=True)
    line(5.30,7.89,5.79,7.80,INDIGO);line(5.30,8.13,5.79,8.22,WINE)
    text(5.31,7.65,.4,.20,'yes',14,color=INDIGO);text(5.31,8.23,.4,.18,'no',14,color=WINE)
    box(5.85,7.65,2.36,.31,'Bounded merge',fill=LILAC,line=LILAC_HEAD,size=19)
    box(5.85,8.09,2.36,.31,'Sparse frontier repair',fill=ROSE,line=ROSE_HEAD,size=19)
    line(8.24,7.80,8.72,7.99,INDIGO);line(8.24,8.24,8.72,8.04,WINE)
    box(8.82,7.77,3.19,.45,'Same exact updated answers',fill=WHITE,line=GOLD,size=20,bold=True)

    # Right: illustrative output followed by actual distribution, no foreign data.
    panel(12.47,.14,3.37,3.96,'Exact maintained output',GRAY,LILAC_HEAD)
    text(12.65,.63,3.0,.25,'Worked example · 3 changed answers',18,True)
    for j,label in enumerate(['Probe','Old','New']):text(12.67+j*1.01,1.08,.87,.25,label,19,True)
    for i,(a,b,c) in enumerate(zip(q,old,result)):
        yy=1.50+i*.35
        for j,t in enumerate([a,b,c]):
            changed=j==2 and b!=c
            box(12.69+j*1.01,yy,.85,.30,str(t),fill=WINE if changed else WHITE,line=WHITE,
                color=WHITE if changed else INK,size=19,bold=changed)
    text(12.64,3.69,3.03,.24,'Illustrative timestamps, not measurements',16)
    from overview_charts import draw_charts
    draw_charts(p,box,text,line,poly,panel,[INK,BORDER,WINE,INDIGO,GOLD,ROSE_HEAD,LILAC_HEAD])
    # Underbraces visually group the three roles as in the supplied references.
    for x,w,label in [(.16,3.12,'Inputs and measured evidence'),(3.49,8.78,'Answer bounds → probe frontiers → adaptive traversal'),(12.47,3.37,'Outputs and evaluation')]:
        line(x,8.55,x,8.68,INK,False,.8);line(x,8.68,x+w,8.68,INK,False,.8);line(x+w,8.68,x+w,8.55,INK,False,.8)
        text(x,8.71,w,.22,label,18,True)

    out=ROOT/'paper'/'figures'
    spec=dict(width=W,height=H,shapes=shapes,palette=dict(ink=INK,indigo=INDIGO,wine=WINE,gold=GOLD))
    (out/'overview_shapes.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2),encoding='utf8')
    record=dict(reference_files=['dasfaa2027_lazy_topk_20260913/paper/figures/revision_overview_latest_editable.vsdx',
        'icme2027_graph_risk_20260913/figures/visio/output/method_flowchart_reference_matched.vsdx'],
        borrowed='three-column layout, stacked method bands, compact measured panels, grouped bottom braces',
        palette=spec['palette'],foreign_results_used=False,source='results/maintenance_full.jsonl',
        example=dict(probes=q.tolist(),old=old.tolist(),delta=delta.tolist(),new=result.tolist(),cover=[1,5]),
        scientific_panels='qa/fig1_scientific_panels.json',shape_count=len(shapes))
    (ROOT/'qa'/'fig1_redesign.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf8')
    print(f'FAR overview: {len(shapes)} native shapes; all example results checked')

if __name__=='__main__':build_overview()
