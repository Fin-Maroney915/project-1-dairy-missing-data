"""Check cross-chunk duplicates, missing labels, and date separation."""
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from clean_data import COLUMNS
from prepare_training_data import prepare


class PrepareDataTest(unittest.TestCase):
    def test_partition_and_duplicates(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            rows = [
                ['001', '1', str(i), 'Pregnant', f'2020-01-{i:02}', '2', '1', '3', '10', '200', '1']
                for i in range(1, 11)
            ]
            rows.append(rows[0].copy())  # Duplicate in a later chunk.
            missing = rows[1].copy()
            missing[8] = ''
            rows.append(missing)
            undated = rows[2].copy()
            undated[4] = 'invalid'
            rows.append(undated)
            different = rows[0].copy()
            different[8] = '11'  # Same cow/date is not necessarily a duplicate.
            rows.append(different)
            source = root / 'raw.csv'
            pd.DataFrame(rows, columns=list(COLUMNS)).to_csv(source, index=False)
            before = source.read_bytes()
            report = prepare(source, root / 'splits', chunksize=3)
            self.assertEqual(source.read_bytes(), before)
            self.assertEqual(report['counts']['duplicates_removed'], 1)
            self.assertEqual(report['counts']['unique_rows'], 13)
            self.assertEqual(report['counts']['missing_yield'], 1)
            self.assertEqual(report['counts']['undated_labeled'], 1)
            splits = {name: pd.read_csv(root / 'splits' / f'{name}.csv', dtype='string')
                      for name in ['train', 'validation', 'test', 'missing_yield', 'undated_labeled']}
            ids = pd.concat(splits.values())['source_row']
            self.assertEqual(len(ids), len(set(ids)))
            self.assertNotIn('11', set(ids))
            self.assertEqual(set(splits['train']['cow_id']), {'001'})
            self.assertLess(splits['train']['event_date'].max(), splits['validation']['event_date'].min())
            self.assertLess(splits['validation']['event_date'].max(), splits['test']['event_date'].min())
            for name in ['train', 'validation', 'test']:
                self.assertFalse(splits[name]['milk_yield'].isna().any())


if __name__ == '__main__':
    unittest.main()
