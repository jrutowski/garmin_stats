import pandas as pd
import sqlite3 

db_path = '/Users/joshuarutowski/HealthData/DBs/garmin_activities.db'
db_path_hr = '/Users/joshuarutowski/HealthData/DBs/garmin.db'

con = sqlite3.connect(db_path)
df = pd.read_sql_query("select * from activities", con)
con.close()
df = df.to_csv('~/desktop/Python/Github/garmin_stats/app/activities.csv', index = False)

con = sqlite3.connect(db_path_hr)
hr_df = pd.read_sql_query("select * from resting_hr", con)
con.close()
hr_df = hr_df.to_csv('~/desktop/Python/Github/garmin_stats/app/hr_df.csv', index = False)
