# mnl_inertia_altFE_players3.py
import numpy as np
import pandas as pd
from biogeme import biogeme as bio
from biogeme import database as db
from biogeme.expressions import Beta, Variable
from biogeme.models import logit

# -----------------------------
# CONFIG
# -----------------------------
PLAYER_FE_IDS = [6, 89, 295]  # Aguero, Cavani, Messi
CSV_PATH = r'c:\Users\52812\Desktop\RWTH\2nd_semester_RWTH\Analytics_project\Project_final\dataset\DataSetModel0NA6Alt.csv'

# -----------------------------
# 1) LOAD & PREP
# -----------------------------
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

# Minimal columns only (avoid object dtype issues)
keep_cols = ['CHOICE', 'prev_choice', 'has_inertia']
if 'ID' in df.columns:
    keep_cols.insert(0, 'ID')
df_min = df[keep_cols].copy()

# Cast to plain NumPy dtypes
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
database = db.Database('penalty_inertia_altFE_3players', df_min)

choice      = Variable('CHOICE')
prev_choice = Variable('prev_choice')
has_inertia = Variable('has_inertia')
id_var      = Variable('ID')

# -----------------------------
# 3) PARAMETERS
# -----------------------------
# ASCs: fix ASC1 as baseline for identification
ASC1 = Beta('ASC1', 0, None, None, 1)  # fixed
ASC2 = Beta('ASC2', 0, None, None, 0)
ASC3 = Beta('ASC3', 0, None, None, 0)
ASC4 = Beta('ASC4', 0, None, None, 0)
ASC5 = Beta('ASC5', 0, None, None, 0)
ASC6 = Beta('ASC6', 0, None, None, 0)

# Alt-specific inertia coefficients
b_inertia1 = Beta('b_inertia1', 0, None, None, 0)
b_inertia2 = Beta('b_inertia2', 0, None, None, 0)
b_inertia3 = Beta('b_inertia3', 0, None, None, 0)
b_inertia4 = Beta('b_inertia4', 0, None, None, 0)
b_inertia5 = Beta('b_inertia5', 0, None, None, 0)
b_inertia6 = Beta('b_inertia6', 0, None, None, 0)

b_inertia = {
    1: b_inertia1, 2: b_inertia2, 3: b_inertia3,
    4: b_inertia4, 5: b_inertia5, 6: b_inertia6,
}

# Player × Alternative fixed effects
# Create FE param for each (player, alt). Fix one for identification: FE_p295_A1 = 0
FE_params = {}
for pid in PLAYER_FE_IDS:
    for alt in [1, 2, 3, 4, 5, 6]:
        name = f'FE_p{pid}_A{alt}'
        fixed = 1 if alt == 1 else 0   # <- changed: fix alt 1 for everyone
        FE_params[(pid, alt)] = Beta(name, 0, None, None, fixed)

def player_fe_for_alt(alt_index):
    # Sum FE for players matching this alt
    terms = 0
    for pid in PLAYER_FE_IDS:
        terms += FE_params[(pid, alt_index)] * (id_var == pid)
    return terms

# -----------------------------
# 4) UTILITIES
# -----------------------------
V = {
    1: ASC1 + b_inertia[1] * (prev_choice == 1) * has_inertia + player_fe_for_alt(1),
    2: ASC2 + b_inertia[2] * (prev_choice == 2) * has_inertia + player_fe_for_alt(2),
    3: ASC3 + b_inertia[3] * (prev_choice == 3) * has_inertia + player_fe_for_alt(3),
    4: ASC4 + b_inertia[4] * (prev_choice == 4) * has_inertia + player_fe_for_alt(4),
    5: ASC5 + b_inertia[5] * (prev_choice == 5) * has_inertia + player_fe_for_alt(5),
    6: ASC6 + b_inertia[6] * (prev_choice == 6) * has_inertia + player_fe_for_alt(6),
}
avail = {i: 1 for i in range(1, 7)}

# -----------------------------
# 5) ESTIMATE
# -----------------------------
logprob = logit(V, avail, choice)
bgm = bio.BIOGEME(database, logprob)
bgm.modelName = 'mnl_inertia_altFE_3players'

results = bgm.estimate()

# -----------------------------
# 6) OUTPUT
# -----------------------------
print("\n=== Estimated Parameters ===")
try:
    print(results.get_estimated_parameters())
except Exception:
    print(results.getEstimatedParameters())

try:
    print("\n=== General Statistics ===")
    print(results.get_general_statistics())
except Exception:
    print(results.getGeneralStatistics())
