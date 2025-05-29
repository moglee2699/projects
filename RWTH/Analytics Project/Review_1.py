
import pandas as pd
import biogeme.database as db
from biogeme.expressions import Beta, Variable, log
from biogeme.models import logit
from biogeme.biogeme import BIOGEME
from biogeme import models 
import pandas as pd
from biogeme import *
from biogeme.expressions import Beta, Variable, log
#Load data
df = pd.read_csv('DataSetModel0NA6Alt.csv', sep=';')
df.rename(columns={df.columns[0]: 'ID'}, inplace=True)  # Ensure first column is 'ID'

# Convert problematic columns to numeric, coercing errors to NaN
columns_to_convert = [
    'notmovingGK', 'nmovGK', 'SR1', 'SRGK1', 'SR2', 'SRGK2', 'SR3', 'SRGK3',
    'SR4', 'SRGK4', 'SR5', 'SRGK5', 'SR6', 'SRGK6', 'MP1', 'MPGK1', 'MP2',
    'MPGK2', 'MP3', 'MPGK3', 'MP4', 'MPGK4', 'MP6', 'MPGK6', 'perc1', 'perc2',
    'perc3', 'perc4', 'perc5', 'perc6'
]

for col in columns_to_convert:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col].str.replace(',', '.'), errors='coerce')
# Create Biogeme database
database = db.Database('mydata', df)

# Define all Beta parameters (initial value, lower bound, upper bound, status)
asc_TL = Beta('asc_TL', 0, None, None, 0)
asc_TC = Beta('asc_TC', 0, None, None, 0)
asc_TR = Beta('asc_TR', 0, None, None, 0)
asc_DL = Beta('asc_DL', 0, None, None, 0)
asc_DC = Beta('asc_DC', 0, None, None, 0)  
asc_DR = Beta('asc_DR', 0, None, None, 0)

b_foot1 = Beta('b_foot1', 0, None, None, 0)
b_foot2 = Beta('b_foot2', 0, None, None, 0)
b_foot3 = Beta('b_foot3', 0, None, None, 0)
b_foot4 = Beta('b_foot4', 0, None, None, 0)
b_foot5 = Beta('b_foot5', 0, None, None, 0) 
b_foot6 = Beta('b_foot6', 0, None, None, 0)

# Define additional Beta parameters for other variables
b_moveGK1 = Beta('b_moveGK1', 0, None, None, 0)
b_moveGK2 = Beta('b_moveGK2', 0, None, None, 0)
b_moveGK3 = Beta('b_moveGK3', 0, None, None, 0)
b_moveGK4 = Beta('b_moveGK4', 0, None, None, 0)
b_moveGK5 = Beta('b_moveGK5', 0, None, None, 0)
b_moveGK6 = Beta('b_moveGK6', 0, None, None, 0)

# DEFINE UTILITY FUNCTIONS

# Define the 'foot' and 'moveGK' variables from the dataframe
foot = Variable('foot')
moveGK = Variable('moveGK')

V = {
    1: (asc_TL 
        + b_foot1 * foot 
        + b_moveGK1 * moveGK),
      

    2: (asc_TC 
        + b_foot2 * foot 
        + b_moveGK2 * moveGK),
   

    3: (asc_TR 
        + b_foot3 * foot 
        + b_moveGK3 * moveGK),
  

    4: (asc_DL 
        + b_foot4 * foot 
        + b_moveGK4 * moveGK),
 

    5: (asc_DC 
        + b_foot5 * foot 
        + b_moveGK5 * moveGK),


    6: (asc_DR 
        + b_foot6 * foot 
        + b_moveGK6 * moveGK),

}


# Availability (1 = always available)
av = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}

# Define the Choice variable
Choice = Variable('Choice')

# Define log-likelihood
prob = models.logit(V, av, Choice)
logprob = log(prob)

# Estimate the model
biogeme = BIOGEME(database, logprob)
biogeme.modelName = 'Biogeme_finished_model'
results = biogeme.estimate()

# Get estimated parameters
estimated_params = results.get_estimated_parameters()

# Access the DataFrame columns directly
params_df = pd.DataFrame({
    'Parameter': estimated_params.index,
    'Estimate': estimated_params['Value'],
    'Std. Error': estimated_params['Rob. Std err'],
    't-ratio': estimated_params['Rob. t-test'],
    'Robust Std. Error': estimated_params['Rob. Std err'],
    'Robust t-ratio': estimated_params['Rob. t-test'],
    'p-value': estimated_params['Rob. p-value']
})

# Clean up the formatting for large numbers and NaN/None values
params_df['Estimate'] = params_df['Estimate'].apply(lambda x: f"{x:,.4f}" if pd.notnull(x) else 'NA')
params_df['Std. Error'] = params_df['Std. Error'].apply(lambda x: f"{x:,.4f}" if pd.notnull(x) else 'NA')
params_df['t-ratio'] = params_df['t-ratio'].apply(lambda x: f"{x:,.4f}" if pd.notnull(x) else 'NA')
params_df['Robust Std. Error'] = params_df['Robust Std. Error'].apply(lambda x: f"{x:,.4f}" if pd.notnull(x) else 'NA')
params_df['Robust t-ratio'] = params_df['Robust t-ratio'].apply(lambda x: f"{x:,.4f}" if pd.notnull(x) else 'NA')
params_df['p-value'] = params_df['p-value'].apply(lambda x: f"{x:,.4e}" if pd.notnull(x) else 'NA')

# Output results to CSV
params_df.to_csv('Biogeme_estimation_results.csv', index=False)

print("Results saved to Biogeme_estimation_results.csv")
