# components/layout.py

from dash import html, dcc
import dash_bootstrap_components as dbc


# Construction du layout principal
def build_layout():

    layout = html.Div(
        [
            html.H1(
                "\U0001f4bc Tableau de bord comptable",
                style={"font-family": "Calibri", "font-size": "35px"},
            ),
            html.Br(),
            dbc.Container(
                dcc.Upload(
                    id="upload-data",
                    children=html.Button(
                        "\U0001f4c2 Charger un fichier Excel (.xlsx)",
                        style={"fontSize": "18px"},
                    ),
                    multiple=False,
                    style={
                        "textAlign": "center",
                        "padding": "10px",
                        "border": "2px dashed #ddd",
                        "borderRadius": "10px",
                        "cursor": "pointer",
                        "marginBottom": "20px",
                    },
                )
            ),
            dcc.Store(id="data-store"),
            html.Div(id="output-data-upload"),
            html.Br(),
            dbc.Container(
                [html.H3("Indicateurs de pilotage"), html.Div(id="kpi_cards")]
            ),
            html.Br(),
            html.Br(),
            dbc.Container(
                [
                    dbc.Row(
                        [
                            html.H3(
                                "Évolution du CA, des Notes de frais et des Achats de matières premières"
                            ),
                            html.Br(),
                            html.Br(),
                            dbc.Col(
                                [
                                    html.Label(
                                        "Période de visualisation:",
                                        style={"font-weight": "bold"},
                                    ),
                                    dcc.Dropdown(
                                        id="granularite",
                                        options=[
                                            {"label": "Bilan Mensuel", "value": "Mois"},
                                            {
                                                "label": "Bilan Trimestriel",
                                                "value": "Trimestre",
                                            },
                                            {"label": "Bilan Annuel", "value": "Année"},
                                        ],
                                        value="Mois",
                                        clearable=False,
                                    ),
                                ],
                                width="auto",
                            ),
                            dbc.Col(
                                dcc.Graph(id="graphique_ca"),
                                width=True,
                            ),
                        ],
                        align="center",
                        style={
                            "font-family": "Calibri",
                            "font-size": "20px",
                            "justify-content": "space-around",
                            "margin-bottom": "10px",
                        },
                    )
                ]
            ),
            html.Br(),
            dbc.Container(html.Div(id="accordion_ca")),
            html.Br(),
            dbc.Container(
                dbc.Row(
                    [
                        dbc.Col(html.Div(id="accordion_charges"), width=6),
                        dbc.Col(html.Div(id="accordion_notes_frais"), width=6),
                    ],
                    align="center",
                )
            ),
        ]
    )

    return layout
