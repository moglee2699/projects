# Introduction to Pandas

This repository contains a Jupyter Notebook that provides an introduction to the **pandas** library for data analysis in Python. It walks through a typical data science workflow using the **auto-mpg.csv** dataset, covering data loading, cleaning, exploration, visualization, and basic analysis.

## 📘 Overview

This notebook introduces key pandas functionalities with practical examples using a real-world dataset. You will learn how to:
- Load and inspect datasets
- Clean and preprocess data
- Perform exploratory data analysis (EDA)
- Visualize relationships and trends
- Engineer features for modeling
- Calculate basic statistics and correlations

---

## 📊 Dataset: `auto-mpg.csv`

The dataset contains information about various cars and their fuel efficiency. The target variable is **mpg** (miles per gallon), and features include:

- `cylinders`: Number of engine cylinders  
- `displacement`: Engine size (in cubic inches)  
- `horsepower`: Engine power  
- `weight`: Vehicle weight (in pounds)  
- `acceleration`: Time to reach 60 mph  
- `year`: Model year (last two digits)  
- `origin`: Car origin (1 = North America, 2 = Europe, 3 = Japan)  

> Note: The `origin` variable is later mapped to categorical values like `America`, `Europe`, and `Japan`.

---

## 📦 Requirements

- Python 3.x
- pandas
- matplotlib

Install the dependencies using:

```bash
pip install pandas matplotlib

