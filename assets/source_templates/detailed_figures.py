"""Expanded measured-data analyses for the manuscript, with complete numeric provenance."""
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.spatial.distance import squareform
from scipy.stats import gaussian_kde

from analyze_final import ROOT, INDEX, DATASETS, gm
from runtime_profiles import PROFILE_METHODS, centered_log_profiles

OUT = ROOT / 'paper/figures'
NAMES = ['Yellow taxi', 'Green taxi', 'Bike January', 'Bike July']
SHORT = ['Yellow', 'Green', 'Bike Jan', 'Bike Jul']
COLORS = ['#414B87', '#A27722', '#973B59', '#706771']
INK = '#302A32'
BASELINES = [('event_descending', 'Descending event repair', COLORS[0]),
             ('delta_merge', 'Delta merge', COLORS[2])]
REGIMES = [(.01, 'burst'), (.01, 'uniform'), (.1, 'burst'), (.1, 'uniform'),
           (1., 'burst'), (1., 'uniform')]
plt.rcParams.update({'font.family': 'serif', 'font.serif': ['Times New Roman'],
    'font.size': 8, 'axes.titlesize': 9, 'axes.labelsize': 8,
    'xtick.labelsize': 7, 'ytick.labelsize': 7, 'text.color': INK,
    'axes.labelcolor': INK, 'pdf.fonttype': 42, 'svg.fonttype': 'none',
    'axes.spines.top': False, 'axes.spines.right': False})


