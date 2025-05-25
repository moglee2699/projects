# README: Online Shoppers Purchasing Intention Prediction  
**First Semester Project**

## Project Overview  
This project focuses on predicting whether an online shopper will make a purchase (Revenue = 1) or not (Revenue = 0) based on their session data. Using various session-based features like time spent on pages, bounce rates, exit rates, and visitor type, we build classification models to identify purchasing intentions. This helps e-commerce businesses optimize user experience, personalize marketing, and increase sales conversion.

## Team Members  
- 471538 - Abishai Srinivasan  
- 469304 - Gurusaran Sivakumar  
- 469312 - Keerthana Karunanithi  
- 470389 - Subhiksha Arcot Praburam  

## Dataset Description  
- Total rows: 12,330  
- Features: 18 (numerical + categorical)  

### Numerical Features:  
Administrative, Administrative_Duration, Informational, Informational_Duration, ProductRelated, ProductRelated_Duration, BounceRates, ExitRates, PageValues, SpecialDay

### Categorical Features:  
Month, OperatingSystems, Browser, Region, TrafficType, VisitorType, Weekend (binary), Revenue (target)

## Project Motivation & Benefits  
- Boost sales conversion by targeting likely buyers  
- Personalize user experience with real-time recommendations  
- Optimize marketing spend on high-conversion visitors  
- Identify site improvement areas via bounce and exit rates  
- Scalable solution for large datasets and businesses  

## Methodology  

### Data Preprocessing:  
- Impute missing categorical values with most frequent  
- One-hot encode categorical features  
- Standardize numerical features with StandardScaler  

### Model Building:  
- Classifiers: Support Vector Machine (SVM), Logistic Regression  
- Hyperparameter tuning with GridSearchCV  
- Feature selection using SelectKBest  
- Robust evaluation with StratifiedKFold cross-validation  

### Pipeline:  
- ColumnTransformer for preprocessing  
- Feature selection  
- Classifier training  

## Evaluation Metrics & Results  

| Metric    | SVM (Recall-Optimized) |
|-----------|------------------------|
| Accuracy  | 88.81%                 |
| Recall    | 70.85%                 |
| Precision | 64.86%                 |
| F1 Score  | 67.72%                 |

## Key Features Impacting Purchase Prediction  
PageValues, ProductRelated, ProductRelated_Duration, ExitRates, Informational_Duration, Informational, BounceRates, Administrative, Weekend, TrafficType  

## Usage Instructions  

### Requirements:  
Python 3.x, pandas, numpy, seaborn, matplotlib, plotly, scikit-learn, joblib  

### Running the Project:  
1. Place the dataset file `online_shoppers_intention.csv` in your working directory.  
2. Run the Jupyter notebook `Project_1_Online_Shopper_Purchasing_Intention_Final.ipynb`.  
3. The notebook covers all steps from data loading, preprocessing, model training, evaluation, to feature importance.  
4. Expected runtime: approx. 10–13 minutes.  

## Outputs  
- Model performance metrics  
- Feature importance ranking  
- Session-wise purchase prediction results  

## Notes  
- Modular codebase, adaptable to other binary classification problems  
- Flexible to try different feature selections or classifiers

