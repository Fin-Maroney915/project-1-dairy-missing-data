# Project 1: Dairy Cow Missing-Data Prediction

## Project overview

This mini project investigates missing information in a dairy-cow milk-yield dataset. Each observation represents a cow record identified by a tag or cow ID and includes a milk-yield measurement. Some observations have a missing cow ID, a missing milk yield, or both. The project will first inspect the data and determine the amount, location, and possible causes of missingness. It will then develop and evaluate a reproducible method for estimating missing milk yields. Missing cow IDs will be handled separately because an ID is not an ordinary numerical value: IDs will be recovered only when other fields or record patterns provide strong evidence of the correct cow. Ambiguous IDs will remain missing rather than being guessed.

### Research question

How accurately can known cow and production information predict missing milk-yield values, and when can incomplete records be linked confidently to the correct cow?

### Planned workflow

1. **Data intake and lineage:** Preserve the original CSV unchanged in `data/raw/`. Record its source, date received, row count, column names, units, and any cleaning decisions. The raw data will not be committed because the repository is public.
2. **Inspection and cleaning:** Use `notebooks/01_data_inspection.ipynb` to examine data types, duplicate rows, invalid values, missingness, cow-level record counts, yield distributions, and observations over time. Standardize column names and data types, convert confirmed zero placeholders to missing values, and flag implausible measurements and statistical outliers. Create a cleaned copy in `data/processed/`; never overwrite the raw file.
3. **Baseline:** Compare model performance with simple approaches such as the herd median, each cow's median, and interpolation between a cow's neighboring measurements.
4. **Feature engineering:** Where available, create features such as previous yield, rolling mean, date, month, days in milk, lactation number, parity, milking session, and time since the previous observation. Lagged variables will use only earlier records to prevent data leakage.
5. **Modeling:** Treat the selected milk-yield or milk-flow variable as a regression target. Compare median and interpolation baselines with regularized linear regression, Random Forest, and a gradient-boosted tree model. Select the simplest model that produces a meaningful and repeatable improvement over the baselines. Treat missing cow ID as a separate record-linkage problem rather than as an ordinary numerical imputation task.
6. **Testing:** Separate records with genuinely missing target values before model development. Split records with observed targets into approximately 70% training, 15% validation, and 15% testing using cow ID as the grouping variable so that a cow cannot appear in more than one split. Use grouped cross-validation within the training set and a secondary chronological holdout to test performance on later records. Artificially mask observed targets, predict them, and compare predictions with the known values using MAE, RMSE, and R-squared.
7. **Final output:** Keep original and predicted values in different columns, include a prediction-method or confidence column, summarize performance and limitations, and make the notebook reproducible from a fresh clone after the private data file is added locally.

### Data-cleaning strategy

The raw dataset will remain unchanged. Cleaning will be performed on a copy, and each transformation will be summarized with before-and-after row counts.

1. Convert column names to lowercase `snake_case`, parse the event-date column as a date, and convert measurement columns to numeric values without altering cow IDs.
2. Count existing `NaN` values separately from zero values. In continuous milk-measurement columns where the data documentation or inspection confirms that zero means the measurement is missing, identify zeros with `notna() & eq(0)`, create a corresponding `*_was_zero_missing` indicator, and convert only those zeros to `NaN`. The project will not use `fillna(0)`.
3. Remove exact duplicate rows and review duplicate cow/date/session combinations before deciding whether they represent repeated records or valid separate milkings.
4. Apply biological and measurement checks to impossible values, such as negative yield, flow, or duration. Questionable values will be flagged before any rows are excluded.
5. Calculate z-scores only for continuous milk-measurement columns. Cow ID, dates, lactation number, days in milk, reproduction status, and other identifiers or categorical variables will not be included in the z-score rule. A row will be flagged when any selected measurement has an absolute z-score greater than 3. For modeling, means and standard deviations will be estimated from the training set only, and only training rows will be filtered. Validation and test rows will remain unchanged so that evaluation reflects real data.
6. Preserve missingness and outlier indicators as potential predictors. Missing cow IDs will be recovered only when record patterns provide strong evidence; ambiguous IDs will remain missing.

### Train, validation, and test strategy

Rows with an observed target will form the model-development dataset. Rows with a missing target will be held aside as the final prediction dataset and will not be used to score model accuracy. The observed-target data will be divided into approximately 70% training, 15% validation, and 15% testing with a grouped split based on cow ID. This prevents records from the same cow from appearing in multiple sets and reduces overly optimistic performance caused by cow-specific leakage.

All learned preprocessing steps—including numeric imputation, category encoding, scaling, z-score thresholds, and feature selection—will be fitted using the training data only. Grouped cross-validation will be used for model tuning. The validation set will guide model and hyperparameter selection, while the test set will be used once for the final comparison. A secondary chronological test, using earlier observations for training and later observations for evaluation, will check whether performance holds when predicting future records. Lagged and rolling features will be calculated using only information available before each observation.

