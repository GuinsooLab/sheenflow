<div align="right">
    <img src="https://raw.githubusercontent.com/GuinsooLab/glab/main/src/images/guinsoolab-badge.png" height="60" alt="badge">
    <br />
</div>
<div align="center">
    <img src="https://raw.githubusercontent.com/GuinsooLab/glab/main/src/images/guinsoolab-sheenflow.svg" alt="logo" height="100" />
    <br />
    <br />
</div>

# Sheenflow

Sheenflow is an orchestrator that's designed for developing and maintaining data assets, such as tables, data sets, machine learning models, and reports.

## Quickstart

You declare functions that you want to run and the data assets that those functions produce or update. Sheenflow then helps you run your functions at the right time and keep your assets up-to-date.

Sheenflow is built to be used at every stage of the data development lifecycle - local development, unit tests, integration tests, staging environments, all the way up to production.

If you're new to Sheenflow, we recommend reading about its [core concepts](https://ciusji.gitbook.io/sheenflow/concepts/assets) or learning with the hands-on [tutorial](https://ciusji.gitbook.io/sheenflow/overview/create-a-new-project).

An asset graph defined in Python:

```python
from sheenflow import asset
from pandas import DataFrame, read_html, get_dummies
from sklearn.linear_model import LinearRegression

@asset
def country_populations() -> DataFrame:
    df = read_html("https://tinyurl.com/mry64ebh")[0]
    df.columns = ["country", "continent", "rg", "pop2018", "pop2019", "change"]
    df["change"] = df["change"].str.rstrip("%").str.replace("−", "-").astype("float")
    return df

@asset
def continent_change_model(country_populations: DataFrame) -> LinearRegression:
    data = country_populations.dropna(subset=["change"])
    return LinearRegression().fit(
        get_dummies(data[["continent"]]), data["change"]
    )

@asset
def continent_stats(
    country_populations: DataFrame, continent_change_model: LinearRegression
) -> DataFrame:
    result = country_populations.groupby("continent").sum()
    result["pop_change_factor"] = continent_change_model.coef_
    return result
```

The graph loaded into Sheenflow's web UI:

![graph-sample](https://raw.githubusercontent.com/GuinsooLab/sheenflow/main/docs/assets/sample.jpg)

## Installation

Sheenflow is available on PyPI and officially supports Python 3.7+.

```bash
pip install sheenflow sheenlet
```

This installs two modules:

- **sheenflow**: The core programming model.
- **sheenlet**: The web interface for developing and operating Sheenflow jobs and assets.

## Documentation

You can find the full Sheenflow documentation [here](https://ciusji.gitbook.io/sheenflow/).

## Contributing

For details on contributing or running the project for development, check out our [contributing
guide](https://ciusji.gitbook.io/sheenflow/reference/contributing).

## License

Sheenflow is [Apache 2.0 licensed](https://github.com/GuinsooLab/sheenflow/blob/main/LICENSE).

<img src="https://raw.githubusercontent.com/GuinsooLab/glab/main/src/images/guinsoolab-group.svg" width="120" alt="license" />
