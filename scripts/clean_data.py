"""Clean the private dairy CSV in chunks; never impute or discard records."""

import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
COLUMNS = {
    "AnimalId": "cow_id",
    "LactationNumber": "lactation_number",
    "DaysInMilk": "days_in_milk",
    "ReproductionStatus": "reproduction_status",
    "EventDate": "event_date",
    "Avgmilkflow": "avg_milk_flow",
    "Flow30_60Session": "flow_30_60_session",
    "YieldFirst2Min_Session": "yield_first_2_min_session",
    "YieldSession": "milk_yield",
    "DurationSession_sec": "duration_session_sec",
    "milking": "milking",
}
INTEGER_COLUMNS = {"lactation_number", "days_in_milk", "milking"}
NUMERIC_COLUMNS = list(COLUMNS.values())[1:3] + list(COLUMNS.values())[5:]
# Zero is retained: its biological meaning requires the data owner's input.
MISSING_TOKENS = {"", "null", "none", "na", "n/a", "nan"}


def clean_chunk(raw, offset=0):
    """Return cleaned records and per-column invalid counts.

    Original source fields remain verbatim in *_raw columns. source_row is a
    1-based CSV data-record number (excluding the header), not a physical line.
    """
    clean = pd.DataFrame(index=raw.index)
    clean["source_row"] = np.arange(offset + 1, offset + len(raw) + 1)
    invalid_counts = {}
    for original, name in COLUMNS.items():
        clean[name + "_raw"] = raw[original]
        text = raw[original].str.strip()
        clean[name] = text.mask(text.str.lower().isin(MISSING_TOKENS))

    # IDs are opaque strings, including negative IDs and leading zeros.
    for name in NUMERIC_COLUMNS:
        values = pd.to_numeric(clean[name], errors="coerce")
        invalid = clean[name].notna() & (
            values.isna() | ~np.isfinite(values) | values.lt(0)
        )
        if name in INTEGER_COLUMNS:
            invalid |= values.mod(1).ne(0).fillna(False)
        invalid = invalid.fillna(False)
        clean[name + "_invalid"] = invalid
        invalid_counts[name] = int(invalid.sum())
        clean[name] = values.mask(invalid)

    dates = pd.to_datetime(clean["event_date"], format="%Y-%m-%d", errors="coerce")
    invalid = clean["event_date"].notna() & dates.isna()
    clean["event_date_invalid"] = invalid
    invalid_counts["event_date"] = int(invalid.sum())
    clean["event_date"] = dates.dt.strftime("%Y-%m-%d").astype("string")
    clean["reproduction_status"] = clean["reproduction_status"].str.lower()
    clean["cow_id_missing"] = clean["cow_id"].isna()
    clean["milk_yield_missing"] = clean["milk_yield"].isna()
    return clean, invalid_counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path,
                        default=ROOT / "data/raw/Data_set_prep_assignment_1.csv")
    parser.add_argument("--output", type=Path,
                        default=ROOT / "data/processed/milk_yield_cleaned_v1.csv")
    parser.add_argument("--chunksize", type=int, default=100_000)
    args = parser.parse_args()
    if args.chunksize < 1:
        parser.error("--chunksize must be positive")
    source, destination = args.input.resolve(), args.output.resolve()
    if source == destination or destination.is_relative_to(ROOT / "data/raw"):
        parser.error("Output must be separate from the raw data directory")
    report_path = destination.with_suffix(".report.json")
    for path in (destination, report_path):
        if path.exists():
            parser.error(f"Output already exists; choose another --output: {path}")
    header = pd.read_csv(source, nrows=0).columns.tolist()
    if len(header) != len(COLUMNS) or set(header) != set(COLUMNS):
        parser.error(f"Unexpected source columns: {header}; expected {list(COLUMNS)}")

    destination.parent.mkdir(parents=True, exist_ok=True)
    missing, invalid, patterns, statuses = Counter(), Counter(), Counter(), Counter()
    rows = 0
    date_min = date_max = None
    # Exclusive creation prevents an accidental overwrite, including concurrent runs.
    with destination.open("x", newline="") as output:
        for raw in pd.read_csv(source, dtype="string", keep_default_na=False,
                               skip_blank_lines=False, chunksize=args.chunksize):
            clean, counts = clean_chunk(raw, rows)
            clean.to_csv(output, index=False, header=rows == 0)
            invalid.update(counts)
            missing.update({c: int(clean[c].isna().sum()) for c in COLUMNS.values()})
            for (cow_missing, yield_missing), count in clean.groupby(
                ["cow_id_missing", "milk_yield_missing"]
            ).size().items():
                patterns[f"cow_id_missing={cow_missing},milk_yield_missing={yield_missing}"] += int(count)
            statuses.update(clean["reproduction_status"].dropna().value_counts().to_dict())
            dates = clean["event_date"].dropna()
            if not dates.empty:
                date_min = min(date_min or dates.min(), dates.min())
                date_max = max(date_max or dates.max(), dates.max())
            rows += len(raw)
            print(f"Processed {rows:,} rows", flush=True)

    report = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "input": str(source), "input_bytes": source.stat().st_size,
        "output": str(destination), "rows_in": rows, "rows_out": rows,
        "column_mapping": COLUMNS,
        "missing_after_cleaning": dict(missing),
        "invalid_values_set_to_missing": dict(invalid),
        "missing_patterns": dict(patterns),
        "reproduction_status_counts": dict(statuses),
        "event_date_range": [date_min, date_max],
        "decisions": [
            "All records retained in original order; no imputation or ID inference.",
            "Original fields retained in *_raw; IDs kept as strings.",
            "Whitespace trimmed; blank/null/none/na/n/a/nan normalized to missing.",
            "Malformed, nonfinite, negative numeric values set to missing and flagged.",
            "Fractional lactation number, days in milk, or milking set to missing and flagged.",
            "Dates parsed as YYYY-MM-DD; invalid dates set to missing and flagged.",
            "Reproduction status lowercased; unknown categories retained.",
            "Zeros and high values retained; yield units and upper limits unconfirmed.",
            "Duplicates not checked or removed: repeated sessions may be legitimate.",
        ],
    }
    with report_path.open("x") as report_file:
        json.dump(report, report_file, indent=2)
    print(f"Saved {destination}\nQuality report: {report_path}")


if __name__ == "__main__":
    main()
