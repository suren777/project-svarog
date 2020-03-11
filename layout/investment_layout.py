import dash_html_components as html
import dash_core_components as dcc
import numpy as np
import plotly.graph_objects as go
from dash.dependencies import Input, Output

from app import app
from layout.reusable import create_input_box
from lib.calc.portfolio_tools import (
    prepare_data,
    calculate_max_sharpe_ratio,
    efficient_frontier,
)
import dash_bootstrap_components as dbc


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
                            portfolio's assets according to an individual's goals, 
                            risk tolerance, and investment horizon. The three main asset 
                            classes - equities, fixed-income, and cash and equivalents - 
                            have different levels of risk and return, so each will behave differently over time."""
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
                        html.H2("How does portfolio look like?"),
                        dcc.Loading(html.Div(id="investment-view",)),
                    ]
                ),
            ]
        ),
    ]


@app.callback(
    Output("investment-view", "children"), [Input("port-button", "n_clicks")],
)
def run_portfolio(n_clicks):
    if n_clicks > 0:
        return generate_portfolio_stock_view()


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


def generate_portfolio_stock_view():

    returns, expected_returns, covariance = prepare_data()
    sharpe_return, sharpe_vol = calculate_max_sharpe_ratio(
        returns, expected_returns, covariance
    )
    eff_front = efficient_frontier(returns, expected_returns, covariance)
    fig = go.Figure(
        data=[
            go.Scatter(
                x=eff_front.vol,
                y=eff_front.returns,
                mode="markers",
                name="Optimal Portfolio",
            ),
            go.Scatter(
                text=list(expected_returns.index.values),
                y=expected_returns.values,
                x=np.sqrt(np.diag(covariance)),
                mode="markers+text",
                marker={"symbol": "x", "size": 7, "color": "black"},
                name="Individual Stocks",
                textposition="top center",
            ),
            go.Scatter(
                text="Sharpe Max",
                y=[sharpe_return],
                x=[sharpe_vol],
                mode="markers+text",
                marker={"symbol": "star", "size": 12, "color": "red"},
                name="Sharpe Max",
                textposition="top center",
            ),
        ]
    )
    fig.update_layout(plot_bgcolor="#fff", paper_bgcolor="#fff")
    # fig.update_layout(height=500, width=800)
    return dcc.Graph(figure=fig)
