import matplotlib.pyplot as plt
import pandas as pd
from grab_data import get_sqls_conn

#constants and default params
SELECT_FILE = 'select_stats.sql'
DB = 'olx'
SERVER = 'localhost'
LOCATIONS = [
    'Галицький', 'Сихівський', 'Залізничний', 'Личаківський', 'Шевченківський',
    'Франківський'
]


#get select query from a file
def get_select_query():
    with open(SELECT_FILE, 'r') as query_file:
        query = query_file.read()
    return query


#get dataframe to visualize
def get_dataframe(connection):
    query = get_select_query()
    return pd.read_sql(query, conn)


#get location dataframe
def get_df_by_location(location, df):
    filter = df['location'] == location
    return df[filter]


#draw 0.05 and 0.95 percentiles for a location on a plot in given axes
def draw_percentiles_by_location(location, df, axes):
    data_filtered = get_df_by_location(location, df)
    #draw 05 percentile
    data_filtered.plot(
        kind='line',
        x='added_on',
        y='perc_05',
        label=(location + ' 0.05'),
        linewidth=1,
        ax=axes)
    #draw 0.95 percentile
    data_filtered.plot(
        kind='line',
        x='added_on',
        y='perc_95',
        label=(location + ' 0.95'),
        linewidth=1,
        ax=axes)


#add legend and labels etc
def config_plot():
    plt.xlabel('DATE WHEN POSTED')
    plt.ylabel('PRICE IN USD')
    plt.title('price in USD - 0.05 and 0.95 percentiles by reqions in time')
    plt.legend()


#########let's do the work - visualize the information###########
if __name__ == '__main__':
    conn = get_sqls_conn(SERVER, DB)
    data = get_dataframe(conn)
    data['added_on'] = pd.to_datetime(
        data['added_on'], infer_datetime_format=True)

    ax = plt.gca()

    for location in LOCATIONS:
        draw_percentiles_by_location(location, data, ax)

    config_plot()
    plt.show()
