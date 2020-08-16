import pandas as pd
import requests
import folium
from datetime import datetime
from flask import Flask, render_template

country_geo = 'world-countries.json'
re = requests.get("https://corona.lmao.ninja/v2/countries?yesterday&sort")
re = re.json()
re = pd.DataFrame.from_dict(re)
pd.set_option('display.max_columns', None)
country_info = re['countryInfo']
country_info = pd.json_normalize(country_info)
df = pd.concat([re, country_info], axis=1,sort=False)
df = df.drop('countryInfo', axis=1)

def thousand_separator(val):
    return f"{val:,}"

def convert_time_stamp(x):
    t = datetime.fromtimestamp(x/1000.0)
    s = t.strftime('%Y-%m-%d %H:%M:%S')
    return s[:-3]

df['recovered'] = df['recovered'].apply(thousand_separator)
df['cases'] = df['cases'].apply(thousand_separator)
df['deaths'] = df['deaths'].apply(thousand_separator)
df['updated'] = df['updated'].apply(convert_time_stamp)
last_update = df['updated'][0]

m = folium.Map(
    width=800,
    height=500,
    tiles="CartoDB positron",
    location=[32,0],
    zoom_start=1.5,
)

folium.Choropleth (
    geo_data= country_geo,
    data=df,
    columns=['lat', 'long'],
    key_on='feature.id',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2,
).add_to(m)

def circle_maker(x):
    folium.Circle(location=[x[0],x[1]],
                 radius=10,
                 color="red",
                 popup='{}\n Cases: {}\n Deaths: {}\n Recovered: {}'.format(x[2], x[3], x[4], x[5])).add_to(m)
df[['lat','long','country','cases','deaths', 'recovered']].apply(lambda x:circle_maker(x),axis=1)
html_map = m._repr_html_()

# IFrame(src=m, width=450, height=450)
folium.Popup(src=m, max_width=1000)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html",update=last_update, cmap=html_map)

@app.route('/about')
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)



