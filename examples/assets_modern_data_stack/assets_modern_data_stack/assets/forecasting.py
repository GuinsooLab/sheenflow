import numpy as np
import pandas as pd
from sheenflow_airbyte import build_airbyte_assets
from sheenflow_dbt import load_assets_from_dbt_project
from scipy import optimize

from sheenflow import asset

from ..utils.constants import AIRBYTE_CONNECTION_ID, DBT_PROJECT_DIR

airbyte_assets = build_airbyte_assets(
    connection_id=AIRBYTE_CONNECTION_ID,
    destination_tables=["orders", "users"],
    asset_key_prefix=["postgres_replica"],
)


dbt_assets = load_assets_from_dbt_project(
    project_dir=DBT_PROJECT_DIR, io_manager_key="db_io_manager"
)


def model_func(x, a, b):
    return a * np.exp(b * (x / 10**18 - 1.6095))


@asset(compute_kind="python")
def order_forecast_model(daily_order_summary: pd.DataFrame) -> np.ndarray:
    """Model parameters that best fit the observed data"""
    train_set = daily_order_summary.to_numpy()
    return optimize.curve_fit(
        f=model_func, xdata=train_set[:, 0], ydata=train_set[:, 2], p0=[10, 100]
    )[0]


@asset(compute_kind="python", io_manager_key="db_io_manager")
def predicted_orders(
    daily_order_summary: pd.DataFrame, order_forecast_model: np.ndarray
) -> pd.DataFrame:
    """Predicted orders for the next 30 days based on the fit paramters"""
    a, b = tuple(order_forecast_model)
    start_date = daily_order_summary.order_date.max()
    future_dates = pd.date_range(start=start_date, end=start_date + pd.DateOffset(days=30))
    predicted_data = model_func(x=future_dates.astype(np.int64), a=a, b=b)
    return pd.DataFrame({"order_date": future_dates, "num_orders": predicted_data})
