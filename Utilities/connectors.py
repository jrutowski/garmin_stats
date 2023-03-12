import pandas as pd
import sqlite3 
import os 

# refreshing local data source
os.system("garmindb_cli.py --all --download --import --analyze --latest")

db_path = '/Users/joshuarutowski/HealthData/DBs/garmin_activities.db'
db_path_hr = '/Users/joshuarutowski/HealthData/DBs/garmin.db'

con = sqlite3.connect(db_path)
df = pd.read_sql_query("select * from activities", con)
con.close()
df = df.to_parquet('~/desktop/Python/Github/garmin_stats/app/activities.gzip', index = False)

con = sqlite3.connect(db_path_hr)
hr_df = pd.read_sql_query("select * from resting_hr", con)
con.close()
hr_df = hr_df.to_parquet('~/desktop/Python/Github/garmin_stats/app/hr_df.gzip', index = False)

con = sqlite3.connect(db_path_hr)
sleep_df = pd.read_sql_query("select * from sleep", con)
con.close()
sleep_df = sleep_df.to_parquet('~/desktop/Python/Github/garmin_stats/app/sleep_df.gzip', index = False)

