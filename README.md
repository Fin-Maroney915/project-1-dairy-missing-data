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

The original dataset should be saved locally as `data/raw/project_1_ANSC_4040_dataset.csv`. This path is ignored by Git. Derived datasets belong in `data/processed/`, while charts and model results belong in `outputs/`. Every transformation should be performed in code and explained in Markdown cells. Important decisions, including removed records, unit conversions, outlier rules, and imputation methods, will be documented. No predicted value will silently replace an observed value.

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
- Keep the raw dataset named `project_1_ANSC_4040_dataset.csv`.
- Name derived datasets by stage and version, such as `milk_yield_cleaned_v1.csv`.
- Name figures by content, such as `missing_values_by_column.png`.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Place the private CSV at `data/raw/project_1_ANSC_4040_dataset.csv`, open the repository in VS Code, select the `.venv` Python kernel, and run the inspection notebook from top to bottom.

## License

The code and documentation are released under the MIT License. The dairy dataset is not included and remains subject to the terms provided by its owner.
