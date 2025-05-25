
# Missing Data and Imputation

A Jupyter Notebook project exploring methods for detecting, analyzing, and imputing missing data in tabular datasets. This notebook is designed as a **class exercise** to demonstrate practical techniques in Python using `pandas`, with clear examples and visualizations.

---

## 📚 Table of Contents

- [Project Overview](#project-overview)
- [Dataset](#dataset)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Results](#results)
- [Contributing](#contributing)
- [Acknowledgments](#acknowledgments)
- [License](#license)

---

## 📘 Project Overview

This notebook investigates how to detect and handle missing values in datasets, with a focus on various imputation techniques. Topics covered include:

- Detecting missing values (e.g., `NaN` in pandas)
- Summarizing missing data patterns
- Imputation strategies:
  - Mean/Median imputation
  - Mode imputation
  - Model-based imputation (optional)
- Assessing how imputation affects data quality and analysis

> 🧑‍🏫 This notebook serves both as a **learning resource** and a **class exercise** to understand missing data handling in real-world scenarios.

---

## 📊 Dataset

The notebook uses the `auto-mpg-orig.csv` dataset, which includes features such as:

- `mpg`: Fuel efficiency
- `cylinders`, `displacement`, `horsepower`, `weight`, `acceleration`
- `year`: Model year
- `origin`: Car origin (1 = USA, 2 = Europe, 3 = Japan)

Some records contain **missing values** (notably in the `horsepower` column), which are imputed during the exercise.

---

## 🛠️ Installation

You’ll need Python 3.x and the following libraries:

```bash
pip install pandas numpy matplotlib scikit-learn
