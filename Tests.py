import pandas as pd
import requests

# API Call to collect the Covid Data Set, Convert into Json format and put into a dataframe.
# Set the display option to max to see all columns
#Grouped the data by country
country_geo = 'world-countries.json'
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