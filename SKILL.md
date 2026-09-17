---
name: fig1-workflow
description: "Create or refine publication-ready Fig. 1 workflow diagrams with an editable Visio-style layout, a fresh palette, and data-driven scientific panels. Use for graphical abstracts, method flowcharts, or requests to add polished plots to a paper figure."
---

# Fig. 1 Workflow

Use this skill when a paper needs a visually rich Fig. 1 that explains the method and
connects it to measured evidence. The output is a reviewable editable source when the
requested tool is available, plus vector exports, paper integration, and a numeric QA
record.

## Source hierarchy

The user's current request controls content and scope. Attached Visio files and the
cool-figure screenshot are style references only. Do not copy their data, labels,
significance marks, or claims. Use the paper's own result files for every plotted value.
Keep negative results and scope conditions visible. Never fill an unsupported panel with
illustrative or invented measurements.

Read the supporting references only as needed:

- [prompt_recipe.md](references/prompt_recipe.md) preserves the reusable instructions
  that produced this Fig. 1 and the expanded analysis figures.
- [fig1_blueprint.md](references/fig1_blueprint.md) gives the layout, palette, panel
  roles, and editability requirements.
- [data_and_qa_contract.md](references/data_and_qa_contract.md) gives the data
  transformations, reproducibility checks, and paper-integration gates.
- [asset_manifest.md](references/asset_manifest.md) maps the bundled screenshot,
  reference Visio files, editable exemplar, and chart exports to their intended use.
- [modelviz_catalog.md](references/modelviz_catalog.md) defines the complete ModelViz
  candidate universe, category-level data requirements, selection rules, and the
  current FAR mapping.
- [modelviz_template_index_snapshot.csv](references/modelviz_template_index_snapshot.csv)
  is the auditable 89-template index snapshot used for candidate recall.
- [page_content_descriptions.md](references/page_content_descriptions.md) supplies
  concise descriptions for the overview page and each expanded scientific figure.

## ModelViz candidate space

Use the upstream [ModelViz catalog](https://github.com/hrdZhu/modelviz-skill) as a
recall space, not as a fixed three-chart recipe. The catalog snapshot covers all
12 upstream families: clustering/reduction, comparison/ranking, composite evaluation,
distribution/uncertainty, multi-panel reports, network/flow, optimization/decision,
prediction evaluation, relationship/correlation, sensitivity/robustness,
spatial/geographic analysis, and trend/time-series analysis. The current FAR heatmap,
radar, and raincloud are only the panels that fit its result tables.

For every new paper, make a short candidate ledger before drawing:

1. consider all 12 families and recall compatible template IDs from the snapshot;
2. match each candidate to the paper's question and exact input schema;
3. select a small non-redundant subset that remains legible at Fig. 1 width and can be
   exported as editable/vector artwork; and
4. record selected IDs, the question each panel answers, and rejected families or
   templates with a concrete reason.

The ModelViz examples and demo data are style and layout references only. Do not
execute their demo data, copy their reported values, or invent missing uncertainty,
significance, spatial coordinates, network edges, prediction labels, or time ordering.
Use the target paper's result files for every plotted value and keep the provenance
record with the figure package.

## Workflow

1. Inspect the manuscript, its result files, the attached references, and the assets in
   this skill. Identify the paper's method stages, inputs, outputs, evaluation metrics,
   and the exact data table that supports each panel.
2. Build a three-column composition: measured inputs/evidence on the left, layered
   method logic in the center, and maintained outputs plus evaluation on the right.
   Use stacked section bands and a compact bottom routing/summary band when they clarify
   the reading order.
3. Run the ModelViz candidate-ledger step before choosing scientific panels. Reserve the
   main diagram for the method mechanism, then add two or three non-redundant,
   data-driven panels that answer distinct questions. The exemplar uses a clustered
   runtime-correlation heatmap, a six-regime baseline/FAR radar, and per-dataset
   speedup rainclouds. Replace these with candidates from any ModelViz family when the
   local data and paper question support them; never treat the exemplar's three charts
   as a whitelist.
4. Use a fully new palette relative to the supplied references. The exemplar palette is
   wine, indigo, copper-gold, warm neutral, and a dark ink. Keep contrast sufficient for
   grayscale printing and use color consistently for method roles and datasets.
5. Keep every Fig. 1 object editable: native Visio rectangles, text, connectors,
   ellipses, and polygons; no screenshot pasted into the VSDX and no rasterized chart
   used as the only source. If a chart is exported separately, retain the native source
   or a reproducible vector generator as well.
6. Add expanded versions of the scientific panels to the experimental section when they
   provide analysis that cannot be read at Fig. 1 width. Put the workload decomposition
   beside the main maintenance-cost result, the distribution comparison after the
   dataset-level summary, and the runtime-structure analysis before ablations or
   mechanism interpretation. Each figure needs a caption that states its aggregation,
   scale, and what the reader should learn.
7. Compile anonymous and identified variants, render the first page and every page
   containing a new figure, run the numeric/native-shape QA, and update the delivery
   package. Stop if a value cannot be traced to the paper's data or if a new figure
   exceeds the venue's page limit without an authorized layout decision.

## Project exemplar commands

In the FAR project bundled with this skill, the reproducible sequence is:

```powershell
python -X utf8 src/detailed_figures.py
& src/create_visio.ps1
python -X utf8 paper/build.py
python -X utf8 src/verify_overview.py
python -X utf8 src/package_release.py
```

Adapt paths and scripts to the target paper. Do not claim that these commands ran for
another project unless their outputs exist and pass the same checks.

## Completion criteria

Deliver the editable Fig. 1 source, overview PDF/SVG/PNG, standalone scientific-panel
exports, the compiled paper variants, and a short provenance/QA record. Report the
actual page count and any remaining author-review item. Keep the reference files
unchanged.
