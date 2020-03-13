import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output

from app import app
from common.extensions import cache
from layout.reusable import create_input_box
from lib.calc.portfolio_tools import (
    calculate_eff_port_,
    calculate_max_sharpe_ratio_,
    calculate_min_vol_,
    efficient_frontier_,
    prepare_data_,
)


def render_investment_layout():

    return [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("What is Allocation?"),
                        html.P(
                            """\
                            Asset allocation is an investment strategy that
                            aims to balance risk and reward by apportioning a
                            portfolio's assets according to an individual's
                            goals,
                            risk tolerance, and investment horizon.
                            The three main asset
                            classes - equities, fixed-income, and cash
                            and equivalents -
                            have different levels of risk and return, so
                            each will behave differently over time."""
                        ),
                        html.H5("Portfolio Settings"),
                        create_input_box("Equity %", 80, "equity-weight"),
                        create_input_box("Bond %", 20, "bond-weight"),
                        create_input_box("Risk Level", 50, "risk-level"),
                        dbc.Button(
                            "Show Portfolio",
                            color="secondary",
                            className="mr-1",
                            id="port-button",
                            n_clicks=0,
                        ),
                    ],
                    md=4,
                ),
                dbc.Col(
                    [
                        html.H2("How can portfolio look like?"),
                        html.Div(id="investment-view",),
                    ]
                ),
            ]
        ),
    ]


@app.callback(
    Output("investment-view", "children"), [Input("risk-level", "value")],
)
def run_portfolio(risk_level):
    if risk_level > 0 and risk_level <= 100:
        return generate_portfolio_stock_view(risk_level / 100)


@app.callback(
    Output("bond-weight", "value"), [Input("equity-weight", "value")]
)
def update_bond_weight(w):
    if w > 100:
        return 0
    elif w < 0:
        return 100
    else:
        return 100 - w


@cache.memoize()
def prepare_data():
    return prepare_data_()


@cache.memoize()
def efficient_frontier(
    expected_returns, covariance, ret_min=None, ret_max=None
):
    return efficient_frontier_(expected_returns, covariance, ret_min, ret_max)


@cache.memoize()
def calculate_max_sharpe_ratio(returns, expected_returns, covariance):
    return calculate_max_sharpe_ratio_(returns, expected_returns, covariance)


@cache.memoize()
def calculate_min_vol(returns, expected_returns, covariance):
    return calculate_min_vol_(returns, expected_returns, covariance)


@cache.memoize()
def calculate_eff_port(expected_returns, covariance, ret):
    return calculate_eff_port_(expected_returns, covariance, ret)


def generate_portfolio_stock_view(risk_multiplier):
    returns, expected_returns, covariance = prepare_data()
    max_sharpe_return, max_sharpe_vol = calculate_max_sharpe_ratio(
        returns, expected_returns, covariance
    )
    miv_vol_vol, min_vol_ret = calculate_min_vol(
        returns, expected_returns, covariance
    )

    eff_front = efficient_frontier(
        expected_returns,
        covariance,
        ret_max=max_sharpe_return,
        ret_min=min_vol_ret,
    )  #
    selected_return = (
        min_vol_ret + (max_sharpe_return - min_vol_ret) * risk_multiplier
    )
    eff_port = calculate_eff_port(
        expected_returns, covariance, selected_return
    )
    eff_port_df = pd.Series(
        data=[selected_return] + eff_port,
        index=["return", "vol"] + list(returns.columns),
    )
    eff_port_df = eff_port_df[eff_port_df > 0].dropna()
    returns_to_plot, covariance_to_plot = select_ticks(
        eff_port_df, expected_returns, returns
    )
    fig = go.Figure(
        data=[
            go.Scatter(
                x=eff_front.vol,
                y=eff_front.returns,
                mode="markers",
                name="Optimal Portfolio",
            ),
            go.Scatter(
                text=list(returns_to_plot.index.values),
                y=returns_to_plot.values,
                x=np.sqrt(np.diag(covariance_to_plot)),
                mode="markers+text",
                marker={
                    "size": 7,
                    "color": eff_port_df.tolist()[2:],
                    "size": np.array(eff_port_df.tolist()[2:]) * 100,
                },
                name="Individual Stocks",
                textposition="top center",
            ),
            go.Scatter(
                text="Portfolio Position",
                y=[eff_port_df.tolist()[0]],
                x=[eff_port_df.tolist()[1]],
                mode="markers+text",
                marker={"symbol": "star", "size": 12, "color": "red"},
                name="Portfolio Position",
                textposition="top center",
            ),
            go.Scatter(
                text="Capital Line",
                y=[0, max_sharpe_return],
                x=[0, max_sharpe_vol],
                mode="lines",
                name="Capital Line",
            ),
        ]
    )
    fig.update_layout(plot_bgcolor="#fff", paper_bgcolor="#fff")
    # fig.update_layout(height=500, width=800)
    return dcc.Graph(figure=fig)


@cache.memoize()
def select_ticks(eff_port_df, expected_returns, returns):
    tickers = eff_port_df[2:].index.unique()
    returns_to_plot = expected_returns[expected_returns.index.isin(tickers)]
    covariance_to_plot = np.sqrt(returns[tickers].cov() * 250)
    return returns_to_plot, covariance_to_plot


def port_weights_card(series):
    return dbc.Card(
        dbc.CardBody(
            [
                html.P("{}: {}".format(index, value[0]))
                for index, value in zip(series.index, series.values)
            ]
        )
    )
