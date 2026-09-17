"""Three descriptive, data-driven panels drawn as native Visio primitives.

Input is the measured per-scenario median runtime table, not demonstration data.
No inference tests or significance markers are attached to these plots.
"""
import json,math
import numpy as np
from scipy.cluster.hierarchy import linkage,dendrogram
from scipy.spatial.distance import squareform
from scipy.stats import gaussian_kde
from analyze_final import ROOT,DATASETS,gm
from runtime_profiles import PROFILE_METHODS, centered_log_profiles

def draw_charts(p,box,text,line,poly,panel,colors):
    ink,border,wine,indigo,gold,rose,lilac=colors
    white='#FFFFFF';gray='#706771';marks=[indigo,gold,wine,gray]
    evidence={};rects={}
    # Correlation of relative profiles removes the shared scale of each scenario.
    methods=PROFILE_METHODS
    codes=dict(zip(methods,['F','E','M','T','B','S']))
    centered=centered_log_profiles(p)
    corr=centered.corr();dist=np.clip(1-corr.to_numpy(),0,2);np.fill_diagonal(dist,0)
    tree=linkage(squareform(dist,checks=False),method='average')
    dend=dendrogram(tree,no_plot=True);order=dend['leaves'];ordered=[methods[i] for i in order]
    panel(.16,.14,3.12,3.14,'Clustered runtime profiles',white,rose)
    text(.25,.55,2.91,.20,'Pearson r · row-centered log times',15)
    x0,y0,cell=1.00,1.06,.25
    maxh=max(max(x) for x in dend['dcoord'])
    for xs,ys in zip(dend['icoord'],dend['dcoord']):
        pts=[(x0+v/10*cell,y0-.07-z/maxh*.22) for v,z in zip(xs,ys)]
        for a,b in zip(pts,pts[1:]):line(*a,*b,indigo,False,.7)
    def shade(v):
        end=indigo if v>=0 else wine;a=abs(float(v))*.86
        return '#'+''.join(f'{round(255*(1-a)+int(end[i:i+2],16)*a):02x}' for i in [1,3,5])
    for i,m in enumerate(ordered):
        text(.67,y0+i*cell,.25,cell,codes[m],16,True)
        text(x0+i*cell,y0+6*cell+.05,cell,.20,codes[m],16,True)
        for j,n in enumerate(ordered):
            v=float(corr.loc[m,n])
            box(x0+j*cell,y0+i*cell,cell-.008,cell-.008,f'{v:.1f}',fill=shade(v),line=white,
                size=12,color=white if abs(v)>.7 else ink)
    for i in range(28):
        v=1-2*i/27;box(2.79,y0+i*(6*cell/28),.14,6*cell/28+.001,fill=shade(v),line=shade(v))
    for v,label in [(1,'1'),(0,'0'),(-1,'−1')]:text(2.96,y0+(1-v)/2*6*cell-.08,.23,.16,label,12)
    text(.26,2.83,2.92,.21,'F: FAR  E: Desc.  M: Merge  T: Trace',13)
    text(.26,3.05,2.92,.21,'B: bounded merge   S: bounded frontier',13)
    evidence['clustered_profile']=dict(methods=methods,order=ordered,pearson=corr.to_dict(),
        transform='natural log of median runtime; subtract each scenario row mean across six methods',
        clustering='average linkage of 1 minus Pearson correlation',scenarios=len(p),significance_tests=False)
    rects['profile_correlation']=[.16,.14,3.12,3.14]

    # Radar: same 0–4.5 radial scale for all datasets; six actual workload regimes.
    panel(.16,4.90,3.12,3.55,'Workload performance radar',white,lilac)
    text(.28,5.33,2.88,.22,'Descending repair / FAR · geometric means',15)
    cx,cy,radius=1.74,6.90,.87;limit=4.5
    regimes=[(.01,'burst'),(.01,'uniform'),(.1,'burst'),(.1,'uniform'),(1.,'burst'),(1.,'uniform')]
    labels=['1% B','1% U','10% B','10% U','100% B','100% U']
    angles=np.linspace(-np.pi/2,3*np.pi/2,6,endpoint=False)
    def point(a,v):return cx+radius*v/limit*np.cos(a),cy+radius*v/limit*np.sin(a)
    for level in [1,2,3,4]:
        pts=[point(a,level) for a in angles]
        for a,b in zip(pts,pts[1:]+pts[:1]):line(*a,*b,border,False,.6 if level!=1 else 1.2,level==1)
    for a,label in zip(angles,labels):
        line(cx,cy,*point(a,limit),border,False,.5)
        x,y=point(a,5.05);text(x-.35,y-.11,.70,.22,label,14)
    for level in [1,2,4]:text(cx+.05,cy-radius*level/limit-.07,.18,.14,str(level),10,color=gray)
    profile=p.event_descending/p.far;summary={}
    for name,color in zip(DATASETS,marks):
        v=[gm(profile.loc[name].xs((frac,pat),level=('qfraction','pattern'))) for frac,pat in regimes]
        assert max(v)<limit
        summary[name]=v;pts=[point(a,value) for a,value in zip(angles,v)]
        poly(pts+[pts[0]],color,color,.90)
        for x,y in pts:box(x-.025,y-.025,.05,.05,fill=color,line=color,kind='ellipse')
    for i,(label,color) in enumerate(zip(['Yellow','Green','Bike Jan','Bike Jul'],marks)):
        x=.33+(i%2)*1.48;y=8.11+(i//2)*.19
        line(x,y+.05,x+.18,y+.05,color,False,1.8);text(x+.22,y-.045,1.00,.19,label,13,align=0)
    text(.34,5.59,2.78,.18,'B: burst   U: uniform   dashed ring: 1×',12)
    evidence['regime_radar']=dict(regimes=regimes,ratios=summary,radial_limits=[0,limit],
        statistic='geometric mean of descending/FAR median runtime ratios across batch sizes and seeds')
    rects['regime_radar']=[.16,4.90,3.12,3.55]

    # Rainclouds: half KDE in log2 space, every measured case, median and IQR.
    panel(12.47,4.28,3.37,4.17,'Speedup rainclouds',white,rose)
    text(12.61,4.74,3.08,.22,'Descending event repair / FAR',17)
    text(12.63,5.01,3.04,.19,'72 scenario-seed medians per dataset',14)
    top,bottom=5.36,7.53
    def sy(v):return bottom-(v+1)/5*(bottom-top)
    for val in [-1,0,1,2,3,4]:
        yy=sy(val);line(12.85,yy,15.70,yy,border,False,.5,val==0)
        text(12.49,yy-.07,.31,.15,f'{2.**val:g}',12)
    distributions={};rng=np.random.default_rng(20260917)
    for i,(name,color) in enumerate(zip(DATASETS,marks)):
        values=profile.loc[name].to_numpy();a=np.log2(values);x=13.12+i*.72
        domain=np.linspace(a.min(),a.max(),64);density=gaussian_kde(a,bw_method='scott')(domain)
        density=.26*density/density.max()
        points=[(x-.03,sy(domain[0]))]+[(x-.03-w,sy(t)) for w,t in zip(density,domain)]+[(x-.03,sy(domain[-1]))]
        poly(points+[points[0]],color,color,.65)
        jitter=rng.uniform(.065,.23,len(a))
        for z,dx in zip(a,jitter):box(x+dx-.011,sy(z)-.011,.022,.022,fill=color,line=color,kind='ellipse')
        lo,q1,med,q3,hi=np.quantile(a,[0,.25,.5,.75,1])
        line(x,sy(lo),x,sy(hi),ink,False,.7)
        box(x-.023,sy(q3),.046,sy(q1)-sy(q3),fill=ink,line=ink)
        box(x-.028,sy(med)-.028,.056,.056,fill=white,line=ink,kind='ellipse')
        text(x-.25,7.63,.53,.22,['Yellow','Green','Jan','Jul'][i],13)
        distributions[name]=dict(n=len(a),ratios=values.tolist(),log2_kde_grid=domain.tolist(),
            display_normalized_kde_width=density.tolist(),ratio_quantiles=np.quantile(values,[0,.25,.5,.75,1]).tolist())
    text(12.58,7.98,3.16,.18,'Density + all points + median / IQR',14)
    text(12.59,8.22,3.14,.17,'Log₂ scale; jitter is visual only',13)
    evidence['raincloud']=dict(datasets=distributions,kde='Gaussian KDE on log2 ratios, Scott bandwidth; truncated to observed min/max; peak width normalized per dataset',
        jitter_seed=20260917,significance_tests=False)
    rects['speedup_raincloud']=[12.47,4.28,3.37,4.17]
    evidence['source']='results/maintenance_full.jsonl';evidence['aggregation']='median of 7 repetitions per scenario-seed and method'
    evidence['panel_rectangles_top_origin_inches']=rects
    (ROOT/'qa/fig1_scientific_panels.json').write_text(json.dumps(evidence,indent=2),encoding='utf8')
    return evidence
