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
batterMetrics = pyb.batting_stats(start_season=2015, end_season=(year-1), split_seasons=True)