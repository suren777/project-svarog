from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
from app import app
from layout.reusable import create_input_box
import plotly.graph_objects as go


def render_profile_settings():
    return [
        html.Div(
            children=[
                create_input_box("My Age", 33, "my-age"),
                html.P("Current Credits:"),
                create_input_box("Bank Account", 1500, "bank-account"),
                create_input_box("Savings", 1500, "my-savings"),
                create_input_box("Income", 4500, "monthtly-income"),
                create_input_box("Investments", 200, "my-investments"),
                html.P("Current Debts:"),
                create_input_box("Credit Card", 1500, "credit-account"),
                html.P("Outgoings:"),
                create_input_box("Bills/Mortgage", 1500, "monthly-bills"),
                create_input_box("Shopping", 800, "monthly-shopping"),
                create_input_box("Savings", 400, "pay-in-savings"),
                create_input_box("Investments", 0, "pay-in-investments"),
            ]
        ),
        html.Div(
            id="waterfall-graph-now",
            children=generate_current_waterfall(
                1500, 1500, 4500, 200, 1500, 1500, 800
            ),
            className="graph-settings",
        ),
    ]


@app.callback(
    Output("waterfall-graph-now", "children"),
    [
        Input("bank-account", "value"),
        Input("my-savings", "value"),
        Input("monthtly-income", "value"),
        Input("my-investments", "value"),
        Input("credit-account", "value"),
        Input("monthly-bills", "value"),
        Input("monthly-shopping", "value"),
    ],
)
def update_waterfall(
    bank_acc, savings, salary, investments, credit_card, bills, shopping
):
    return generate_current_waterfall(
        bank_acc, savings, salary, investments, credit_card, bills, shopping
    )


def generate_current_waterfall(
    bank_acc, savings, salary, investments, credit_card, bills, shopping
):
    fig = go.Figure(
        go.Waterfall(
            name="20",
            orientation="v",
            measure=[
                "relative",
                "relative",
                "relative",
                "relative",
                "total",
                "relative",
                "relative",
                "relative",
                "total",
            ],
            x=[
                "Bank Account",
                "Savings",
                "Salary",
                "Investments",
                "Gross Value",
                "Credit Card",
                "Bills",
                "Shopping",
                "Net Value",
            ],
            # textposition="outside",
            # text=["+60", "+80", "", "-40", "-20", "Total"],
            y=[
                bank_acc,
                savings,
                salary,
                investments,
                0,
                -credit_card,
                -bills,
                -shopping,
                0,
            ],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
        )
    )

    fig.update_layout(
        title="Income and Outcome graph",
        showlegend=False,
        plot_bgcolor="#fff",
        paper_bgcolor="#fff",
        width=800,
        height=500,
    )
    return dcc.Graph(figure=fig)

