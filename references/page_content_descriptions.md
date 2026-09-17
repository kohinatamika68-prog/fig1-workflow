# Page content descriptions

Use these descriptions when a paper, report, or skill page needs a concise explanation
of what the Fig. 1 materials show.

## Fig. 1 overview page

The overview page introduces the full visual argument in one scan. The left column
states the input state and measured context. The center column explains the method's
ordered stages, exact bounds, frontier/event reduction, repair branch, and route choice.
The right column shows the maintained output and the evaluation view. Compact heatmap,
radar, and raincloud panels connect the mechanism to measured behavior without turning
the overview into a results table.

## Workload-regime page or figure

This page answers where the method's advantage changes across workload structure. Each
dataset receives a panel with six vertices: 1%, 10%, and 100% probe fractions crossed
with burst and uniform batches. Baseline/FAR ratios use a log2 radial scale and a dashed
1x parity ring. The descending-repair and delta-merge traces make sparse-versus-dense
routing behavior visible.

## Speedup-distribution page or figure

This page answers how consistently the method wins across individual scenarios. Each
point is a scenario-seed median. The raincloud density is estimated in log2 ratio space;
the dark bar shows the IQR, the white marker the median, and the labels below each
dataset give geometric mean plus FAR wins, ties, and losses. Slowdowns remain visible.

## Runtime-structure page or figure

This page answers whether methods respond to workload changes in similar ways. Panel (a)
clusters correlations of scenario-centered log runtimes across six methods. Panel (b)
shows FAR's correlation with the other methods separately for each dataset. The result
is descriptive and should not be described as a significance test.

## Asset/reference page

The supplied Visio files and the cool-figure screenshot are inspiration pages. They
define visual rhythm, density, and composition cues. They are not data sources. Any
paper-specific number, label, method name, or claim must be regenerated from the target
paper's evidence.
