import pandas as pd
import requests

# API Call to collect the Covid Data Set, Convert into Json format and put into a dataframe.
# Set the display option to max to see all columns
#Grouped the data by country
# def find_top_confirmed(n=15):
re = requests.get("https://api.covid19api.com/all")
data = re.json()
covid_df = pd.DataFrame(data)
pd.set_option('display.max_columns', None)
# print(covid_df.head())
france = covid_df[covid_df['Country'] == 'France']
print(france)
by_country = covid_df.groupby('Country').sum()[['Confirmed', 'Deaths', 'Recovered', 'Active']]
# l_cases = by_country.nlargest(n, 'Confirmed')
# return l_cases,

# print(find_top_confirmed())


