import dash
from dash_bootstrap_components.themes import SLATE

import dash_auth
import os

external_stylesheets = [SLATE]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True
app.title = "Ethical Wealth"
auth = dash_auth.BasicAuth(
    app, {os.environ.get("LOGIN"): os.environ.get("PASSWORD")}
)

