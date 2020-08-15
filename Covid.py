import pandas as pd
import requests
import os
import folium
from flask import Flask,render_template
import datetime


# API Call to collect the Covid Data Set, Convert into Json format and put into a dataframe.
# Set the display option to max to see all columns
#Grouped the data by country
# country_geo = '{url}/us-states.json'
re = requests.get("https://corona.lmao.ninja/v2/countries?yesterday&sort")
re = re.json()
re = pd.DataFrame.from_dict(re)
pd.set_option('display.max_columns', None)
country_info = re['countryInfo']
country_info = pd.json_normalize(country_info)
df = pd.concat([re, country_info], axis=1,sort=False)
df = df.drop('countryInfo', axis=1)

def find_largest_cases(n):
    by_country = df.groupby('country').sum()[['cases', 'deaths', 'recovered', 'active']]
    covid_df = by_country.nlargest(n, 'cases')
    return covid_df
# print(find_largest_cases(5))

m = folium.Map(
    location=[100, 0],
    zoom_start=3,
    tiles='Stamen Toner'
)

folium.Choropleth (
    geo_data= 'geo.json',
    data=df,
    columns=['lat', 'long'],
    key_on='feature.id',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Test'
).add_to(m)

popup = 'Test'

folium.CircleMarker(
    location=[48, -102],
    radius=10,
    fill=True,
    popup=popup,
    weight=1,
).add_to(m)

m.save(os.path.join('results', 'CheckZorder.html'))

m

#
# df[['lat','long','cases']].apply(lambda x: circle_maker(x), axis=1)
# html_map = m._repr_html()
#
# app = Flask(__name__)
# @app.route('/')
# def home():
#     return render_template("home.html", table=df, cmap=html_map, pairs=pairs)
#
# if __name__ == "__main__":
#     app.run(debug=True)
