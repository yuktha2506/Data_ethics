# ShopNest Anonymization Assessment — Demonstration Code

This folder contains the actual working code used to produce every number, table
and figure in the report `ShopNest_Anonymization_Report.docx`.

## How to reproduce the results

```bash
pip install pandas numpy matplotlib openpyxl
python3 generate_datasets.py   # creates Dataset A and Dataset B (synthetic, seeded)
python3 analysis.py            # runs baseline uniqueness check, linkage attack
                                # (before + after anonymization), and all 8
                                # anonymization techniques -> writes results.json
python3 make_figures.py        # renders Figure 1 and Figure 2 used in the report
```

## Files

- `generate_datasets.py` — builds the synthetic Dataset A (ShopNest customer/order
  records) and Dataset B (public auxiliary directory) with a controlled 380-person
  overlap, used as the linkage-attack demonstration.
- `analysis.py` — the linkage/anonymization pipeline: baseline quasi-identifier
  uniqueness, the pre-anonymization linkage attack, all 8 anonymization
  techniques (suppression, generalization, masking, aggregation, perturbation,
  k-anonymity, pseudonymization, differential privacy), and the
  post-anonymization re-linkage test. Outputs `results.json` and the CSV
  datasets used to build the accompanying Excel workbook.
- `make_figures.py` — builds Figure 1 (re-identification risk across stages) and
  Figure 2 (utility retained after anonymization).

All random seeds are fixed, so re-running this code reproduces the exact numbers
quoted in the report (e.g. 63.3% pre-anonymization re-identification, 0%
post-anonymization re-identification for this specific tested attack).
