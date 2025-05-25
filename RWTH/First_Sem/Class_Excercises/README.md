# Machine Learning Pipeline with Categorical and Numerical Features

This project demonstrates how to build a complete machine learning pipeline in Python using **scikit-learn**, capable of handling datasets with both **numerical and categorical features**, including missing values. The pipeline is applied to the classic [auto-mpg dataset](https://archive.ics.uci.edu/ml/datasets/auto+mpg), predicting car fuel efficiency (mpg).

---

## Features

- **Automatic Handling of Missing Values:** Imputes missing numerical data using the median strategy.
- **Categorical Feature Encoding:** One-hot encodes categorical columns.
- **Numerical Feature Scaling:** Standardizes numerical columns for better model performance.
- **Flexible Preprocessing:** Uses `ColumnTransformer` to apply different preprocessing steps to numerical and categorical columns.
- **Model Pipelines:** Combines preprocessing and model training into a single, reusable pipeline.
- **Hyperparameter Tuning:** Performs cross-validated grid search to find the best regularization parameter for Lasso and Ridge regression models.

---

## Workflow Overview

1. **Data Loading and Preparation**
   - Reads the dataset and marks missing values (`?` in `hp` column).
   - Converts the `origin` column to categorical with human-readable labels.

2. **Feature Engineering**
   - Separates features into numerical and categorical types.
   - Defines the target variable (`mpg`).

3. **Train/Test Split**
   - Splits the data into training and testing subsets.

4. **Preprocessing Pipelines**
   - Numerical: Imputation (median) → Standardization.
   - Categorical: One-hot encoding.

5. **ColumnTransformer**
   - Applies respective preprocessing steps to each feature subset.

6. **Model Pipelines**
   - Combines preprocessing with regression models (Lasso or Ridge).

7. **Hyperparameter Tuning**
   - Uses `GridSearchCV` to optimize the regularization parameter (`alpha`).

8. **Model Training**
   - Fits the best model to training data and evaluates on test data.

---

## Installation

Ensure you have Python 3 installed. Then, install required libraries using pip:

```bash
pip install pandas scikit-learn numpy
