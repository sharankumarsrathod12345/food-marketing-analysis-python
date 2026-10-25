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
