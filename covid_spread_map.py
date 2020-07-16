from webbrowser import open as web_open

import folium
import geopandas as gpd
import numpy as np
import pandas as pd
from branca.colormap import linear
from folium.plugins import TimeSliderChoropleth

# load data files
df_covid = pd.read_csv('./coordinates/full_grouped.csv')
world_geojson = gpd.read_file('./coordinates/world.json')


def update_main_df(df_covid_data, df_world_geojson):
    df_covid_data['Date'] = pd.to_datetime(df_covid_data['Date']).apply(lambda x: x - pd.DateOffset(days=1))

    df_covid_data['Country/Region'].replace('Tanzania', 'United Republic of Tanzania', inplace=True)
    df_covid_data['Country/Region'].replace('Czechia', 'Czech Republic', inplace=True)
    df_covid_data['Country/Region'].replace('US', 'United States of America', inplace=True)
    df_covid_data['Country/Region'].replace('Congo (Kinshasa)', 'Democratic Republic of the Congo', inplace=True)
    df_covid_data['Country/Region'].replace('Congo (Brazzaville)', 'Republic of the Congo', inplace=True)
    df_covid_data['Country/Region'].replace('Taiwan*', 'Taiwan', inplace=True)
    df_covid_data['Country/Region'].replace('Serbia', 'Republic of Serbia', inplace=True)
    df_covid_data['Country/Region'].replace('North Macedonia', 'Macedonia', inplace=True)

    del df_covid_data['WHO Region']
    del df_world_geojson['id']

    return df_covid_data, df_world_geojson


def create_style_dict(list_of_country, df):
    main_dict = {}
    for i in range(len(list_of_country)):
        result = df[df['Country/Region'] == list_of_country[i]]
        inner_dict = {}
        for _, r in result.iterrows():
            inner_dict[r['date_sec']] = {
                'color': r['colour'],
                'opacity': 0.7,
            }
        main_dict[str(i)] = inner_dict
    return main_dict


if __name__ == '__main__':
    corona_df, world_geojson = update_main_df(df_covid, world_geojson)
    world_geojson = world_geojson.rename(columns={'name': 'Country/Region'})
    corona_df = corona_df[corona_df.Confirmed != 0]
    sorted_df = corona_df.sort_values(['Country/Region', 'Date']).reset_index(drop=True)
    sum_df = sorted_df.groupby(['Country/Region', 'Date'], as_index=False).sum()
    joined_df = sum_df.merge(world_geojson, on='Country/Region')
    joined_df['log_Confirmed'] = np.log10(joined_df['Confirmed'])
    joined_df['date_sec'] = pd.to_datetime(joined_df['Date']).astype(int) / 10**9
    joined_df['date_sec'] = joined_df['date_sec'].astype(int).astype(str)
    joined_df = joined_df[['Country/Region', 'date_sec', 'log_Confirmed', 'geometry']]

    cmap = linear.YlOrRd_09.scale(min(joined_df['log_Confirmed']), max(joined_df['log_Confirmed']))
    joined_df['colour'] = joined_df['log_Confirmed'].map(cmap)

    country_list = joined_df['Country/Region'].unique().tolist()
    style_dict = create_style_dict(country_list, joined_df)
    countries_df = joined_df[['geometry']]
    countries_gdf = gpd.GeoDataFrame(countries_df).drop_duplicates().reset_index()

    slider_map = folium.Map(min_zoom=2, max_bounds=True,tiles='cartodbpositron')
    _ = TimeSliderChoropleth(
        data=countries_gdf.to_json(),
        styledict=style_dict,

    ).add_to(slider_map)

    _ = cmap.add_to(slider_map)
    cmap.caption = 'Log of number of confirmed cases'
    slider_map.save(outfile='TimeSliderChoropleth.html')
    web_open('TimeSliderChoropleth.html')