### Modeling techniques

The project will compare the following methods:

- **Baselines:** herd median, lactation-stage median, cow-level median when cow history is available, and linear interpolation between a cow's neighboring observed measurements.
- **Regularized linear regression:** a Ridge or Elastic Net model will provide an interpretable benchmark and test whether the target can be predicted from mostly linear relationships.
- **Random Forest regression:** this model can capture nonlinear effects and interactions among days in milk, lactation number, session yield, duration, reproduction status, and recent cow history without requiring strong distributional assumptions.
- **Gradient-boosted trees:** HistGradientBoosting, XGBoost, or CatBoost will be tested for improved performance on nonlinear relationships. CatBoost is especially relevant if categorical predictors are retained, while model choice will depend on package compatibility and cross-validation results.

Candidate predictors include days in milk, lactation number, reproduction status, event-date features, session duration, other observed yield or flow measurements, prior yield, rolling averages, and time since the previous observation. Features unavailable at the time a prediction would be made will be excluded to avoid leakage. MAE will be the primary metric because it is easy to interpret in the target's units; RMSE will show sensitivity to large errors, and R-squared will be reported as a secondary measure. Performance will also be checked across lactation groups and stages of lactation. The final model will be the simplest approach that consistently improves on the baselines without relying on leaked information.

### Timeline

| Stage | Target date | Deliverable |
|---|---|---|
| Repository setup and initial inspection | Sept. 21–23 | Public repository structure, README, license, `.gitignore`, and inspection notebook |
| Wednesday discussion and plan revision | Sept. 23 | Confirm prediction target, available features, missingness assumptions, and testing design |
| Cleaning and exploratory analysis | Sept. 24–27 | Data dictionary, missingness summary, cleaned dataset, and initial figures |
| Baseline and feature engineering | Sept. 28–30 | Baseline results and leakage-safe predictor set |
| Model training and validation | Oct. 1–4 | Model comparison using MAE/RMSE and chronological testing |
| Final analysis and documentation | Oct. 5–7 | Final notebook, results, limitations, and polished README |

Dates after the Wednesday discussion may be adjusted to match the course deadline.

### Computing environment

The project will be completed **locally** in **Visual Studio Code** using its Jupyter Notebook extension and a Python virtual environment. Git and GitHub will provide version control and a public record of the code. The dataset will remain local and will not be uploaded to GitHub. If cloud computing becomes necessary, a copy of the code may be run in Google Colab, but the primary reproducible environment will remain VS Code.

### Data lineage and reproducibility

The original dataset should be saved locally as `data/raw/Data_set_prep_assignment_1.csv`. This path is ignored by Git. Derived datasets belong in `data/processed/`, while charts and model results belong in `outputs/`. Every transformation should be performed in code and explained in Markdown cells. Important decisions, including removed records, unit conversions, outlier rules, and imputation methods, will be documented. No predicted value will silently replace an observed value.

### Anticipated risks

- Milk yield alone is unlikely to identify a cow reliably.
- Rows missing both ID and yield may not contain enough information to recover either value.
- Randomly splitting repeated cow observations may leak cow-specific or future information into testing.
- Missingness may not be random; equipment or tag failures could systematically affect certain cows or times.
- A complicated model may appear accurate without outperforming a cow-level median or interpolation baseline.

## Repository structure

