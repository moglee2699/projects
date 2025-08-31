# mnl_inertia_altFE_altSPEC_covariates.py
import numpy as np
import pandas as pd
from biogeme import biogeme as bio
from biogeme import database as db
from biogeme.expressions import Beta, Variable
from biogeme.models import logit

# ---------------------------------
# CONFIG – edit these
# ---------------------------------
CSV_PATH = r'c:\Users\52812\Desktop\RWTH\2nd_semester_RWTH\Analytics_project\Project_final\dataset\DataSetModel0NA6Alt.csv'
PLAYER_FE_IDS = [295, 89, 6]   # e.g., Messi, Cavani, Agüero (order matters for FE identification)
STANDARDIZE_FOOT = True        # z-score foot for stability

# ---------------------------------
# 1) LOAD & PREP
# ---------------------------------
df = pd.read_csv(CSV_PATH, sep=';')

# Canonical column names
if 'CHOICE' not in df.columns and 'Choice' in df.columns:
    df = df.rename(columns={'Choice': 'CHOICE'})
if 'ClubNT' in df.columns:
    df = df.rename(columns={'ClubNT': 'clubNT'})

# Keep valid choices 1..6
df['CHOICE'] = pd.to_numeric(df['CHOICE'], errors='coerce')
df = df[df['CHOICE'].between(1, 6)].copy()

# Panel-aware inertia terms
if 'ID' in df.columns:
    df['prev_choice'] = df.groupby('ID')['CHOICE'].shift(1).fillna(0)
    df['has_inertia'] = df['ID'].duplicated().astype(int)
else:
    df['prev_choice'] = df['CHOICE'].shift(1).fillna(0)
    df['has_inertia'] = (df.index > 0).astype(int)

# Ensure covariates exist
for col in ['foot', 'RepGK']:
    if col not in df.columns:
        raise RuntimeError(f"Column '{col}' not found in data.")

# Numeric & optional standardization
if STANDARDIZE_FOOT:
    mu = pd.to_numeric(df['foot'], errors='coerce').mean()
    sd = pd.to_numeric(df['foot'], errors='coerce').std()
    df['foot'] = (pd.to_numeric(df['foot'], errors='coerce') - mu) / (sd + 1e-9)
else:
    df['foot'] = pd.to_numeric(df['foot'], errors='coerce')

df['RepGK'] = pd.to_numeric(df['RepGK'], errors='coerce').fillna(0)

# Minimal columns only
keep_cols = ['CHOICE', 'prev_choice', 'has_inertia', 'foot', 'RepGK']
if 'ID' in df.columns:
    keep_cols.insert(0, 'ID')
df_min = df[keep_cols].copy()

# Cast to plain NumPy dtypes
df_min['CHOICE'] = pd.to_numeric(df_min['CHOICE'], errors='coerce').fillna(0).astype(np.int64)
df_min['prev_choice'] = pd.to_numeric(df_min['prev_choice'], errors='coerce').fillna(0).astype(np.int64)
df_min['has_inertia'] = pd.to_numeric(df_min['has_inertia'], errors='coerce').fillna(0).astype(np.int64)
df_min['foot'] = pd.to_numeric(df_min['foot'], errors='coerce').fillna(0).astype(np.float64)
df_min['RepGK'] = pd.to_numeric(df_min['RepGK'], errors='coerce').fillna(0).astype(np.float64)
if 'ID' in df_min.columns:
    df_min['ID'] = pd.to_numeric(df_min['ID'], errors='coerce').fillna(-1).astype(np.int64)

print("Using columns and dtypes:\n", df_min.dtypes)
print(df_min.head())

# ---------------------------------
# 2) BIOGEME SETUP
# ---------------------------------
database = db.Database('penalty_inertia_altFE_altSPEC', df_min)

choice      = Variable('CHOICE')
prev_choice = Variable('prev_choice')
has_inertia = Variable('has_inertia')
foot_var    = Variable('foot')
repgk_var   = Variable('RepGK')
id_var      = Variable('ID')

# ---------------------------------
# 3) PARAMETERS
# ---------------------------------
# ASCs (fix ASC1)
ASC1 = Beta('ASC1', 0, None, None, 1)
ASC2 = Beta('ASC2', 0, None, None, 0)
ASC3 = Beta('ASC3', 0, None, None, 0)
ASC4 = Beta('ASC4', 0, None, None, 0)
ASC5 = Beta('ASC5', 0, None, None, 0)
ASC6 = Beta('ASC6', 0, None, None, 0)

