import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date, timedelta

def main():
    def time_delta_convertor(delta):
        '''goal is to obtain hours from timedelta type'''
        secs = delta.total_seconds()
        hours = secs / 3600
        return round(hours, 2)

    def sleep_conditioning():  
        df = pd.read_parquet('~/desktop/Python/Github/garmin_stats/app/sleep_df.gzip')  
        df = df.loc[df['start'].notna()] # removing NA rows

        df['day'] = pd.to_datetime(df['day'])
        df['start'] = pd.to_datetime(df['start'])
        df['end'] = pd.to_datetime(df['end'])

        df['total_sleep'] = pd.to_timedelta(df['total_sleep'])
        df['deep_sleep'] = pd.to_timedelta(df['deep_sleep'])
        df['rem_sleep'] = pd.to_timedelta(df['rem_sleep'])

        df['total_sleep_hrs'] = df['total_sleep'].apply(lambda x: time_delta_convertor(x))
        df['deep_sleep_hrs'] = df['deep_sleep'].apply(lambda x: time_delta_convertor(x))
        df['rem_sleep_hrs'] = df['rem_sleep'].apply(lambda x: time_delta_convertor(x))

        df['sleep_pct_rem'] = round(df['rem_sleep_hrs'] / df['total_sleep_hrs'], 2)
        df['sleep_pct_deep'] = round(df['deep_sleep_hrs'] / df['total_sleep_hrs'], 2)

        df['weekday'] = df['day'].dt.day_name()


        return df
    sleep_df = sleep_conditioning()

    with st.sidebar:
        st.subheader('Sleep Analysis')
        st.markdown("""
        This page is meant to dive deeper into my own sleep data and evaluate how it effects my performance. The goal is to not only understand the descriptive trends of
        my sleep patterns, but also how we can directly tie these to how it effects performance
        """)

    with st.container():
        st.subheader('Boxplots for Sleep Analysis')
        col_map = {
            'total_sleep_hrs':'Total Sleep Hours',
            'sleep_pct_rem':'Percent of Sleep as REM',
            'sleep_pct_deep':'Percent of Sleep as Deep' }
        boxplot_option = st.selectbox('Sleep Type Selection', col_map.keys(), format_func = lambda x: col_map[x] )
        st.plotly_chart(
            px.box(sleep_df, x = 'weekday', y = boxplot_option,
                category_orders = dict(weekday=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']),
                title = 'Distribution of {0} by Weekday'.format(col_map[boxplot_option])),
                labels = {
                        'weekday': 'Weekday',
                        'boxplot_option': col_map[boxplot_option]})
    
if __name__ == '__main__':
    main()
