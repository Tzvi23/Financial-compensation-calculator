#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import datetime

xls = pd.ExcelFile('data/data4.xlsx')
# Load workers data
# Replacing all the nan values with -1 <br> and replacing all the '-' to -1
df1 = pd.read_excel(xls, 'data').fillna(-1)
df1 = df1.replace('-', -1)
df1 = df1.replace('התפטרות', 'resignation')
df1 = df1.replace('פיטורין', 'dismissal')
df1 = df1.replace('פרישה לגמלאות', 'retirement')

# Converting the data frame using to_dict to create for each line worker list with values
data_dict = df1.to_dict('split')
header_dict = data_dict['data'].pop(0)  # Popping the header list
data = data_dict['data']
# Update the header dict
header_dict[0] = 'ID'
header_dict = {v: k for v, k in enumerate(header_dict)}
print(header_dict)

# Load second sheet from the excel
df3 = pd.read_excel(xls, 'הנחות')
# Define interest rate variable as dictionary
df4 = df3.iloc[2:, 1:2]
df4.index -= 1
interest_rate = df4.to_dict()['Unnamed: 1']
print(interest_rate)


# Departure probabilities
def get_prob(age):
    # Dict: key: (age, age) : value: [dismissal, resignation]
    prob_table = {(18, 29): [0.07, 0.2],
                  (30, 39): [0.05, 0.13],
                  (40, 49): [0.04, 0.1],
                  (50, 59): [0.03, 0.07],
                  (60, 67): [0.02, 0.03]
                  }
    for key in prob_table.keys():
        if key[0] <= age <= key[1]:
            return prob_table[key]
    return None


# ### Other parameters
pay_rise = 0.03
payroll_date_rise = datetime.datetime(2020, 7, 1)

# Death tables
cs1 = pd.read_csv('data/deathBoardMale.csv', header=None)
male_death = cs1.to_dict()[0]
cs2 = pd.read_csv('data/deathBoradFemale.csv', header=None)
female_death = cs2.to_dict()[0]

