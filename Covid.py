import pandas as pd
import requests
import json

# API Call to collect the Covid Data Set, Convert into Json format and put into a dataframe.
# Set the display option to max to see all columns
#Grouped the data by country
# def find_top_confirmed(n=15):
re = requests.get("https://api.thevirustracker.com/free-api?countryTotals=ALL")
re = re.json()
re = re['countryitems']
# print(re)
df = pd.DataFrame(re)
print(df)


# re = pd.DataFrame.from_dict(re)
# re = pd.DataFrame(re)
# re = re.T
# print(re)

# print(re)




# covid_df = pd.DataFrame(data)
# pd.set_option('display.max_columns', None)
# print(covid_df.head())
# by_country = covid_df.groupby('Country').sum()['Deaths']
# print(by_country)

# l_cases = by_country.nlargest(n, 'Confirmed')
# return l_cases,

# print(find_top_confirmed())


