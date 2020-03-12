import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State

from app import app
from layout.reusable import create_input_box


def make_card(name, content):
    # we use this function to make the example items to avoid code duplication
    return dbc.Card(
        [dbc.CardBody([html.H5(name, className="card-title")] + content,)]
    )


def profile_settings():
    return dbc.CardDeck(
        [
            make_card(
                "Current Balance",
                [
                    create_input_box("Bank Account", 1500, "bank-account"),
                    create_input_box("Savings", 1500, "my-savings"),
                    create_input_box("Income", 4500, "monthtly-income"),
                    create_input_box("Investments", 200, "my-investments"),
                ],
            ),
            make_card(
                "Current Debts",
                [create_input_box("Credit Card", 1500, "credit-account")],
            ),
            make_card(
                "Outgoings",
                [
                    create_input_box("Bills/Mortgage", 1500, "monthly-bills"),
                    create_input_box("Shopping", 800, "monthly-shopping"),
                    create_input_box("Savings", 400, "pay-in-savings"),
                    create_input_box("Investments", 0, "pay-in-investments"),
                ],
            ),
        ],
        style={"margin-top": "10px"},
    )


def render_profile_layout():

    return [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("What is Wealh?"),
                        html.P(
                            """\
                            Wealth refers to value of everything a person or family owns. 
                            This includes tangible items such as jewelry, housing, cars, 
                            and other personal property. 
                            Financial assets such as stocks and bonds, 
                            which can be traded for cash, 
                            also contribute to wealth. Wealth is measured as 
                            "net assets," minus how much debt one owes."""
                        ),
                    ],
                    md=4,
                ),
                dbc.Col(
                    [
                        html.H2("Where will you be?"),
                        html.Div(id="waterfall-graph-now",),
                    ]
                ),
            ]
        ),
        profile_settings(),
    ]


@app.callback(
    [Output(f"collapse-{i}", "is_open") for i in range(0, 4)],
    [Input(f"group-{i}-toggle", "n_clicks") for i in range(0, 4)],
    [State(f"collapse-{i}", "is_open") for i in range(0, 4)],
)
def toggle_accordion(n0, n1, n2, n3, is_open0, is_open1, is_open2, is_open3):
    ctx = dash.callback_context

    if not ctx.triggered:
        return ""
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "group-0-toggle" and n0:
        return not is_open0, False, False, False
    if button_id == "group-1-toggle" and n1:
        return False, not is_open1, False, False
    elif button_id == "group-2-toggle" and n2:
        return False, False, not is_open2, False
    elif button_id == "group-3-toggle" and n3:
        return False, False, False, not is_open3
    return False, False, False, False


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
                float(bank_acc),
                float(savings),
                float(salary),
                float(investments),
                0,
                -float(credit_card),
                -float(bills),
                -float(shopping),
                0,
            ],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
        )
    )

    fig.update_layout(
        showlegend=False, plot_bgcolor="#fff", paper_bgcolor="#fff",
    )
    return dcc.Graph(figure=fig)
