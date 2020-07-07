#!/usr/bin/env python

import json
import requests
from matplotlib import pyplot as plt


r = requests.get('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.json')

if r.status_code != 200:
    print("Error retrieving the raw dataset from GitHub!")

cv19_data = json.loads(r.text)


""" Helper functions """
def plot_field_rolling_n_day_avg(dataset_or_country_code, n, field_names):
    FIELD_LEGEND_MAPPING = {
        'new_cases': " - New Cases",
        'new_deaths': " - New Deaths",
        'new_cases_per_million': " - New Cases per million",
        'new_deaths_per_million': " - New Deaths per million",
    }
    datasets = []

    if isinstance(dataset_or_country_code, str) and len(dataset_or_country_code) == 3:
        datasets = {cv19_data[dataset_or_country_code].get('location'): cv19_data[dataset_or_country_code]['data']}
    elif isinstance(dataset_or_country_code, list) and all([isinstance(item, str) and len(item) == 3 for item in dataset_or_country_code]):
        # List of country codes
        datasets = {cv19_data[item].get('location'): cv19_data[item]['data'] for item in dataset_or_country_code}
    if isinstance(field_names, str):
        field_names = [field_names]

    legends = []

    for country_name, dataset in datasets.items():
        rolling_average = []
        for index, item in enumerate(dataset[n:]):
            roll_avg_item = {'date': item.get('date')}
            for field_name in field_names:
                roll_avg_val = sum([item.get(field_name) for item in dataset[index:index+n]]) / float(n)
                roll_avg_item[field_name] = roll_avg_val
            rolling_average.append(roll_avg_item)
        for field_name in field_names:
           plt.plot([item.get('date') for item in rolling_average], [item.get(field_name) for item in rolling_average])
           legends.append([country_name + FIELD_LEGEND_MAPPING.get(field_name, '- UNKNOWN')])
    plt.legend(legends)
    # Handle max number of value displayed on X axis
    ax = plt.gca()
    ax.xaxis.set_major_locator(plt.MaxNLocator(len(rolling_average) // 15))
    plt.show()

def plot_cases(dataset, n=1):
    return plot_field_rolling_n_day_avg(dataset, n, 'new_cases')

def plot_cases_per_million(dataset, n=1):
    return plot_field_rolling_n_day_avg(dataset, n, 'new_cases_per_million')

def plot_deaths(dataset, n=1):
    return plot_field_rolling_n_day_avg(dataset, n, 'new_deaths')

def plot_deaths_per_million(dataset, n=1):
    return plot_field_rolling_n_day_avg(dataset, n, 'new_deaths_per_million')

def plot_cases_and_deaths(dataset, n=1):
    return plot_field_rolling_n_day_avg(dataset, n, ['new_cases', 'new_deaths'])

def plot_cases_and_deaths_per_million(dataset, n=1):
    return plot_field_rolling_n_day_avg(dataset, n, ['new_cases_per_million', 'new_deaths_per_million'])
