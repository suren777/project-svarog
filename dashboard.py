from layout.index_layout import generate_main_layout
from app import app

app.layout = generate_main_layout()

if __name__ == "__main__":
    app.run_server(debug=True, host="192.168.86.117")

