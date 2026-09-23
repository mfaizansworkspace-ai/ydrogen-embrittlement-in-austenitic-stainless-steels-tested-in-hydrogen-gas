# HE-Austenite

An open dataset of hydrogen embrittlement in austenitic stainless steels tested in **hydrogen gas**, with the weld zone recorded for every row.

**Version 1.0** · 113 records · 9 sources, 1983–2024 · Data CC BY 4.0 · Code MIT

Values were extracted by hand from published tables. No new experiments were performed, and no source document is redistributed here.

## Why this dataset exists

Hydrogen infrastructure is welded. Refuelling stations run at 70 MPa, storage vessels and tube trailers are welded assemblies, and repurposing existing pipe networks depends on how the joints behave rather than the plate.

A weld is a casting sitting inside a wrought product. Its structure is dendritic, its composition differs from the parent metal, and austenitic stainless weld metal deliberately retains a few percent of delta ferrite to avoid solidification cracking. The weld is therefore the part of a joint least like the material a designer looked up, and the part hydrogen reaches first.

Most published embrittlement data covers base metal, and most recent weld studies charge specimens electrochemically, which cannot be converted to an equivalent gas pressure without assumptions about charging efficiency. This dataset keeps only gaseous exposure and records the weld zone for every row.

## What the data shows

Relative reduction of area (RRA) is the reduction of area measured in or after hydrogen divided by the value in the reference environment. A value of 1.0 means no measurable loss. Japanese regulatory practice accepts austenitic stainless steels for hydrogen service at RRA ≥ 0.80.

Zone and alloy family are **not independent** in this dataset, so they have to be read together. The table below is the honest form of the comparison — each cell gives the number of records and their median RRA.

| Alloy family | Base metal | Whole welded joint | Weld metal | All |
|---|---|---|---|---|
| Type 304 family | 14 / 0.72 | 8 / 0.59 | 12 / 0.48 | 34 / 0.53 |
| Types 316 and 317 | 8 / 0.99 | 4 / 0.96 | 2 / 0.73 | 14 / 0.96 |
| Types 321 and 347 | 3 / 0.91 | — | — | 3 / 0.91 |
| 21-6-9 | 2 / 0.98 | 12 / 0.87 | — | 14 / 0.92 |
| 22-13-5 | 4 / 1.01 | — | — | 4 / 1.01 |
| Type 310 | 2 / 0.97 | — | — | 2 / 0.97 |
| Duplex 2507 | 2 / 0.43 | — | — | 2 / 0.43 |
| A286 | 1 / 0.51 | — | — | 1 / 0.51 |
| **All families** | **36 / 0.85** | **24 / 0.83** | **14 / 0.49** | **74 / 0.80** |

The bottom row — base metal 0.85 against weld metal 0.49 — looks like a large weld penalty, but the two groups are not comparable head to head. The 14 weld-metal records come from three sources and 12 of them are type 304 family, while the 36 base-metal records span eight families and include the more stable grades. The within-family rows are where the zone effect can actually be read: 0.72 against 0.48 in the type 304 family, and 0.99 against 0.73 in types 316 and 317, on two weld records.

![Relative reduction of area in gaseous hydrogen by alloy family](figures/fig1_family.png)

The alloy family ordering follows austenite stability. Type 310 and the nitrogen-strengthened grades 21-6-9 and 22-13-5 hold their ductility; the type 304 family, whose austenite transforms under strain, does not.

### On delta ferrite

Nakamura et al. (2018) tested one TIG-welded bar three ways at 228 K (−45 °C) in 106 MPa hydrogen against a nitrogen reference:

| Condition | RRA |
|---|---|
| 316 hi-Ni base metal | 1.02 |
| 317L weld metal, as welded (delta ferrite present) | 0.55 |
| 317L weld metal, post-weld solution treated | 0.91 |

One material, one gas, one temperature, and the solution treatment that dissolves the ferrite is what changes.

**This reading is contested, and the dataset cannot settle it.** Hirata (2015), which reports RRA against delta ferrite ratio for ten weld metals in 45 MPa hydrogen gas, concludes the opposite: that weld-metal embrittlement is governed by austenite stability (Md30, nickel equivalent) rather than by delta ferrite, and attributes the effect to strain-induced α′-martensite. That study reports its results only in figures and is not in this dataset.

Meanwhile `ferrite_number` is populated for **2 of 113 records** here — the two notched 304L/308L composite welds from the Sandia reference, at FN 4.7 → RRA 0.350 and FN 8.5 → RRA 0.425, which run in the opposite direction to the Nakamura reading. Nobody should model ferrite content against ductility from this release.

## Repository contents

```
data/     he_austenite_v1.0.csv     the dataset, 113 records, 30 fields
          HE-Austenite_v1.0.xlsx    same rows plus summary, data dictionary, sources, extraction log
          records_raw.json          raw extraction records with full provenance notes
scripts/  schema.json               record schema
          normalise.py              derived values and validation
          build_outputs.py          cleaning and CSV export
          build_workbook.py         Excel workbook
          make_figures.py           figures
figures/  the three figures used in the paper
paper/    data descriptor, Word and PDF
docs/     data dictionary with per-field completeness, and the source list
```

