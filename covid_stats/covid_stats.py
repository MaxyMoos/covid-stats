#!/usr/bin/env python

import json
import requests
from datetime import datetime
from matplotlib import pyplot as plt


r = requests.get('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.json')

if r.status_code != 200:
    print("Error retrieving the raw dataset from GitHub!")

cv19_data = json.loads(r.text)


def dt(date_string):
    return datetime.strptime(date_string, "%Y-%m-%d").date()


def binsearch_from_date(date_from, dataset):
    l = len(dataset) // 2
    elem = dt(dataset[l].get('date'))
    dt_df = dt(date_from)

    if elem == dt_df:
        return l
    elif elem < dt_df:
        return l + binsearch_from_date(date_from, dataset[l:])
    elif elem > dt_df:
        return binsearch_from_date(date_from, dataset[:l])


""" Helper functions """
def plot_field_rolling_n_day_avg(
    dataset_or_country_code,
    n,
    field_names,
    from_date=False,
    to_date=False
):
    FIELD_LEGEND_MAPPING = {
        'new_cases': "New Cases",
        'new_deaths': "New Deaths",
        'new_cases_per_million': "New Cases per million",
        'new_deaths_per_million': "New Deaths per million",
    }
    datasets = []

    if isinstance(dataset_or_country_code, str) and len(dataset_or_country_code) == 3:
        datasets = {
            cv19_data[dataset_or_country_code].get('location'): cv19_data[dataset_or_country_code]['data']
        }
    elif (
        isinstance(dataset_or_country_code, list)
        and all([isinstance(item, str) and len(item) == 3 for item in dataset_or_country_code])
    ):
        # List of country codes
        datasets = {
            cv19_data[item].get('location'): cv19_data[item]['data']
            for item in dataset_or_country_code
        }
    if isinstance(field_names, str):
        field_names = [field_names]

    legends = []

    for country_name, dataset in datasets.items():
        rolling_average = []

        start_index = binsearch_from_date(from_date, dataset) if from_date else 0

        for index, item in enumerate(dataset[start_index+n:]):
            date = item.get('date')
            if to_date and dt(date) > dt(to_date):
                break

            roll_avg_item = {'date': item.get('date')}
            for field_name in field_names:
                roll_avg_val = [
                    item.get(field_name)
                    for item in dataset[start_index+index:start_index+index+n]
                    if item.get(field_name) is not None
                ]
                roll_avg_val = sum(roll_avg_val) / len(roll_avg_val)
                roll_avg_item[field_name] = roll_avg_val
            rolling_average.append(roll_avg_item)
        for field_name in field_names:
            plt.plot(
                [item.get('date') for item in rolling_average],
                [item.get(field_name) for item in rolling_average]
            )
            legends.append([country_name])
    title = '/'.join([FIELD_LEGEND_MAPPING[f_name] for f_name in field_names])
    if n > 1:
        title += " (Rolling {} day average)".format(n)
    plt.legend(legends)
    plt.title(title)
    # Handle max number of value displayed on X axis
    ax = plt.gca()
    tick_nb = len(rolling_average) // 15 if len(rolling_average) > 15 else len(rolling_average)
    ax.xaxis.set_major_locator(plt.MaxNLocator(tick_nb))
    plt.show()

def plot_cases(dataset, n=1, from_date=False, to_date=False):
    return plot_field_rolling_n_day_avg(dataset, n, 'new_cases', from_date, to_date)

def plot_cases_per_million(dataset, n=1, from_date=False, to_date=False):
    return plot_field_rolling_n_day_avg(dataset, n, 'new_cases_per_million', from_date, to_date)

def plot_deaths(dataset, n=1, from_date=False, to_date=False):
    return plot_field_rolling_n_day_avg(dataset, n, 'new_deaths', from_date, to_date)

def plot_deaths_per_million(dataset, n=1, from_date=False, to_date=False):
    return plot_field_rolling_n_day_avg(dataset, n, 'new_deaths_per_million', from_date, to_date)

def plot_cases_and_deaths(dataset, n=1, from_date=False, to_date=False):
    return plot_field_rolling_n_day_avg(dataset, n, ['new_cases', 'new_deaths'], from_date, to_date)

def plot_cases_and_deaths_per_million(dataset, n=1, from_date=False, to_date=False):
    return plot_field_rolling_n_day_avg(dataset, n, ['new_cases_per_million', 'new_deaths_per_million'], from_date, to_date)
