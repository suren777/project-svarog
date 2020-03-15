import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output

from app import app
from layout.reusable import create_input_form


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
                    create_input_form(
                        label="Bank Account",
                        id="bank-account",
                        value=1500,
                        label_width=6,
                        input_width=5,
                    ),
                    create_input_form(
                        label="Savings",
                        id="my-savings",
                        value=1500,
                        label_width=6,
                        input_width=5,
                    ),
                    create_input_form(
                        label="Income",
                        id="monthtly-income",
                        value=4500,
                        label_width=6,
                        input_width=5,
                    ),
                    create_input_form(
                        label="Investments",
                        id="my-investments",
                        value=200,
                        label_width=6,
                        input_width=5,
                    ),
                ],
            ),
            make_card(
                "Current Debts",
                [
                    create_input_form(
                        label="Credit Card",
                        id="credit-account",
                        value=2000,
                        label_width=6,
                        input_width=5,
                    )
                ],
            ),
            make_card(
                "Outgoings",
                [
                    create_input_form(
                        label="Bills/Mortgage",
                        id="monthly-bills",
                        value=1500,
                        label_width=6,
                        input_width=5,
                    ),
                    create_input_form(
                        label="Shopping",
                        id="monthly-shopping",
                        value=800,
                        label_width=6,
                        input_width=5,
                    ),
                    create_input_form(
                        label="Savings",
                        id="pay-in-savings",
                        value=400,
                        label_width=6,
                        input_width=5,
                    ),
                    create_input_form(
                        label="Investments",
                        id="pay-in-investments",
                        value=0,
                        label_width=6,
                        input_width=5,
                    ),
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
                            Wealth refers to value of everything a person or
                            family owns.
                            This includes tangible items such as jewelry,
                            housing, cars,
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
                        html.H2("Where are you now?"),
                        html.Div(id="waterfall-graph-now",),
                    ]
                ),
            ]
        ),
        profile_settings(),
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