## Scope

A record is included when:

1. the material is an austenitic stainless steel, or a related grade flagged by `material_family` (duplex 2507, A286);
2. hydrogen was introduced **as a gas**, either by testing in high-pressure hydrogen or by thermal precharging in hydrogen gas;
3. a reference measurement exists from the same study and material, in air, helium, nitrogen, argon or the uncharged condition;
4. the value appears in a table rather than only in a figure.

Coverage: 228 to 423 K throughout, and 0.1 to 172 MPa hydrogen for the 104 records whose source stated a pressure.

Electrochemically charged studies are excluded. They are listed with the reason in the Extraction log sheet of the workbook, along with sources identified too late for this release.

## Field completeness

Not every field is populated for every record. The full table is in `docs/data_dictionary.md` and in the workbook's Data dictionary sheet. The ones worth knowing before you download:

| Field | Populated |
|---|---|
| `h2_pressure_MPa` | 104 of 113 |
| `strain_rate_per_s` | 64 of 113 |
| `weld_process` | 60 of 113 |
| `hydrogen_content_wppm` | 52 of 113 |
| `filler_metal` | 50 of 113 |
| `charging_time_h` | 45 of 113 |
| `heat` | 16 of 113 |
| `ni_equivalent` | 14 of 113 |
| `ferrite_number` | **2 of 113** |

Md30 is not computed in this release: too few sources report the nitrogen and carbon contents it needs.

## Data quality

- Extraction was manual, from source tables into a validated JSON schema.
- 24 of 113 records were independently re-extracted from the source documents and compared; all matched. Those rows are marked `verified = yes`.
- 103 of the 113 ratios were computed from a stored pair of absolute values, and every one reproduces to within 0.002 on recomputation. The nine records from Younes (2013) carry a ratio computed from a reported percentage loss (1 − loss/100) and so have no `property_reference` or `property_h2`; the single Matsuoka record carries a ratio the source printed directly.
- Every record was checked against the scope rule, validated against the schema, range-checked, and checked for a unique identifier.
- Where a source printed its own ratio alongside absolute values, the computed value was compared against it. For Balch et al. (2015) the six computed weld values reproduce the published ones within rounding.
- Identification, screening and extraction were done by one person. There was no second independent screener, so screening error cannot be quantified.

## Known gaps

- The heat affected zone and fusion line are defined in the `zone` vocabulary but carry **no records** in v1.0.
- Four relevant studies report results only in figures and are not included: Hirata (2015), Yamabe et al. (2017), Zhang et al. (2013), and the remainder of Matsuoka et al. (2017) beyond the one numeric value used. Hirata is the most important and is the first target for the next release.
- Family medians for types 321/347 (n = 3), type 310 (n = 2), duplex (n = 2) and A286 (n = 1) rest on few records and are indicative only.
- Reference environments are mixed: 48 records against air, 28 against high-pressure helium, 32 against the uncharged condition, 5 against nitrogen or argon. A helium reference at test pressure is stricter than an air reference. The field is recorded so users can filter. Twelve of the 14 weld-metal records use an uncharged reference.
- Three sources were identified after extraction closed and are logged as candidates rather than quietly omitted: J. Nakamura et al. (2024) on GTAW 316L joints in high-pressure hydrogen at two heat inputs; Bao et al. (2021) on type 304 with delta ferrite in 5 MPa hydrogen against argon; and Hirata et al. (2013), the Japanese original of the 2015 translation.

## Reproducing

```bash
pip install -r requirements.txt
# run from the repository root
python scripts/normalise.py data/records_raw.json   # validate and recompute derived values
python scripts/build_outputs.py                     # clean, write data/he_austenite_v1.0.csv and data/clean.json
python scripts/build_workbook.py                    # rebuild data/HE-Austenite_v1.0.xlsx
python scripts/make_figures.py                      # regenerate figures/
```

## Sources

Caskey, DP-1643 (1983) · San Marchi and Somerday, SAND2012-7321 (2012) · Balch et al., PVP2015-45591 · Michler et al., Int. J. Hydrogen Energy (2009) · Nakamura et al., Trans. JSME (2018) · Younes et al., Int. J. Hydrogen Energy (2013) · Iyer, Can. Metall. Q. 28 (2) (1989) 153 · Fukunaga, Eng. Fail. Anal. (2024) · Matsuoka et al., Solid State Phenomena (2017).

Full citations are in `docs/data_dictionary.md`, in the Sources sheet of the workbook, and in the paper.

## Corrections and contributions

If a value here disagrees with the source in front of you, open an issue with the `record_id`, the value in the dataset, the value you read, and the table it came from. Additions are welcome under the same scope rule: gaseous hydrogen, a paired reference measurement, and a value that appears in a table.

Record identifiers taken from the Sandia reference changed in v1.0, from `SAND-2101-…` to `SAND2012-ch2101-…`, so that the report number and the chapter number are no longer confusable.

## Citation

See `CITATION.cff`. Once the release is archived on Zenodo, cite the DOI.

## Licence

Code MIT. Dataset files in `data/` are CC BY 4.0.
