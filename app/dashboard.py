import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, date, timedelta
import numpy as np
import plotly.express as px

def main():
    def load_data():
        # activities - main df
        df = pd.read_parquet("activities.gzip")

        # condition df
        df['start_time'] = pd.to_datetime(df['start_time'])
        df['hrz_4_time'] = pd.to_timedelta(df['hrz_4_time'])
        df['hrz_5_time'] = pd.to_timedelta(df['hrz_5_time'])
        df['elapsed_time'] = pd.to_timedelta(df['elapsed_time'])
        df['activity_date'] = df['start_time'].dt.date
        df['week_start'] = df['start_time'].dt.to_period('W').apply(lambda r: r.start_time)

        # resting hr 
        hr_df = pd.read_parquet("hr_df.gzip")

        hr_df['day'] = pd.to_datetime(hr_df['day'])
        hr_df['week_start'] = hr_df['day'].dt.to_period('W').apply(lambda r: r.start_time)

        return df, hr_df

    def agg_frames():
        start_date = df['activity_date'].min()
        end_date = datetime.today().date()

        # filters
        filters = (df['sport'] == 'running') & ((df['activity_date'] >= start_date) & (df['activity_date'] <= end_date))
        hr_filters = ((hr_df['day'].dt.date >= start_date) & (hr_df['day'].dt.date <= end_date))
        cols_to_show = ['activity_date', 'week_start','name', 'sport', 'distance', 'elapsed_time', 'avg_hr', 'calories', 'training_effect']

        agg_df = df[filters].groupby('week_start').agg(
            TotalDistance = ('distance', 'sum'), 
            TotalActivities = ('distance', 'count'),
            AverageHeartRateActive = ('avg_hr', 'mean')).reset_index().round(2)
        
        agg_df_hr = hr_df[hr_filters].groupby('week_start').agg(AverageHeartRateResting = ('resting_heart_rate', 'mean')).reset_index().round(2)

        return agg_df, agg_df_hr


    def comparisons(frame, metric):
        '''Function to return the difference in values between the max week and previous week for delta values
        frame: the agg frame from the group by of start date
        metric: the column name of the values to obtain the deltas for'''

        max_week = frame['week_start'].max() - pd.Timedelta(1, unit = 'W')
        previous_week = frame['week_start'].max() - pd.Timedelta(2, unit = 'W')

        max_week_value = frame.loc[frame['week_start'] == max_week][metric].item()
        max_week_delta = round(float(max_week_value - frame.loc[frame['week_start'] == previous_week][metric].values), 2)
        return max_week_value, max_week_delta

    def race_deltas(race_date):
        return datetime.now() - race_date

    def pct_time_tempo(start, end, sport = 'running'):
        temp_frame = df.loc[(df['activity_date'] >= start) & (df['activity_date'] <= end) & (df['sport'] == sport)].copy()
        temp_frame['pct_above_tempo'] = (temp_frame['hrz_4_time'].dt.seconds + temp_frame['hrz_5_time'].dt.seconds) / temp_frame['elapsed_time'].dt.seconds
        return temp_frame[['activity_date', 'pct_above_tempo', 'distance', 'avg_cadence']]

    df, hr_df = load_data()
    agg_df, agg_df_hr = agg_frames()

    max_week_distance, max_week_delta = comparisons(agg_df, 'TotalDistance')
    max_week_activities, max_week_activities_delta = comparisons(agg_df, 'TotalActivities')
    max_week_hr_active, max_week_hr_active_delta = comparisons(agg_df, 'AverageHeartRateActive')
    max_week_hr_resting, max_week_hr_active_resting = comparisons(agg_df_hr, 'AverageHeartRateResting')

    vt100 = datetime.strptime("07-14-2023 04:00:00", "%m-%d-%Y %H:%M:%S")
    ia50 = datetime.strptime("05-13-2023 06:00:00", "%m-%d-%Y %H:%M:%S")
    chi_marathon = datetime.strptime("10-08-2023 07:00:00", "%m-%d-%Y %H:%M:%S")

    vt_delta = race_deltas(vt100)
    ia50_delta = race_deltas(ia50)
    chi_delta = race_deltas(chi_marathon)

    # default values
    run_start_date_init = df['activity_date'].min()
    run_end_date_init = df['activity_date'].max()

    st.set_page_config(
        page_title = "Garmin Running Data"
    )

    with st.sidebar:
        st.header('Welcome!')
        st.markdown('This dashboard is meant to be a combination of my two passions, running and data science. We live in a world where we are able to meticiliously track most metrics and derive valuable insights from them which allow us to perform not only better but smarter. This dashboard is meant to be a display of this')
        
        st.subheader('Date Selection')
        st.markdown('Select the date range below which will allow you to see my weekly mileage count')
        run_start_date = st.date_input('Input Running Start Date', min_value = df['activity_date'].min())
        run_end_date = st.date_input('Input Running End date', max_value = date.today())
        
        if run_start_date <= run_end_date:
            st.success('Start date: `%s`\n\nEnd date:`%s`' % (run_start_date, run_end_date))
        else:
            st.error('Error: End date must fall after start date.')

    tab1, tab2, tab3 = st.tabs(['Home', 'Sleep Analysis', 'Spooky'])
    with tab1:
        with st.container():
            st.header('Previous Week Metrics')
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Distance (in miles)", max_week_distance, max_week_delta)
            col2.metric("Activities", max_week_activities, max_week_activities_delta)
            col3.metric("Active Heart Rate (in BPM)",max_week_hr_active, max_week_hr_active_delta) 
            col4.metric("Resting Heart Rate (in BPM)", max_week_hr_resting, max_week_hr_active_resting)

            st.header('Upcoming Races')
            col1, col2, col3 = st.columns(3)
            col1.metric("Ice Age 50 Mile Ultramarathon", f"{ia50_delta.days * -1} days")
            col2.metric("Vermont 100 Mile Ultramarathon", f"{vt_delta.days * -1} days")
            col3.metric("Chicago Marathon", f"{chi_delta.days * -1} days")

        st.plotly_chart(
            px.bar(agg_df[(agg_df['week_start'].dt.date >= run_start_date) & (agg_df['week_start'].dt.date <= run_end_date)], x = 'week_start', y = 'TotalDistance',
                title = 'Total Running Distance (in Miles) by Week',
                labels = {
                    'week_start': 'Start Week Date',
                    'TotalDistance': 'Total Distance (in Miles)'
                }
            ))
        
        test = pct_time_tempo(run_start_date, run_end_date) 
        st.plotly_chart(
            px.scatter(test, x = 'activity_date', y = 'pct_above_tempo', size = 'distance', color = 'avg_cadence',
                title = 'Percent of Workout At or Above Threshold (HR)',
                color_continuous_scale = 'portland',
                labels = {
                    'activity_date':'Activity Date',
                    'pct_above_tempo':'Percent of Workout At/Above Threshold',
                    'avg_cadence':'Average Cadence (in SPM)'
                }
            )
        )
if __name__ == '__main__':
    main()
#sleep by relative effort?
# DEV
# manual overrides
# activities = 'running'
# max_day = date.today()

# start_date = df['activity_date'].min()
# end_date = datetime.today().date()
