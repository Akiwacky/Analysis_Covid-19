import pandas as pd
import requests
import folium
from flask import Flask,render_template
import datetime


# API Call to collect the Covid Data Set, Convert into Json format and put into a dataframe.
# Set the display option to max to see all columns
#Grouped the data by country

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

# m = folium.Map(location=(37.76, -122.45), zoom_start=12)
#
# def circle_maker(x):
#     folium.Circle(location=[x[0],x[1]],
#                   radius=float(x[2])* 10,
#                   color="red",
#                   popup='{}\n confirmed cases: {}'.format((x[3],x[2])).add_to(m))
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
