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
    calculate_eff_port,
    calculate_max_sharpe_ratio,
    calculate_min_vol,
    efficient_frontier,
    prepare_data,
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
                        # dbc.Button(
                        #     "Show Portfolio",
                        #     color="secondary",
                        #     className="mr-1",
                        #     id="port-button",
                        #     n_clicks=0,
                        # ),
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
        dbc.Row(
            [
                dbc.Col([], md=4,),
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label("Risk Level", html_for="slider"),
                            dcc.Slider(
                                id="risk-level",
                                min=0,
                                max=100,
                                step=5,
                                value=50,
                            ),
                        ]
                    ),
                ),
            ]
        ),
        html.Div(id="result-card"),
    ]


@app.callback(
    [Output("investment-view", "children"), Output("result-card", "children")],
    [Input("risk-level", "value")],
)
def run_portfolio(risk_level):
    if risk_level > 0 and risk_level <= 100:
        return generate_portfolio_stock_view(risk_level / 100)
    else:
        return generate_portfolio_stock_view(0.00001)


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
    return dcc.Graph(figure=fig), port_weights_card(eff_port_df)


@cache.memoize()
def select_ticks(eff_port_df, expected_returns, returns):
    tickers = eff_port_df[2:].index.unique()
    returns_to_plot = expected_returns[expected_returns.index.isin(tickers)]
    covariance_to_plot = np.sqrt(returns[tickers].cov() * 250)
    return returns_to_plot, covariance_to_plot


def port_weights_card(series):
    return dbc.Card(
        dbc.CardBody(
            [html.H3("Portfolio Statistics")]
            + [
                html.H5(
                    [
                        index,
                        dbc.Badge(
                            f"{ (round(value, 2) * 100):3.0f}%",
                            className="ml-1",
                        ),
                    ]
                )
                for index, value in zip(series.index, series.tolist())
            ]
        ),
        style={"width": "18rem"},
    )
