import dash
import dash_auth
import os

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True
auth = dash_auth.BasicAuth(
    app, {os.environ.get("LOGIN"): os.environ.get("PASSWORD")}
)