```text
project-1-dairy-missing-data/
├── data/
│   ├── raw/                 # Original private data; ignored by Git
│   └── processed/           # Reproducible derived data; ignored by default
├── notebooks/
│   └── 01_data_inspection.ipynb
├── outputs/
│   └── figures/
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## Naming convention

- Use lowercase `snake_case` for Python variables, functions, and data columns: `milk_yield`, `cow_id`.
- Number notebooks in execution order: `01_data_inspection.ipynb`, `02_cleaning.ipynb`, `03_modeling.ipynb`.
- Use lowercase descriptive filenames with underscores and no spaces.
- Keep the raw dataset named `Data_set_prep_assignment_1.csv`.
- Name derived datasets by stage and version, such as `milk_yield_cleaned_v1.csv`.
- Name figures by content, such as `missing_values_by_column.png`.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Place the private CSV at `data/raw/Data_set_prep_assignment_1.csv`, open the repository in VS Code, select the `.venv` Python kernel, and run the inspection notebook from top to bottom.

## Clean the raw data

The supplied file is `data/raw/Data_set_prep_assignment_1.csv`. After installing
requirements, run from the project root:

```bash
python3 scripts/clean_data.py
```

The script processes 100,000 records at a time so the approximately 903 MB raw
file does not need to fit in memory. It writes:

- `data/processed/milk_yield_cleaned_v1.csv`: cleaned records, original fields in
  `*_raw` columns, invalid-value flags, and a `source_row` record number.
- `data/processed/milk_yield_cleaned_v1.report.json`: row counts, missingness,
  invalid-value counts, date range, and cleaning decisions.

Both outputs remain private under the existing Git ignore rules. Original fields
make the output larger than the input. Existing outputs are never overwritten;
choose a new output name for another run:

```bash
python3 scripts/clean_data.py --input data/raw/Data_set_prep_assignment_1.csv --output data/processed/milk_yield_cleaned_v2.csv --chunksize 50000
```

`AnimalId` becomes `cow_id`, `YieldSession` becomes `milk_yield`, and other
columns use snake_case (see the report for the complete mapping). Cow IDs remain
text to preserve large signed identifiers exactly. The cleaner trims whitespace,
normalizes missing tokens, parses numeric values and dates, and flags invalid
values while retaining their original text. It retains zeros, high measurements,
unknown reproduction statuses, all incomplete records, and possible duplicates.
It does not infer IDs, impute yields, convert units, sort observations, or remove
outliers. Confirm yield units and valid ranges with the data owner before modeling.
A failed run can leave a partial CSV; a successful run also creates its report.

When loading the cleaned CSV, explicitly preserve IDs as text:

```python
import pandas as pd

# Use chunksize=100_000 instead of nrows to iterate over the entire dataset.
df = pd.read_csv(
    "data/processed/milk_yield_cleaned_v1.csv",
    dtype={"cow_id": "string", "cow_id_raw": "string"},
    parse_dates=["event_date"],
    nrows=100_000,
)
```

The inspection notebook is configured for the supplied raw filename and columns.
It reads the first 100,000 records and preserves IDs as text; its summaries describe
that preview. Use the cleaning report for full-dataset missingness counts.

## License

The code and documentation are released under the MIT License. The dairy dataset is not included and remains subject to the terms provided by its owner.

## Deduplicate and split for modeling

Run the preparation script directly on the raw CSV (the earlier cleaned CSV is
not required):

```bash
python3 scripts/prepare_training_data.py
```

This creates a new private directory, `data/processed/milk_yield_splits_v1/`:

- `deduplicated.csv`: cleaned data with exact duplicate source records removed.
- `train.csv`, `validation.csv`, `test.csv`: approximately 70%, 15%, and 15% of
  records with observed, valid milk yields and valid dates, ordered by date range.
- `missing_yield.csv`: records reserved for later yield prediction.
- `undated_labeled.csv`: observed yields without valid dates, excluded from the
  chronological splits.
- `report.json`: counts, actual split fractions, date ranges, and decisions.

Duplicates must match all 11 original field values exactly. The first occurrence
is retained, including its `source_row`. Distinct sessions for the same cow and
date remain. Deduplication checks the entire dataset across chunk boundaries
using a temporary disk-backed index. The raw file and earlier cleaned files are
preserved. Whitespace or numeric-format differences are not exact duplicates.

The split keeps entire dates together and places earlier dates in training and
later dates in validation and testing. Fractions can differ from 70/15/15 to avoid
sharing a date across partitions. Rows retain their original order inside each
file; sort by date before constructing temporal features. Cows may occur in
multiple splits, consistent with predicting later measurements for this herd.

Use `milk_yield` as the target. Select predictor columns explicitly: do not feed
`source_row`, any `*_raw` columns, or `milk_yield_missing` into the model. Review
whether same-session flow, duration, and first-two-minute yield are available
when a yield needs predicting. Fit preprocessing and imputers on training data
only, tune on validation, and reserve test data for final evaluation. Preserve
cow IDs with `dtype={"cow_id": "string", "cow_id_raw": "string"}` when loading.

Choose a fresh `--output-dir` to rerun. Existing directories are never overwritten;
a run is complete only when `report.json` exists. Use `--chunksize 50000` to reduce
memory use. Verify the partitioning logic with:

```bash
python3 -m unittest discover -s tests
```


## Context imputation results

The final dataset contains 4,688,514 rows and 23 columns.

High-confidence imputation results:

- Reproduction status: 939,749 missing values imputed
- Days in milk: 22,417 high-confidence predictions retained
- Lactation number: 149,541 high-confidence predictions retained
- Cow ID was not imputed because validation accuracy was insufficient
- Predictions that did not satisfy the selected confidence thresholds were left missing

Missing values remaining:

- Cow ID: 939,749
- Average milk flow: 100
- Lactation number: 790,208
- Days in milk: 917,334
- Reproduction status: 0

The final dataset was excluded from Git because of its size and must be generated locally by running the notebooks.