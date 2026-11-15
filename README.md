# EV Data Insights

A data mining study of 271,113 electric vehicle registrations in Washington State, with a Streamlit dashboard that presents the findings.

## Overview

This project takes the public Washington State Electric Vehicle Population dataset through a full data mining pipeline: cleaning and feature engineering, OLAP-style analysis, clustering, association rule mining, outlier detection and predictive modeling. Each stage is a separate notebook that saves its figures and result tables, and a Streamlit app brings them together in one dashboard.

## Key findings

- **Adoption is accelerating.** Model years 2022 and later account for 68.9% of all registrations.
- **Tesla leads by a wide margin** with 110,530 vehicles, more than the next nine manufacturers combined.
- **Battery electric vehicles dominate:** 79.8% BEV against 20.2% plug-in hybrid.
- **King County stands alone.** K-Means places it in a cluster by itself, and all four outlier detection methods flag it, with a Z-score of 14.79 on total EVs.
- **Vehicle type is set by design, not geography.** In the predictive model, electric range and CAFV eligibility carry 78.7% of the feature importance, while county and cluster carry almost none.

## Pipeline

| Stage | Notebook | What it does |
|---|---|---|
| 1 | `01_preprocessing.ipynb` | Cleans the raw data, engineers four features (CAFV category, EV type, range category, EV era), and builds standardized county-level profiles |
| 2 | `02_OLAP_Analysis.ipynb` | Answers eight research questions with group-by aggregations, pivot tables and charts |
| 3 | `03_clustering.ipynb` | Groups 246 counties with K-Means, using the elbow method and silhouette scores, and visualizes the clusters with PCA |
| 4 | `04_association_rules.ipynb` | Mines manufacturer co-occurrence patterns with Apriori, treating each county as a transaction |
| 5 | `05_outlier_detection.ipynb` | Compares IQR, Z-score, Isolation Forest and Local Outlier Factor, then builds a consensus across methods |
| 6 | `06_predictive_model.ipynb` | Predicts BEV or PHEV with a Decision Tree baseline and a Random Forest, with 5-fold cross-validation |

## Results

**Clustering** (K-Means, K = 4, silhouette score 0.44)

| Cluster | Counties |
|---|---|
| Low adoption, BEV-leaning | 156 |
| Low adoption, PHEV-dominant | 59 |
| High adoption, mixed fleet | 30 |
| King County | 1 |

**Association rules:** 656 frequent itemsets and 1,240 rules across 47 manufacturers, plus 35 make-to-EV-type rules and 37 make-to-cluster rules.

**Outlier detection:** 70 counties flagged by at least one method, 8 by three methods, and King County by all four.

**Predictive model** (54,221 test vehicles)

| Model | Accuracy | F1 | ROC-AUC |
|---|---|---|---|
| Decision Tree, depth 5 | 99.95% | 0.9995 | 1.0000 |
| Random Forest, 200 trees | 99.996% | 1.0000 | 1.0000 |

The near-perfect scores are expected: electric range and CAFV eligibility almost fully determine whether a vehicle is a BEV or a PHEV. The useful result is the feature importance ranking, which shows that location adds nothing once vehicle attributes are known.

## Notes on the data

The dataset lists 246 distinct counties because it includes vehicles registered in Washington whose owners live in other states. Most of those counties have only a handful of vehicles, which shapes the two low-adoption clusters.

## Dashboard

`ev_app.py` is a Streamlit app with seven pages: an overview and one page per pipeline stage. It reads the saved figures in `outputs/figures`, so it runs without the raw data.

```bash
pip install streamlit pillow pandas numpy
streamlit run ev_app.py
```

## Running the analysis

1. Install the dependencies:

   ```bash
   pip install pandas numpy matplotlib seaborn scikit-learn scipy mlxtend jupyter
   ```

2. Download the [Electric Vehicle Population Data](https://catalog.data.gov/dataset/electric-vehicle-population-data) as a CSV and save it in the project folder as `Electric_Vehicle_Population_Data.csv`. The data files are not stored in this repository because of their size.
3. Run the notebooks in this order: 01, 03, 02, 04, 05, 06. The OLAP notebook uses the cluster assignments produced by the clustering notebook, so clustering runs first.

Figures are written to `outputs/figures` and result tables to `outputs/results`.

## Repository structure

```
├── 01_preprocessing.ipynb
├── 02_OLAP_Analysis.ipynb
├── 03_clustering.ipynb
├── 04_association_rules.ipynb
├── 05_outlier_detection.ipynb
├── 06_predictive_model.ipynb
├── ev_app.py
└── outputs
    ├── figures
    └── results
```

## Tech stack

Python, pandas, NumPy, scikit-learn, mlxtend, SciPy, Matplotlib, seaborn, Streamlit

## Author

Soundarya Lahari Singaraju

- GitHub: [laharisingaraju-19](https://github.com/laharisingaraju-19)
- LinkedIn: [soundaryalaharisingaraju](https://www.linkedin.com/in/soundaryalaharisingaraju)