def save(fig, name):
    for ext in ['pdf', 'svg', 'png']:
        fig.savefig(OUT / f'{name}.{ext}', dpi=320, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def radar(p):
    fig, axes = plt.subplots(2, 2, figsize=(5.45, 3.85), subplot_kw={'projection': 'polar'})
    fig.subplots_adjust(left=.08, right=.95, top=.83, bottom=.09, hspace=.64, wspace=.45)
    theta = np.linspace(0, 2*np.pi, 6, endpoint=False)
    closed = np.r_[theta, theta[0]]
    evidence = {}
    for i, (ax, dataset, name) in enumerate(zip(axes.flat, DATASETS, NAMES)):
        ax.set_theta_offset(np.pi/2)
        ax.set_theta_direction(-1)
        ax.set_ylim(0, 4)
        ax.set_yticks([1, 2, 3, 4], ['1', '2', '4', '8'])
        ax.set_rlabel_position(15)
        ax.tick_params(axis='y', labelsize=6.5, pad=0)
        ax.set_xticks(theta, ['1% B', '1% U', '10% B', '10% U', '100% B', '100% U'])
        ax.tick_params(axis='x', pad=1)
        ax.spines['polar'].set_color('#D1CBCF')
        ax.grid(color='#C8C2C7', lw=.55)
        ring = np.linspace(0, 2*np.pi, 200)
        ax.fill_between(ring, 0, 1, color='#F3F0EE', zorder=0)
        ax.plot(ring, np.ones_like(ring), '--', color=INK, lw=.9)
        ax.set_title(f'({chr(97+i)}) {name}', pad=19, weight='bold')
        evidence[dataset] = {}
        for j, (method, label, color) in enumerate(BASELINES):
            ratio = p.loc[dataset, method] / p.loc[dataset, 'far']
            vals = [gm(ratio.xs((f, b), level=('qfraction', 'pattern'))) for f, b in REGIMES]
            assert min(vals) >= .5 and max(vals) <= 8
            r = np.log2(vals) + 1
            ax.plot(closed, np.r_[r, r[0]], color=color, lw=1.3, marker=['o', 's'][j],
                    ms=3, linestyle=['-', '-.'][j], label=label)
            ax.fill(closed, np.r_[r, r[0]], color=color, alpha=.10)
            evidence[dataset][method] = vals
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', ncol=2, frameon=False, bbox_to_anchor=(.51, 1.025))
    fig.text(.51, .954, 'Baseline / FAR   |   log₂ radial scale: 0.5–8×   |   dashed ring: 1×',
             ha='center', fontsize=7.5)
    fig.text(.51, .007, 'B: burst    U: uniform    |    12 scenario-seed ratios per vertex', ha='center', fontsize=7.5)
    save(fig, 'workload_regimes')
    return dict(regimes=REGIMES, n_per_vertex=12, ratios=evidence, radial_limits=[.5, 8])


def raincloud(p):
    fig, axes = plt.subplots(1, 2, figsize=(5.25, 3.35), sharey=True)
    fig.subplots_adjust(left=.10, right=.98, bottom=.21, top=.86, wspace=.15)
    rng = np.random.default_rng(20260917)
    evidence = {}
    for panel, (ax, (method, label, _)) in enumerate(zip(axes, BASELINES)):
        evidence[method] = {}
        ax.set_title(f'({chr(97+panel)}) {label}', fontweight='bold', pad=18)
        for i, (dataset, color) in enumerate(zip(DATASETS, COLORS)):
            ratio = (p.loc[dataset, method] / p.loc[dataset, 'far']).to_numpy()
            vals = np.log2(ratio)
            domain = np.linspace(vals.min(), vals.max(), 180)
            density = gaussian_kde(vals, bw_method='scott')(domain)
            width = .36 * density / density.max()
            ax.fill_betweenx(domain, i-.08-width, i-.08, color=color, alpha=.27, lw=0)
            ax.plot(i-.08-width, domain, color=color, lw=1.1)
            ax.plot([i-.08, i-.08], [domain[0], domain[-1]], color=color, lw=.7)
            ax.scatter(i+rng.uniform(.075, .32, len(vals)), vals, s=5, color=color,
                       alpha=.78, edgecolors='none', zorder=3)
            lo, q1, med, q3, hi = np.quantile(vals, [0, .25, .5, .75, 1])
            ax.plot([i, i], [lo, hi], color=INK, lw=.8)
            ax.plot([i, i], [q1, q3], color=INK, lw=3.2, solid_capstyle='butt')
            ax.scatter(i, med, s=17, color='white', edgecolor=INK, lw=.65, zorder=5)
            wins, ties, losses = [int(np.sum(op(ratio, 1))) for op in [np.greater, np.equal, np.less]]
            evidence[method][dataset] = dict(n=len(vals), ratios=ratio.tolist(), gm=gm(ratio),
                wins=wins, ties=ties, losses=losses, quantiles=np.quantile(ratio, [0,.25,.5,.75,1]).tolist(),
                log2_kde_grid=domain.tolist(), normalized_density_width=width.tolist())
        ax.set_xlim(-.57, 3.45)
        ax.set_ylim(-1.12, 5.16)
        ax.set_yticks(np.arange(-1, 6), ['0.5', '1', '2', '4', '8', '16', '32'])
        ax.axhline(0, color=INK, ls='--', lw=.9)
        ax.grid(axis='y', color='#DAD5D8', lw=.5)
        ax.set_axisbelow(True)
        labels = [f'{short}\n{evidence[method][d]["gm"]:.2f}×\n'
                  f'{evidence[method][d]["wins"]}/{evidence[method][d]["ties"]}/{evidence[method][d]["losses"]}'
                  for short, d in zip(SHORT, DATASETS)]
        ax.set_xticks(range(4), labels)
        ax.tick_params(axis='x', length=0)
    axes[0].set_ylabel('Baseline / FAR (log₂ scale)')
    fig.text(.54, 1.02, '72 cases per dataset; all medians and slowdowns retained', ha='center', fontsize=7.5)
    fig.text(.53, -.052, 'Below each dataset: geometric mean; FAR wins / ties / losses', ha='center', fontsize=7.5)
    save(fig, 'speedup_distributions')
    return dict(baselines=evidence, kde='Gaussian, Scott bandwidth on log2 ratios; observed min/max support; peak-normalized width',
                seed=20260917, wins='strict baseline/FAR > 1; ties are exact equality of median times')


def correlations(p):
    centered = centered_log_profiles(p)
    corr = centered.corr()
    dist = np.clip(1-corr.to_numpy(), 0, 2)
    np.fill_diagonal(dist, 0)
    tree = linkage(squareform(dist, checks=False), method='average')
    order = dendrogram(tree, no_plot=True)['leaves']
    methods = [PROFILE_METHODS[i] for i in order]
    codes = dict(zip(PROFILE_METHODS, ['F', 'E', 'M', 'T', 'B', 'S']))
    fig = plt.figure(figsize=(5.25, 3.25))
    ax = fig.add_axes([.09, .24, .43, .54])
    dendax = fig.add_axes([.09, .80, .43, .10])
    dendrogram(tree, ax=dendax, no_labels=True, color_threshold=0, above_threshold_color=COLORS[0])
    dendax.axis('off')
    strip = fig.add_axes([.65, .30, .29, .48])
    cmap = LinearSegmentedColormap.from_list('wine_indigo', [COLORS[2], '#FFFFFF', COLORS[0]])
    def heat(axis, values, rows, cols):
        im = axis.imshow(values, cmap=cmap, vmin=-1, vmax=1, aspect='auto')
        axis.set_xticks(range(len(cols)), cols)
        axis.set_yticks(range(len(rows)), rows)
        axis.tick_params(length=0)
        axis.set_xticks(np.arange(-.5, len(cols)), minor=True)
        axis.set_yticks(np.arange(-.5, len(rows)), minor=True)
        axis.grid(which='minor', color='white', lw=1.8)
        axis.tick_params(which='minor', length=0)
        for (i,j), v in np.ndenumerate(values):
            axis.text(j, i, f'{v:.2f}', ha='center', va='center', fontsize=6.7,
                      color='white' if abs(v) > .68 else INK)
        for s in axis.spines.values():s.set_visible(False)
        return im
    im = heat(ax, corr.loc[methods, methods].to_numpy(), [codes[m] for m in methods], [codes[m] for m in methods])
    others = [m for m in methods if m != 'far']
    within = np.array([[centered.loc[d].corr().loc[m, 'far'] for m in others] for d in DATASETS])
    heat(strip, within, SHORT, [codes[m] for m in others])
    fig.text(.09, .96, '(a) Clustered method profiles', weight='bold', fontsize=9)
    fig.text(.61, .96, '(b) FAR within each dataset', weight='bold', fontsize=9)
    fig.text(.795, .835, '72 scenarios per row', ha='center', fontsize=7)
    cbax = fig.add_axes([.10, .135, .40, .024])
    cb = fig.colorbar(im, cax=cbax, orientation='horizontal', ticks=[-1, -.5, 0, .5, 1])
    cb.set_label('Pearson r (centered log runtimes)', fontsize=7, labelpad=1)
    fig.text(.65, .215, 'Shared color scale: −1 to 1', fontsize=7)
    fig.text(.52, -.052, 'F: FAR   E: descending   M: delta merge   T: Trace-Range\n'
             'B: bounded merge   S: bounded frontier', ha='center', fontsize=7.5)
    save(fig, 'runtime_structure')
    return dict(methods=PROFILE_METHODS, order=methods, pooled_pearson=corr.to_dict(),
                within_dataset_columns=others, within_dataset_far=dict(zip(DATASETS, within.tolist())),
                transform='natural log median runtimes centered by each scenario mean across six methods',
                clustering='average linkage on 1-r', scenarios=len(p))


def main():
    d = pd.read_json(ROOT / 'results/maintenance_full.jsonl', lines=True)
    assert len(d) == 30240 and d.correct.all()
    assert (d.groupby(INDEX+['method']).size() == 7).all()
    p = d.groupby(INDEX+['method']).seconds.median().unstack()
    assert len(p) == 288
    evidence = dict(source='results/maintenance_full.jsonl', aggregation='median of seven repeats per scenario-seed and method',
                    significance_tests=False, radar=radar(p), raincloud=raincloud(p), correlations=correlations(p))
    (ROOT/'qa/detailed_figure_provenance.json').write_text(json.dumps(evidence, indent=2), encoding='utf8')
    print('Three expanded vector figures and numeric provenance exported')


if __name__ == '__main__':
    main()
