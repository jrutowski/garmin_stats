# garmin_stats
This project originally started out to achieve my goal this year of incorporating Docker into some sort of personal project and has evolved into so much more. The dashboard itself is a visualization to showcase where my stats are at with respect to running, and answering various physiological questions with the data collected by my Garmin.

**Pages**:
1. dashboard (home): This is the main page which features base statistics in terms of running mileage by week, along with allowing the user to select a specific timeframe to view mileage there. This page also shows base level metrics for 2 week change, such as change in resting and active heart rate(s), mileage, and activities. It also features a countdown for my upcoming 'A' races for 2023. 

**Links**:
1. https://joshruns.com

## Data Sources:
*Physical Data* is collected via my Garmin Forerunner 955 which is worn most of the day. The garmin data is synced locally to a SQLite database, where I currently am manually updating the source parquet files inside of this repo. 

The dashboard found [here](https://joshruns.com) and is hosted as a deployment of a docker container built from this repo. 

## Contributions:
1. [GarminDB Repo](https://github.com/tcgoetz/GarminDB) is the code which allows me to parse my garmin data to create this dashboard

