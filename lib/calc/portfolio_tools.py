import pandas as pd
import numpy as np
import scipy.optimize
from lib.db.dbutils import get_time_series_from_db
from data.data import good_symbols


def portfolio_stats(weights, returns, T):
    mean = weights.dot(returns.mean().values * T)
    std = np.sqrt(weights.dot(returns.cov().dot(weights.T)) * T)
    return mean, std


def portfolio_return(weights, returns):
    return weights.T.dot(returns.values)


def portfolio_volatility(weights, covariance):
    return np.sqrt(weights.T.dot(covariance.dot(weights)))


def sharpe_ratio(weights, returns, covariance):
    return portfolio_return(weights, returns) / portfolio_volatility(
        weights, covariance
    )


def maximize_sharpe(weights, returns, covariance):
    return -sharpe_ratio(weights, returns, covariance)


def efficient_frontier(returns, expected_returns, covariance):
    nStocks = returns.shape[1]
    covariance = returns.cov() * 250
    expected_returns = returns.mean() * 250
    output = []
    w0 = np.array([1 / nStocks for _ in range(nStocks)])
    for ret in np.linspace(expected_returns.min(), expected_returns.max(), 50):
        constr = (
            dict(type="eq", fun=lambda x: np.sum(x) - 1),
            dict(
                type="eq",
                fun=lambda x: portfolio_return(x, expected_returns) - ret,
            ),
        )
        bounds = tuple((0, 1) for _ in range(nStocks))
        res = scipy.optimize.minimize(
            portfolio_volatility,
            w0,
            method="SLSQP",
            args=covariance,
            constraints=constr,
            bounds=bounds,
        )
        output.append([ret, res.fun] + list(np.round(res.x, 2)))
    return pd.DataFrame(
        output, columns=["returns", "vol"] + list(returns.columns + " weight")
    )


def calculate_max_sharpe_ratio(returns, expected_returns, covariance):
    nStocks = returns.shape[1]
    w0 = np.array([1 / nStocks for _ in range(nStocks)])
    constraints = {"type": "eq", "fun": lambda x: np.sum(x) - 1}
    bounds = tuple((0, 1) for x in range(nStocks))
    optimal_sharpe = scipy.optimize.minimize(
        maximize_sharpe,
        w0,
        method="SLSQP",
        bounds=bounds,
        args=(expected_returns, covariance),
        constraints=constraints,
    )
    return (
        portfolio_return(optimal_sharpe.x, expected_returns),
        portfolio_volatility(optimal_sharpe.x, covariance),
    )


def prepare_data():
    data_table = (
        get_time_series_from_db(good_symbols)
        .pivot(index="Date", columns="Symbol", values="Price")
        .iloc[-500:, 1:20]
    )
    data_table.index = pd.to_datetime(data_table.index)
    returns = data_table.pct_change()
    expected_returns = returns.mean() * 250
    expected_returns.dropna(inplace=True)
    expected_returns = expected_returns[expected_returns < 1]
    returns = returns[expected_returns.index]
    covariance = returns.cov() * 250
    return returns, expected_returns, covariance

