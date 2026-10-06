"""Deduplicate raw records and create date-separated milk-yield datasets."""
import argparse
import csv
from collections import Counter
from contextlib import ExitStack
import json
from pathlib import Path
import sqlite3
import tempfile

import pandas as pd

from clean_data import COLUMNS, ROOT, clean_chunk


def write_csv(frame, output, header=False):
    writer = csv.writer(output)
    if header:
        writer.writerow(frame.columns)
    writer.writerows(frame.astype(object).where(frame.notna(), '').itertuples(index=False, name=None))


def prepare(source, destination, chunksize=100_000):
    # A new directory also prevents mixing a failed run with a successful run.
    destination.mkdir(parents=True, exist_ok=False)
    counts = Counter()
    dates = Counter()
    dedup_path = destination / 'deduplicated.csv'
    with tempfile.TemporaryDirectory(prefix='dairy_dedup_') as temporary:
        database = sqlite3.connect(str(Path(temporary) / 'seen.sqlite'))
        database.execute('PRAGMA journal_mode=OFF')
        database.execute('PRAGMA synchronous=OFF')
        database.execute('PRAGMA cache_size=-131072')
        database.execute('CREATE TABLE seen (record TEXT PRIMARY KEY) WITHOUT ROWID')
        with dedup_path.open('x') as output:
            for raw in pd.read_csv(source, dtype='string', keep_default_na=False,
                                   skip_blank_lines=False, chunksize=chunksize):
                if set(raw.columns) != set(COLUMNS):
                    raise ValueError('Unexpected raw data columns')
                # Store the complete field tuple, not a hash: equality is exact.
                keep = []
                for record in raw[list(COLUMNS)].itertuples(index=False, name=None):
                    key = json.dumps(record, ensure_ascii=False, separators=(',', ':'))
                    cursor = database.execute('INSERT OR IGNORE INTO seen VALUES (?)', (key,))
                    keep.append(cursor.rowcount == 1)
                database.commit()
                clean, _ = clean_chunk(raw, counts['input_rows'])
                unique = clean.loc[keep]
                write_csv(unique, output, header=counts['input_rows'] == 0)
                eligible = unique['milk_yield'].notna() & unique['event_date'].notna()
                dates.update(unique.loc[eligible, 'event_date'].value_counts().to_dict())
                counts['input_rows'] += len(raw)
                counts['duplicates_removed'] += len(raw) - len(unique)
                counts['unique_rows'] += len(unique)
                print(f"Read {counts['input_rows']:,}; removed {counts['duplicates_removed']:,} duplicates", flush=True)
        database.close()

    ordered = sorted(dates)
    if len(ordered) < 3:
        raise ValueError('Need at least three eligible dates for chronological splitting')
    cumulative = []
    total = 0
    for day in ordered:
        total += dates[day]
        cumulative.append(total)
    train_index = min(range(len(ordered) - 2), key=lambda i: abs(cumulative[i] - total * .70))
    validation_index = min(range(train_index + 1, len(ordered) - 1),
                           key=lambda i: abs(cumulative[i] - total * .85))
    train_end, validation_end = ordered[train_index], ordered[validation_index]
    ranges = {}
    names = ['train', 'validation', 'test', 'missing_yield', 'undated_labeled']
    with ExitStack() as stack:
        files = {name: stack.enter_context((destination / f'{name}.csv').open('x')) for name in names}
        first = True
        for chunk in pd.read_csv(dedup_path, dtype='string', keep_default_na=False, chunksize=chunksize):
            labeled = chunk['milk_yield'].ne('')
            dated = chunk['event_date'].ne('')
            day = chunk['event_date']
            masks = {
                'train': labeled & dated & day.le(train_end),
                'validation': labeled & dated & day.gt(train_end) & day.le(validation_end),
                'test': labeled & dated & day.gt(validation_end),
                'missing_yield': ~labeled,
                'undated_labeled': labeled & ~dated,
            }
            for name, mask in masks.items():
                selected = chunk.loc[mask]
                write_csv(selected, files[name], header=first)
                counts[name] += len(selected)
                valid_dates = selected.loc[selected['event_date'].ne(''), 'event_date']
                if not valid_dates.empty:
                    old = ranges.get(name, [valid_dates.min(), valid_dates.max()])
                    ranges[name] = [min(old[0], valid_dates.min()), max(old[1], valid_dates.max())]
            first = False
    assert sum(counts[name] for name in names) == counts['unique_rows']
    assert counts['input_rows'] == counts['unique_rows'] + counts['duplicates_removed']
    assert ranges['train'][1] < ranges['validation'][0] <= ranges['validation'][1] < ranges['test'][0]
    report = {
        'input': str(source.resolve()), 'counts': dict(counts), 'date_ranges': ranges,
        'requested_fractions': {'train': .70, 'validation': .15, 'test': .15},
        'actual_labeled_dated_fractions': {n: counts[n] / total for n in names[:3]},
        'duplicate_definition': 'Exact equality of all 11 original CSV field values; first occurrence retained.',
        'split_method': 'Chronological date boundaries nearest 70% and 85% cumulative eligible rows; entire dates stay together.',
        'notes': [
            'Raw input preserved; source_row identifies the first original record.',
            'CSV rows retain source order within splits; sort by event_date before temporal feature engineering.',
            'Missing yields are reserved for prediction, never used as training labels.',
            'Known yields without valid dates are excluded from chronological evaluation.',
            'Cows can appear across splits: evaluation targets later observations, not unseen cows.',
            'Fit imputers, encoders and scalers on training data only.',
            'Exclude source_row, *_raw and milk_yield_missing from model features. milk_yield is the target.',
            'Review same-session yield, flow and duration predictors for availability at prediction time.',
        ],
    }
    (destination / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2), flush=True)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=ROOT / 'data/raw/Data_set_prep_assignment_1.csv')
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'data/processed/milk_yield_splits_v1')
    parser.add_argument('--chunksize', type=int, default=100_000)
    args = parser.parse_args()
    if args.chunksize <= 0:
        parser.error('--chunksize must be positive')
    if args.output_dir.resolve().is_relative_to(ROOT / 'data/raw'):
        parser.error('Outputs must be outside data/raw')
    prepare(args.input, args.output_dir, args.chunksize)


if __name__ == '__main__':
    main()
