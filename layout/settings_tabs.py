import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from layout.profile_layout import render_profile_settings
from layout.future_layout import render_future_profile_settings
from layout.investment_layout import render_investment_layout

# from layout.investment_layout import render_investment_layout


def generate_tab_panel():
    return (
        dcc.Tabs(
            id="tabs-main",
            value="tab-investment",
            parent_className="custom-tabs",
            className="custom-tabs-container",
            children=[
                dcc.Tab(
                    label="I'm now",
                    value="tab-profile",
                    selected_className="custom-tab--selected",
                ),
                dcc.Tab(
                    label="Future",
                    value="tab-future",
                    selected_className="custom-tab--selected",
                ),
                dcc.Tab(
                    label="Investments",
                    value="tab-investment",
                    selected_className="custom-tab--selected",
                ),
            ],
        ),
        html.Div(id="tab-settings"),
    )


@app.callback(
    [
        Output("tab-settings", "children"),
        Output("results-placeholder", "children"),
    ],
    [Input("tabs-main", "value")],
)
def render_tab(tab):
    if tab == "tab-profile":
        return render_profile_settings()
    elif tab == "tab-future":
        return render_future_profile_settings()
    elif tab == "tab-investment":
        return render_investment_layout()
    else:
        return [1, 1]
