# main.py

from dash import Dash, html
import dash_bootstrap_components as dbc

from components.layout import build_layout
from components.callbacks import register_callbacks

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.SLATE],
    title="Tableau de bord de Comptabilité",
    suppress_callback_exceptions=True,
)

app.layout = build_layout()

# Enregistrement des callbacks (graphique + chargement fichier)
register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)
