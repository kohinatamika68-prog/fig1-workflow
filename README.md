# Fig. 1 Workflow Skill

This repository packages a reusable Codex skill for building a publication-ready Fig. 1
that connects a method workflow to measured evidence. It preserves the editable Visio
source, the visual references used for composition, the prompt recipe, and the chart
generation/verification templates.

## Page and file map

| Page or file | What it contains | When to read it |
| --- | --- | --- |
| `SKILL.md` | The main workflow, source hierarchy, editability rules, and completion gates. | Start here when invoking the skill. |
| `references/prompt_recipe.md` | The reusable redesign, scientific-panel, paper-integration, and delivery instructions. | When translating a user's natural-language request into a Fig. 1 plan. |
| `references/fig1_blueprint.md` | Three-column layout, palette, typography, panel roles, and native-shape guidance. | When deciding geometry and visual hierarchy. |
| `references/data_and_qa_contract.md` | Data transforms, provenance rules, PDF/VSDX checks, and package validation. | Before plotting or delivering. |
| `references/asset_manifest.md` | Description of every bundled image, VSDX, vector export, and source template. | When selecting a reference or exemplar asset. |
| `references/modelviz_catalog.md` | Complete ModelViz category map, data requirements, panel decision rules, and FAR mapping. | Before selecting any scientific panel. |
| `references/modelviz_template_index_snapshot.csv` | Full 89-template index snapshot from the pinned ModelViz commit. | When recalling candidate templates and recording exclusions. |
| `assets/fig1_editable_exemplar.vsdx` | Editable FAR Fig. 1 source. | When starting from a complete native layout. |
| `assets/fig1_overview_with_panels.*` | Overview render with the compact “cool” panels. | When checking the intended final composition. |
| `assets/workload_regimes.*` | Expanded radar analysis. | For workload-regime comparisons in the paper body. |
| `assets/speedup_distributions.*` | Expanded raincloud analysis. | For full-distribution baseline comparisons. |
| `assets/runtime_structure.*` | Expanded correlation and dataset-strip analysis. | For method-behavior and mechanism interpretation. |
| `assets/reference_*.vsdx` | The two supplied Visio composition references. | For layout rhythm only; never copy their data. |
| `assets/reference_cool_figures_grid.png` | The supplied scientific-figure moodboard. | For the requested rich, multi-panel visual direction. |
| `assets/source_templates/` | Generator, exporter, verifier, and packaging templates used by the exemplar. | When adapting the workflow to a new paper. |

## Paper reading order

The bundled paper places the visual story in this order:

1. **Fig. 1, overview page:** left-side inputs and measured evidence, center method
   mechanism, right-side maintained output and compact evaluation panels.
2. **Workload-regime analysis:** the radar expands the compact overview into six
   probe-fraction and batch-placement regimes for each dataset.
3. **Distribution analysis:** the rainclouds expose all scenario-seed ratios, central
   tendency, dispersion, long tails, and baseline win/tie/loss counts.
4. **Runtime-structure analysis:** the clustered heatmap and dataset strip separate
   shared workload scale from method-specific behavior before the ablation discussion.

Each page or figure answers a different question. The overview explains how the method
works; the expanded figures explain when the measured benefit appears and how stable it
is across the workload grid.

## Complete ModelViz candidate space

The skill uses [hrdZhu/modelviz-skill](https://github.com/hrdZhu/modelviz-skill) as a
candidate catalog. The included snapshot is pinned to commit
`cd9eac0202163706bbcef269c0c5623c79bb8eb5` (checked 2026-09-17). It covers all 89
templates in these 12 families:

| Family | Templates | Typical evidence question |
| --- | ---: | --- |
| Clustering / reduction | 4 | Are samples or variables grouped, separated, or projected? |
| Comparison / ranking | 16 | Which method, regime, metric, or composition is larger or better? |
| Composite evaluation | 2 | How do several evaluation dimensions combine? |
| Distribution / uncertainty | 6 | How variable, skewed, separated, or statistically different are observations? |
| Multi-panel report | 4 | Which coordinated views are needed for one evidence story? |
| Network / flow | 2 | What connects, overlaps, transfers, or flows between entities? |
| Optimization / decision | 1 | Which parameter or configuration optimizes a stated objective? |
| Prediction evaluation | 10 | How accurate, calibrated, or stable are predictions? |
| Relationship / correlation | 21 | What association, effect, interaction, or regression relationship is supported? |
| Sensitivity / robustness | 15 | Which inputs drive output and how do effects change across values? |
| Spatial / geographic | 4 | Where does an effect or prediction occur? |
| Trend / time series | 4 | How does a measure change over ordered time or lag? |

The heatmap, radar, and raincloud in the bundled FAR example are only one data-driven
subset: `09_REL`, `02_CMP`, and `04_DIS`, respectively. For a new paper, the workflow
considers all 12 families first, then selects two or three non-redundant panels that
match the paper's question, exact data schema, and Fig. 1 width. The selection record
must list the families and template IDs considered, selected, and rejected with
reasons. ModelViz demo data and preview values are never used as paper evidence.

## Use the skill

Invoke it with:

```text
Use $fig1-workflow to create or refine an editable Fig. 1 workflow diagram from the
paper's actual result files, using a new palette and two or three evidence-backed
scientific panels.
```

For the bundled FAR exemplar, the reproducible commands are:

```powershell
python -X utf8 src/detailed_figures.py
& src/create_visio.ps1
python -X utf8 paper/build.py
python -X utf8 src/verify_overview.py
python -X utf8 src/package_release.py
```

The skill is intentionally evidence-bound: reference diagrams provide style, while all
numbers and claims come from the target paper's own data. The current GitHub repository
is private because the assets include user-provided screenshots and Visio files.
