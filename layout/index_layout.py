import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from layout.future_layout import render_future_layout
from layout.investment_layout import render_investment_layout
from layout.profile_layout import render_profile_layout

reason1 = dbc.Card(
    dbc.CardBody(
        [
            html.H4("360", className="card-title"),
            html.H6("View on your finance", className="card-subtitle"),
            html.P(
                "It is important to have a view where you are "
                "what are your finances sit",
                className="card-text",
            ),
        ]
    ),
    style={"width": "18rem"},
)

reason2 = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Future", className="card-title"),
            html.H6("What will happen next", className="card-subtitle"),
            html.P(
                "Once you have idea where are you standing "
                "in terms of finance it is important to understand "
                "where you can get. Plus, understand how you can improve it",
                className="card-text",
            ),
        ]
    ),
    style={"width": "18rem"},
)

reason3 = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Investment", className="card-title"),
            html.H6("What else can you do?", className="card-subtitle"),
            html.P(
                "It is good to underdand where you are "
                "and where are you going. But..."
                "Why not to make some money from your money? ",
                className="card-text",
            ),
        ]
    ),
    style={"width": "18rem"},
)


def generate_main_layout():
    navbar = dbc.NavbarSimple(
        children=[
            # dbc.NavItem(dbc.NavLink("Profile", href="/current")),
            dbc.DropdownMenu(
                nav=True,
                in_navbar=True,
                label="Menu",
                children=[
                    dbc.DropdownMenuItem("Current State", href="/current"),
                    dbc.DropdownMenuItem("My Profile Settings", disabled=True),
                    dbc.DropdownMenuItem(
                        "My Future Projections", href="/projections"
                    ),
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem(
                        "Investment Opportunities", href="/investments"
                    ),
                ],
                direction="left",
            ),
        ],
        brand="Conscious Wealth",
        brand_href="/",
        sticky="top",
        color="primary",
        dark=True,
    )
    body = dbc.Container(id="body", className="mt-4",)
    return html.Div(children=[dcc.Location(id="url"), navbar, body])


def generate_jumbotron():
    return [
        dbc.Jumbotron(
            [
                html.H1("Conscious Wealth", className="display-3"),
                html.P(
                    "This platform help you to save money " "Consciously.",
                    className="lead",
                ),
                html.Hr(className="my-2"),
                html.P(
                    "Independent Financial Advisor for a price of a penny "
                ),
                html.P(
                    dbc.Button(
                        "Let's start saving", color="primary", href="/current",
                    ),
                    className="lead",
                ),
            ],
        ),
        dbc.CardDeck([reason1, reason2, reason3]),
    ]


@app.callback(
    Output("body", "children"), [Input("url", "pathname")],
)
def render_page(url):
    if url == "/":
        return generate_jumbotron()
    if url == "/current":
        return render_profile_layout()
    elif url == "/projections":
        return render_future_layout()
    elif url == "/investments":
        return render_investment_layout()
    else:
        return html.H4("404 Page Not Found")

