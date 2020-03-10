import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from layout.reusable import create_input_box
import plotly.graph_objects as go
import numpy as np
from app import app


def render_future_profile_settings():
    return [
        html.Div(
            children=[
                create_input_box("Simulation Years", 10, "sim-years"),
                create_input_box(
                    "Savings Interest %", 0.2, "savings-interest"
                ),
                create_input_box(
                    "Investments Interest %", 6, "investment-interest"
                ),
            ]
        ),
        html.Div(
            id="future-fin-health-projection",
            children=generate_future_projection(10, 0.2, 6),
            className="graph-settings",
        ),
    ]


@app.callback(
    Output("future-fin-health-projection", "children"),
    [
        Input("sim-years", "value"),
        Input("savings-interest", "value"),
        Input("investment-interest", "value"),
    ],
)
def update_projection_graph(years, savings_ir, investments_ir):
    return generate_future_projection(years, savings_ir, investments_ir)


def generate_future_projection(years, savings_ir, investments_ir):
    years = years if years else 1
    savings_ir = savings_ir if savings_ir else 0
    investments_ir = investments_ir if investments_ir else 0
    current_savings = 1500
    monthly_savings = 400
    current_investments = 400
    monthly_investments = 400
    monthly_outgoings = 1500
    current_bank = 1500
    monthly_income = 5000
    bank_account = [current_bank]
    saving_account = [current_savings]
    investment_account = [current_investments]
    loss_account = np.array([monthly_outgoings] * int(years * 12))
    accidential_spending = np.random.uniform(800, 2000, size=int(years * 12))
    loss_account = list(loss_account + accidential_spending)
    total = [current_bank + current_investments + current_savings]
    for t in range(int(years * 12)):
        saving_account.append(
            saving_account[-1] * (savings_ir / 12 / 100 + 1) + monthly_savings
        )
        investment_account.append(
            investment_account[-1] * (investments_ir / 12 / 100 + 1)
            + monthly_investments
        )
        bank_account.append(
            bank_account[-1]
            + monthly_income
            - monthly_savings
            - monthly_investments
            - loss_account[t]
        )
        total.append(
            saving_account[-1] + bank_account[-1] + investment_account[-1]
        )
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=list(range(int(years * 12))),
            y=saving_account,
            name="Savings Account",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=list(range(int(years * 12))),
            y=investment_account,
            name="Investment Account",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=list(range(int(years * 12))),
            y=bank_account,
            name="Bank Account",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=list(range(int(years * 12))),
            y=loss_account,
            name="Outgoings Account",
        )
    )
    fig.add_trace(
        go.Scatter(x=list(range(int(years * 12))), y=total, name="Total",)
    )
    fig.update_layout(
        title="Balance Projection",
        plot_bgcolor="#fff",
        paper_bgcolor="#fff",
        width=800,
        height=500,
    )

    return dcc.Graph(figure=fig)
