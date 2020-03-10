import dash_html_components as html
from layout.settings_tabs import generate_tab_panel


def generate_main_layout():
    return html.Div(
        children=[
            html.Div(
                id="title-box",
                children=html.H1("Ethical Wealth"),
                className="project-title",
            ),
            html.Div(
                children=[
                    html.Div(
                        className="settings-panel",
                        children=generate_tab_panel(),
                    ),
                    html.Div(
                        id="results-placeholder", className="results-panel"
                    ),
                ],
                className="project-box",
            ),
        ]
    )
