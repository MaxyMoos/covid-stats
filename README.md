# covid-stats

A very basic Python module to plot Covid-19 stats pulled from [Our World In Data](https://ourworldindata.org/)

### Python dependencies

* requests
* matplotlib

### Usage

Just clone the repo, `cd` to the repo root then open a Python console & play around:

```python
from covid_stats import covid_stats as cs

# Plot cases for a country (3-letter [ISO_3166-1_alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) country code)
cs.plot_cases('FRA')

# ...or for multiple countries
cs.plot_cases(['FRA', 'CHE'])

# Plot a rolling average over 7 days rather than raw cases per day
cs.plot_cases(['FRA', 'CHE'], 7)

# Nope, I'd rather see too much data, please
cs.plot_cases_and_deaths_per_million(['FRA', 'CHE', 'USA', 'BRA'], 7)
```

Available functions:
* `plot_cases` / `plot_cases_per_million`
* `plot_deaths` / `plot_deaths_per_million`
* `plot_cases_and_deaths` / `plot_cases_and_deaths_per_million`

All of those are user-friendly proxies to the real MVP: `plot_field_rolling_n_day_avg()` which does everything behind the scenes.
When imported, the module loads & parses data from Our World In Data's JSON data dump.
