import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from layout.future_layout import render_future_layout
from layout.investment_layout import render_investment_layout
from layout.profile_layout import render_profile_layout


def generate_main_layout():
    navbar = dbc.NavbarSimple(
        children=[
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
        brand="Ethical Wealth",
        brand_href="/",
        sticky="top",
    )
    body = dbc.Container(id="body", className="mt-4",)
    return html.Div(children=[dcc.Location(id="url"), navbar, body])


def generate_jumbotron():
    return dbc.Jumbotron(
        [
            html.H1("Ethical Wealth", className="display-3"),
            html.P(
                "This platform help you to save money " "ethically.",
                className="lead",
            ),
            html.Hr(className="my-2"),
            html.P("Independent Financial Advisor for a price of a penny "),
            html.P(
                dbc.Button(
                    "Let's start saving", color="primary", href="/current",
                ),
                className="lead",
            ),
        ]
    )


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
        return [1, 1]

