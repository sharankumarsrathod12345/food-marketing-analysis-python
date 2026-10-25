# Review notes

Original notebook issues corrected:
1. Age-group population shares were labeled campaign acceptance percentages. Population counts and within-group response rates now have separate charts.
2. Purchase counts were labeled sales. They are now explicitly counts.
3. Arbitrary category codes were used in regression/correlation. Marital and education fields are decoded from validated one-hot indicators and summarized categorically.
4. A binary any-campaign indicator was named like a count. Counts and any-acceptance flags are now distinct; the latest response is separate.
5. Campaign budget allocations were recommended without cost, revenue attribution, or lift evidence. These recommendations were removed.
6. Colab-only paths and malformed prose inside code were replaced with portable paths and markdown.
7. Exact-row deletion is documented as an assumption. A sensitivity table compares all 2,205 source rows with 2,021 deduplicated rows.

Input SHA256: c49624a1611b27172becb351be6692863c07f897181f26d4c0f8880ce5670a9c

The source u_food_marketing.csv was subsequently supplied. Removing 184 exact duplicates reproduces every shared column of the cleaned input. Both inputs are retained for an explicit reconciliation check. The original case describes mock data; the dictionary confirms last-campaign response and two-year spending definitions. Exact calendar coverage, currency, and reuse terms remain unspecified.

## GitHub publication review — 2026-10-25

Published input, code, notebook, and output blobs matched the reviewed package. Removed the redundant outer project directory so the root README and run instructions agree. Added a business summary, clarified third-party data licensing, and changed the standalone script to resolve paths relative to its file. Standalone scripts were rerun; native notebook-kernel validation was pending at that stage and is now completed below.

## Native Jupyter validation completed — 2026-10-25

[Successful GitHub Actions run](https://github.com/sharankumarsrathod12345/food-marketing-analysis-python/actions/runs/40205390284) at commit `f26144546526047439a30b7e9918c0aa0751a570`.

Executed 9 code cells in a fresh Python 3.12.15 kernel after clearing saved outputs and execution counts. All 9 aggregate CSV files reconciled to the repository baselines using numerical tolerances (rtol=1e-9, atol=1e-10). Source hashes and notebook structure passed. The earlier local socket restriction is superseded by this successful hosted run. See `native-validation.json` for the package versions and file list.
