import os
import pandas as pd
import numpy as np
import pybaseball as pyb
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor 

pd.set_option("display.max_columns", None)
pd.set_option('display.max_colwidth', None)

# Only going back to 2015 because that is the Statcast era
import datetime
today = datetime.date.today()
year = today.year
pitcherMetrics = pyb.pitching_stats(start_season=2015, end_season=(year-1), ind=1, qual = 50)

pitcherStats = pitcherMetrics[['ERA', 'K%', 'BB%', 'HR/9', 'GB%', 'FB%', 'IFFB%', 'HardHit%', 'Pull%', 'Cent%', 'Oppo%']]
X = pitcherStats.drop('ERA', axis=1)
y = pitcherStats.ERA
model = sm.OLS(y, X)
results = model.fit()

# Declare test set
pitcherMetrics2024 = pyb.pitching_stats(start_season=year, end_season=year, ind=1, qual = 50)

pitcherStats2024 = pitcherMetrics2024[['ERA', 'K%', 'BB%', 'HR/9', 'GB%', 'FB%', 'IFFB%', 'HardHit%', 'Pull%', 'Cent%', 'Oppo%']]
X = pitcherStats2024.drop('ERA', axis=1)
pred = results.predict(X)
pitcherMetrics2024['predERA'] = pred
pitcherMetrics2024['Diff'] = pitcherMetrics2024['predERA']-pitcherMetrics2024['ERA']
pitcherMetrics2024 = pitcherMetrics2024[['Name', 'IDfg', 'Team', 'Age', 'ERA', 'predERA', 'Diff', 'K%', 'BB%', 'HR/9', 'GB%', 'FB%', 'IFFB%', 'HardHit%', 'Pull%', 'Cent%', 'Oppo%'] + [col for col in pitcherMetrics2024.columns if col not in ['Name', 'IDfg', 'Team', 'Age', 'ERA', 'predERA', 'Diff', 'K%', 'BB%', 'HR/9', 'GB%', 'FB%', 'IFFB%', 'HardHit%', 'Pull%', 'Cent%', 'Oppo%']]]

os.chdir('/Users/parkergeis/Library/CloudStorage/OneDrive-WesternGovernorsUniversity/Apps/Microsoft Power Query/Uploaded Files')
pitcherMetrics2024.to_excel('currYearPitching.xlsx', index=False)


# # Export to Google Sheets (for possible live Tableau refresh)

# import gspread
# import gspread_dataframe as gd
# from oauth2client.service_account import ServiceAccountCredentials

# # Use the credentials file you downloaded from Google Cloud Console
# scope = ['https://spreadsheets.google.com/feeds',
#          'https://www.googleapis.com/auth/drive']
# creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/parkergeis/Downloads/seismic-bucksaw-427616-e6-7082af692c88.json', scope)
# client = gspread.authorize(creds)

# # Open the Google Spreadsheet (Make sure you have edit permissions to this spreadsheet)
# sheet = client.open('ERAPredictor').sheet1

# # Clear all existing data in the sheet
# sheet.clear()

# # Assuming `sheet` is the gspread Sheet instance you've created as before
# gd.set_with_dataframe(sheet, pitcherMetrics2024)
