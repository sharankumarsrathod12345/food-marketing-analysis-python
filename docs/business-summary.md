# Business summary: customer segmentation

## Decision

Which groups merit a controlled marketing test? This simulated case supports prioritizing hypotheses, not committing a budget based on observed response alone.

## Evidence

The deduplicated extract contains 2,021 profile rows and 311 latest-campaign responses (15.39%). Higher-spend/recent profiles account for 330 rows and 100 responses (30.30%). Lower-spend/less-recent profiles account for 683 rows and 38 responses (5.56%). See [segment table](../outputs/behavior_segments.csv).

Segments use the sample median of `MntTotal` and a 30-day recency cutoff. A response is not evidence that contact caused a purchase. Spending may also overlap the campaign period; do not treat these features as a validated predictive model.

## Recommended next step

Use the higher-spend/recent segment as a candidate for a randomized test. Before launch, obtain stable customer IDs, dated transactions and contacts, assignment/exposure records, offer costs, contribution margin, and consent/eligibility rules. Freeze segment membership using only pre-campaign information.

Randomize eligible profiles within segments into treatment and holdout groups. Agree the outcome window, minimum worthwhile effect, and sample-size calculation before testing. Evaluate incremental conversion and contribution margin per eligible customer; monitor opt-outs and complaints. Expand only if the evidence and economics support it. No lift or financial return has been measured in this project.

## Example client handoff

For a similar scoped engagement: input-quality log, agreed metric definitions, reconciled segment table, four explanatory charts, reproducible script/notebook, and an executive recommendation. Campaign execution and causal measurement require additional data and scope.

## Read next

[Notebook](../notebooks/food_marketing_analysis.ipynb) · [Duplicate sensitivity](../outputs/duplicate_sensitivity.csv) · [Source notes](../data/README.md)
