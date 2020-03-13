from layout.index_layout import generate_main_layout
from app import app

app.layout = generate_main_layout()
server = app.server

if __name__ == "__main__":
    app.run_server(debug=True)
