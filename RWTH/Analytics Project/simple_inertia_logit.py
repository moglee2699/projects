# simple_inertia_logit.py
import numpy as np
import pandas as pd
from biogeme import biogeme as bio
from biogeme import database as db
from biogeme.expressions import Beta, Variable
from biogeme.models import logit

# -----------------------------
# 1) LOAD & PREP
# -----------------------------
CSV_PATH = r'c:\Users\52812\Desktop\RWTH\2nd_semester_RWTH\Analytics_project\Project_final\dataset\DataSetModel0NA6Alt.csv'
df = pd.read_csv(CSV_PATH, sep=';')

# Standardize names
if 'CHOICE' not in df.columns and 'Choice' in df.columns:
    df = df.rename(columns={'Choice': 'CHOICE'})
if 'ClubNT' in df.columns:
    df = df.rename(columns={'ClubNT': 'clubNT'})

# Keep only valid choices 1..6
df['CHOICE'] = pd.to_numeric(df['CHOICE'], errors='coerce')
df = df[df['CHOICE'].between(1, 6)].copy()

# Build inertia terms (panel-aware if ID exists)
if 'ID' in df.columns:
    df['prev_choice'] = df.groupby('ID')['CHOICE'].shift(1).fillna(0)
    df['has_inertia'] = df['ID'].duplicated().astype(int)
else:
    df['prev_choice'] = df['CHOICE'].shift(1).fillna(0)
    df['has_inertia'] = (df.index > 0).astype(int)

# Minimal columns only → avoids Biogeme complaining about object dtypes
keep_cols = ['CHOICE', 'prev_choice', 'has_inertia']
if 'ID' in df.columns:
    keep_cols.insert(0, 'ID')
df_min = df[keep_cols].copy()

# Cast to plain NumPy dtypes (not pandas nullable Int64)
df_min['CHOICE'] = pd.to_numeric(df_min['CHOICE'], errors='coerce').fillna(0).astype(np.int64)
df_min['prev_choice'] = pd.to_numeric(df_min['prev_choice'], errors='coerce').fillna(0).astype(np.int64)
df_min['has_inertia'] = pd.to_numeric(df_min['has_inertia'], errors='coerce').fillna(0).astype(np.int64)
if 'ID' in df_min.columns:
    df_min['ID'] = pd.to_numeric(df_min['ID'], errors='coerce').fillna(-1).astype(np.int64)

print("Using columns and dtypes:\n", df_min.dtypes)
print(df_min.head())

# -----------------------------
# 2) BIOGEME SETUP
# -----------------------------
database = db.Database('penalty_inertia_only', df_min)

choice = Variable('CHOICE')
prev_choice = Variable('prev_choice')
has_inertia = Variable('has_inertia')

# -----------------------------
# 3) PARAMETERS (fix ASC1 for ID)
# -----------------------------
ASC1 = Beta('ASC1', 0, None, None, 1)  # fixed base
ASC2 = Beta('ASC2', 0, None, None, 0)
ASC3 = Beta('ASC3', 0, None, None, 0)
ASC4 = Beta('ASC4', 0, None, None, 0)
ASC5 = Beta('ASC5', 0, None, None, 0)
ASC6 = Beta('ASC6', 0, None, None, 0)
b_inertia = Beta('b_inertia', 0, None, None, 0)

# -----------------------------
# 4) UTILITIES: inertia only
# -----------------------------
V = {
    1: ASC1 + b_inertia * (prev_choice == 1) * has_inertia,
    2: ASC2 + b_inertia * (prev_choice == 2) * has_inertia,
    3: ASC3 + b_inertia * (prev_choice == 3) * has_inertia,
    4: ASC4 + b_inertia * (prev_choice == 4) * has_inertia,
    5: ASC5 + b_inertia * (prev_choice == 5) * has_inertia,
    6: ASC6 + b_inertia * (prev_choice == 6) * has_inertia,
}
avail = {i: 1 for i in range(1, 7)}

# -----------------------------
# 5) ESTIMATE
# -----------------------------
logprob = logit(V, avail, choice)
bgm = bio.BIOGEME(database, logprob)
bgm.modelName = 'mnl_inertia_only'

results = bgm.estimate()

# -----------------------------
# 6) OUTPUT
# -----------------------------
print("\n=== Estimated Parameters ===")
print(results.getEstimatedParameters())

try:
    print("\n=== General Statistics ===")
    print(results.getGeneralStatistics())
except Exception:
    pass

