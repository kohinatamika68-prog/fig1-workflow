# Data, provenance, and QA contract

## Data contract

Every plotted number must be recomputable from a result table. For the bundled FAR
exemplar the canonical source is `results/maintenance_full.jsonl`; the derived median
table groups by dataset, probe fraction, requested batch, pattern, seed, and method,
then takes the median of seven repeats. The exemplar contains 288 scenario-seed cases,
30,240 correct timed outputs, and 72 cases per dataset. New projects must recompute
these counts rather than copying them.

The exemplar transforms are:

1. **Runtime structure.** Take natural logs of the six displayed method medians for each
   scenario and subtract that scenario's mean log runtime. Compute Pearson correlations
   over scenarios and average-linkage clustering on `1 - r`. This is descriptive; no
   significance claim is attached.
2. **Workload regimes.** For each dataset and each of six regimes (1%, 10%, 100% probe
   fraction crossed with burst/uniform placement), compute the geometric mean of the
   baseline/FAR ratio over requested batch sizes and seeds. Use a log2 radial scale and
   a clearly marked 1x ring.
3. **Distributions.** Keep every scenario-seed median per dataset. Estimate a Gaussian
   KDE in log2 ratio space with Scott bandwidth over the observed min/max; normalize
   only the displayed density width within each dataset. Show all points, median, IQR,
   and min/max. Jitter must be deterministic and described as visual only.

## Visual and manuscript gates

- Check every native shape's coordinates against the page bounds; for lines check both
  endpoints rather than an axis-aligned width.
- Inspect PDF text bounding boxes for clipping and render all pages containing changed
  figures.
- For a VSDX, inspect the package for embedded `ForeignData` or bitmap media. A vector
  export is not a substitute for an editable source.
- Compile anonymous and identified variants. Check venue page limit, Fig. 1 placement,
  captions, references, `Overfull`, undefined references, and author leakage from the
  anonymous version.
- Verify standalone ZIP entries with a ZIP read/CRC test. If the source package is
  intended to compile independently, extract it to a temporary directory and compile it.

## FAR project verification commands

`src/verify_overview.py` checks the 614 native shapes, the measured overview values, the
expanded-figure ratios, the page count, PDF text bounds, anonymous/identified separation,
and the build logs. Use it as a model for a target-specific verifier; do not hard-code
614 or 288 for a new paper.
