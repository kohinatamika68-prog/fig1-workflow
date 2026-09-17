# Reusable Fig. 1 prompt recipe

These are the task instructions that shaped the bundled exemplar. They are prompts to
adapt, not hidden requirements for unrelated papers.

## Flowchart redesign

> Use the two supplied Visio Fig. 1 files as layout references. Redraw the paper's Fig. 1
> as an editable native Visio workflow diagram. Keep the method mechanism and worked
> example from the current paper, but replace the reference palette completely. Use a
> three-column composition with inputs/evidence, the central method, and outputs/evaluation.
> Preserve exact paper data and do not reuse data from the reference Visio files.

The useful constraints are:

- borrow composition and visual rhythm, not content;
- keep a clear left-to-right reading order;
- use stacked method bands and a bottom routing or summary band;
- retain a compact worked example when it explains the algorithm;
- use Times-compatible typography and enough contrast for a printed paper;
- write a geometry/specification file so the Visio export is deterministic.

## Data-driven “cool” panels

> Add two or three polished scientific panels related to the paper and generated only
> from the paper's measured data. The panels should make different evidence visible,
> carry readable labels at paper width, and avoid unsupported significance annotations.

For the FAR exemplar, the selected panels were:

1. A clustered correlation heatmap of scenario-centered log runtimes.
2. A radar chart of baseline/FAR ratios for six probe-fraction and batch-placement
   regimes, with a dashed parity ring.
3. Raincloud distributions of all per-dataset scenario-seed ratios, with the median,
   IQR, observed points, and a log-scale axis.

## Expansion into the paper

> Process the selected panels in more detail and place the expanded versions at the
> appropriate locations in the experimental section. The text around each figure must
> explain the comparison, aggregation, and the evidence-supported takeaway. Keep Fig. 1
> as the overview and use the expanded figures to expose patterns that cannot be read at
> overview size.

## Delivery

> Compile the anonymous and identified PDFs, render the affected pages, verify the values
> against the raw result table, confirm the editable source has no embedded bitmap-only
> figure, and package the source and research artifacts. Report paths and actual page
> counts.
