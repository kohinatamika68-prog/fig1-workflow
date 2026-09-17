# ModelViz candidate catalog

This reference records the complete chart-family search space used by
`fig1-workflow`. It is based on the upstream [hrdZhu/modelviz-skill](https://github.com/hrdZhu/modelviz-skill)
repository at commit `cd9eac0202163706bbcef269c0c5623c79bb8eb5` (snapshot checked
2026-09-17). The accompanying
[`modelviz_template_index_snapshot.csv`](modelviz_template_index_snapshot.csv)
contains all 89 indexed templates at that commit. It is an index only: do not
execute its demo data or treat its preview values as results for a paper.

## Selection contract

The 12 categories below are the candidate universe. A new Fig. 1 run must first
consider every category, then narrow the list using the paper's scientific question,
data schema, readability at the target width, and the need for an editable/vector
output. A category may be rejected when the paper has no compatible data; record that
reason instead of silently ignoring it. The final selection record should contain:

1. every category considered;
2. the selected template IDs and the panel question each answers; and
3. the rejected candidates and a short reason (missing schema, redundant question,
   unsupported uncertainty, unreadable at Fig. 1 scale, or page/layout constraint).

Use the upstream catalog and this snapshot to recall candidates. Adapt a template's
layout and visual grammar, but copy neither its demo data nor unsupported claims. All
plotted values, transformations, error bars, significance marks, and labels must be
traceable to the target paper's result files.

## Complete category map

| Code | Upstream category | Templates | Scientific questions and compatible inputs |
| --- | --- | ---: | --- |
| `01_CLU` | `clustering_reduction`（聚类与降维） | 4 | Group structure, distances, covariance, or low-dimensional projections. Use a feature matrix plus optional labels, distances, or environmental variables. |
| `02_CMP` | `comparison_ranking`（比较与排序） | 16 | Which methods, datasets, regimes, or metrics are larger, better, or compositionally different? Use grouped metric tables, profiles, proportions, or ranked values. |
| `03_EVL` | `composite_evaluation`（综合评估） | 2 | How do several evaluation dimensions combine in one report? Use model-by-metric scores or aligned multi-omics/validation measurements with a defined scale. |
| `04_DIS` | `distribution_uncertainty`（分布与不确定性） | 6 | How variable, skewed, separated, or statistically different are observations? Use replicate-level values, group/scenario labels, and defensible uncertainty or test results. |
| `05_MPN` | `multi_panel_report`（多面板报告） | 4 | Which coordinated views are needed to tell one evidence story? Use aligned tables or precomputed panels that share entities, models, or time points. |
| `06_NET` | `network_flow`（网络与流向） | 2 | What connects, overlaps, transfers, or flows between entities? Use node-edge, overlap, adjacency, or flow data; do not infer edges from visual proximity. |
| `07_OPT` | `optimization_decision`（优化与决策） | 1 | Which parameter, threshold, or configuration optimizes an objective under stated constraints? Use a parameter grid, objective values, and constraint/decision metadata. |
| `08_PRD` | `prediction_evaluation`（预测与评估） | 10 | How accurate, calibrated, or stable are predictions? Use observed outcomes with scores/predictions, folds, model labels, and a declared evaluation protocol. |
| `09_REL` | `relationship_correlation`（关系与相关性） | 21 | What association, effect, interaction, or regression relationship is supported? Use paired observations or an auditable correlation/effect/edge table; association is not causation. |
| `10_SEN` | `sensitivity_robustness`（敏感性与稳健性） | 15 | Which inputs drive model output and how do effects change across values or interactions? Use model explanations (SHAP/PDP/GAM) or a sensitivity grid generated from the fitted model. |
| `11_SPA` | `spatial_geographic`（空间与地理） | 4 | Where does an effect or prediction occur, and how does it vary spatially? Use coordinates, geometries, rasters, or a declared CRS; never invent geography from row order. |
| `12_TRD` | `trend_time_series`（趋势与时间序列） | 4 | How does a measure change over ordered time, including lag or smoothing? Use timestamps/periods, one or more measures, and an explicitly stated aggregation or lag rule. |

The category counts sum to 89 templates. The full template IDs, source filenames,
data-file hints, and runtime status are preserved in the CSV snapshot. When an
upstream update is available, refresh the snapshot and this commit pin together so
the candidate universe remains auditable.

## Fig. 1 panel decision rules

- Start from the panel question, not from a visually attractive chart. A panel should
  explain a method mechanism, a comparison, a distribution/uncertainty claim, a
  relationship, a robustness property, or another question the paper explicitly asks.
- Prefer two or three non-redundant panels in the overview. If a category is useful but
  too dense at Fig. 1 width, place its expanded version in the experimental section and
  keep a legible summary in the overview.
- Treat `05_MPN` as a composition option when several categories must be coordinated,
  not as permission to combine unrelated statistics. Every subpanel still needs its
  own data trace and caption.
- Reject `06_NET`, `07_OPT`, `08_PRD`, `10_SEN`, `11_SPA`, or `12_TRD` when the paper
  lacks the required edges, objective grid, prediction protocol, explanation output,
  spatial reference, or ordered time axis. Do not fill the gap with simulated values.
- Check panel semantics before layout: uncertainty bands require repeated observations
  or a reported uncertainty estimate; significance annotations require the stated test
  and correction; causal wording requires a causal design.

## Current FAR exemplar mapping

The bundled FAR Fig. 1 currently selects only a small, data-supported subset:

| Panel | ModelViz category | Why it was selected |
| --- | --- | --- |
| Runtime-correlation heatmap | `09_REL` relationship/correlation | The result table contains paired runtime/structure measures and the panel exposes their association. |
| Workload-regime radar | `02_CMP` comparison/ranking | The same metric can be compared across six workload regimes and method roles. |
| Per-dataset speedup raincloud | `04_DIS` distribution/uncertainty | Scenario-seed ratios support distribution shape, central tendency, dispersion, and win/tie/loss counts. |

These three are examples of the final data-driven choice, not a hard-coded whitelist.
For another paper, the selection may come from any of the 12 categories, including a
different subset or a coordinated multi-panel template.