# Alt-specific inertia
b_inertia1 = Beta('b_inertia1', 0, None, None, 0)
b_inertia2 = Beta('b_inertia2', 0, None, None, 0)
b_inertia3 = Beta('b_inertia3', 0, None, None, 0)
b_inertia4 = Beta('b_inertia4', 0, None, None, 0)
b_inertia5 = Beta('b_inertia5', 0, None, None, 0)
b_inertia6 = Beta('b_inertia6', 0, None, None, 0)
b_inertia = {1:b_inertia1, 2:b_inertia2, 3:b_inertia3, 4:b_inertia4, 5:b_inertia5, 6:b_inertia6}

# Alt-specific foot effects
b_foot1 = Beta('b_foot1', 0, None, None, 1)
b_foot2 = Beta('b_foot2', 0, None, None, 0)
b_foot3 = Beta('b_foot3', 0, None, None, 0)
b_foot4 = Beta('b_foot4', 0, None, None, 0)
b_foot5 = Beta('b_foot5', 0, None, None, 0)
b_foot6 = Beta('b_foot6', 0, None, None, 0)
b_foot = {1:b_foot1, 2:b_foot2, 3:b_foot3, 4:b_foot4, 5:b_foot5, 6:b_foot6}

# Alt-specific RepGK effects
b_rep1 = Beta('b_repGK1', 0, None, None, 1)
b_rep2 = Beta('b_repGK2', 0, None, None, 0)
b_rep3 = Beta('b_repGK3', 0, None, None, 0)
b_rep4 = Beta('b_repGK4', 0, None, None, 0)
b_rep5 = Beta('b_repGK5', 0, None, None, 0)
b_rep6 = Beta('b_repGK6', 0, None, None, 0)
b_repGK = {1:b_rep1, 2:b_rep2, 3:b_rep3, 4:b_rep4, 5:b_rep5, 6:b_rep6}

# Player × Alternative fixed effects
# Player × Alternative fixed effects
if len(PLAYER_FE_IDS) == 0:
    raise RuntimeError("PLAYER_FE_IDS is empty. Add at least one ID.")

FE_params = {}
for pid in PLAYER_FE_IDS:
    for alt in [1, 2, 3, 4, 5, 6]:
        # Fix ALT1 for all player IDs (value=0)
        fixed = 1 if alt == 1 else 0
        FE_params[(pid, alt)] = Beta(f'FE_p{pid}_A{alt}', 0, None, None, fixed)

def player_fe_for_alt(alt_index):
    return sum(FE_params[(pid, alt_index)] * (id_var == pid) for pid in PLAYER_FE_IDS)

# ---------------------------------
# 4) UTILITIES
# ---------------------------------
V = {
    1: ASC1 + b_inertia[1]*(prev_choice==1)*has_inertia + player_fe_for_alt(1) + b_foot[1]*foot_var + b_repGK[1]*repgk_var,
    2: ASC2 + b_inertia[2]*(prev_choice==2)*has_inertia + player_fe_for_alt(2) + b_foot[2]*foot_var + b_repGK[2]*repgk_var,
    3: ASC3 + b_inertia[3]*(prev_choice==3)*has_inertia + player_fe_for_alt(3) + b_foot[3]*foot_var + b_repGK[3]*repgk_var,
    4: ASC4 + b_inertia[4]*(prev_choice==4)*has_inertia + player_fe_for_alt(4) + b_foot[4]*foot_var + b_repGK[4]*repgk_var,
    5: ASC5 + b_inertia[5]*(prev_choice==5)*has_inertia + player_fe_for_alt(5) + b_foot[5]*foot_var + b_repGK[5]*repgk_var,
    6: ASC6 + b_inertia[6]*(prev_choice==6)*has_inertia + player_fe_for_alt(6) + b_foot[6]*foot_var + b_repGK[6]*repgk_var,
}
avail = {i: 1 for i in range(1, 7)}

# ---------------------------------
# 5) ESTIMATE
# ---------------------------------
logprob = logit(V, avail, choice)
bgm = bio.BIOGEME(database, logprob)
bgm.modelName = 'mnl_inertia_altFE_altSPEC'

results = bgm.estimate()

# ---------------------------------
# 6) OUTPUT
# ---------------------------------
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
