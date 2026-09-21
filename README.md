# Project 1: Dairy Cow Missing-Data Prediction

## Project overview

This mini project investigates missing information in a dairy-cow milk-yield dataset. Each observation represents a cow record identified by a tag or cow ID and includes a milk-yield measurement. Some observations have a missing cow ID, a missing milk yield, or both. The project will first inspect the data and determine the amount, location, and possible causes of missingness. It will then develop and evaluate a reproducible method for estimating missing milk yields. Missing cow IDs will be handled separately because an ID is not an ordinary numerical value: IDs will be recovered only when other fields or record patterns provide strong evidence of the correct cow. Ambiguous IDs will remain missing rather than being guessed.

### Research question

How accurately can known cow and production information predict missing milk-yield values, and when can incomplete records be linked confidently to the correct cow?

### Planned workflow

1. **Data intake and lineage:** Preserve the original CSV unchanged in `data/raw/`. Record its source, date received, row count, column names, units, and any cleaning decisions. The raw data will not be committed because the repository is public.
2. **Inspection and cleaning:** Use `notebooks/01_data_inspection.ipynb` to examine data types, duplicate rows, invalid values, missingness, cow-level record counts, yield distributions, and observations over time. Create a cleaned copy in `data/processed/`; never overwrite the raw file.
3. **Baseline:** Compare model performance with simple approaches such as the herd median, each cow's median, and interpolation between a cow's neighboring measurements.
4. **Feature engineering:** Where available, create features such as previous yield, rolling mean, date, month, days in milk, lactation number, parity, milking session, and time since the previous observation. Lagged variables will use only earlier records to prevent data leakage.
5. **Modeling:** Treat milk yield as a regression problem. Begin with a simple linear model and a tree-based model such as Random Forest. Select the simplest model that produces a meaningful improvement over the baseline. Treat missing cow ID as record linkage or classification only if the dataset contains identifying predictors such as time, station, session, lactation, or surrounding records.
6. **Testing:** Artificially mask a sample of known yields, make predictions, and compare them with the true values using MAE and RMSE. Use a chronological train/test split so that later records form the test set. If the goal changes to predicting entirely new cows, use a cow-level grouped split instead.
7. **Final output:** Keep original and predicted values in different columns, include a prediction-method or confidence column, summarize performance and limitations, and make the notebook reproducible from a fresh clone after the private data file is added locally.

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
