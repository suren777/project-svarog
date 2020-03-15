import dash
from dash_bootstrap_components.themes import SLATE
from common.extensions import cache

import dash_auth
import os

external_stylesheets = [SLATE]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True
app.title = "Conscious Wealth"
auth = dash_auth.BasicAuth(
    app, {os.environ.get("LOGIN"): os.environ.get("PASSWORD")}
)
CACHE_CONFIG = {"CACHE_TYPE": "simple"}
cache.init_app(app.server, config=CACHE_CONFIG)
