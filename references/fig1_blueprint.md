# Fig. 1 blueprint

## Composition

Use a 16:9 overview page when the target venue permits it. The exemplar is a 16 by 9
inch native Visio page with a thin outer frame and three columns:

- left: equality-key input, measured evidence, and a compact workload panel;
- center: the method contract, answer bounds, frontier/event compaction, exact repair,
  and route selection;
- right: maintained-output example and measured output/evaluation panels.

The center receives the strongest visual weight. Headbands state the problem and the
method in one line, and a bottom band summarizes the route from answer bounds to probe
frontiers to adaptive traversal. Use arrows and braces only where they explain dataflow.

## Exemplar palette

The reference files are not the palette source. The exemplar uses:

| Role | Color |
| --- | --- |
| dark ink | `#302A32` |
| wine | `#973B59` |
| indigo | `#414B87` |
| copper-gold | `#A27722` |
| warm neutral | `#F3F0EE` |
| rose tint | `#F7E8ED` |
| lilac tint | `#EDF0FA` |
| sand tint | `#FBF4E3` |

When the target paper has a house palette, replace all colors coherently and record the
new mapping. “Replace the palette” means no accidental reuse of the reference's dominant
colors, not arbitrary color changes inside one panel.

## Scientific panel roles

The overview panels are deliberately small and descriptive:

- **Correlation heatmap:** show whether methods respond similarly after removing each
  scenario's shared scale. Put method codes and the transform in the panel itself.
- **Regime radar:** show how the comparison changes with workload regime. Use the same
  radial scale for every dataset, show the parity ring, and define abbreviations.
- **Raincloud:** show all observations, central tendency, and long tails. State that
  jitter is visual only and keep slowdowns rather than filtering them.

Expanded figures should enlarge the question rather than repeat the overview. The
exemplar's expanded radar overlays two baselines for each dataset, the expanded
raincloud compares both primary baselines and prints geometric mean plus win/tie/loss
counts, and the expanded correlation figure adds a per-dataset FAR strip.

## Text and source rules

- Use native text with real font metrics; fit text to boxes instead of allowing clipping.
- Use vector PDF/SVG exports for manuscript figures.
- Keep worked examples labeled as illustrative if they are not measurements.
- Keep method names and abbreviations consistent across the overview, expanded figures,
  captions, and body text.
- Do not place statistical significance stars or p-values unless they were actually
  computed and preregistered for the displayed comparison.
