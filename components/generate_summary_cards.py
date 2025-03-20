# components/generate_summary_cards.py

from dash import html, dcc
import dash_bootstrap_components as dbc
from utils.utils import format_nombre


def generate_summary_card(
    title,
    value,
    color=False,
    backgroundColor="#deb572",
    plot=False,
    figure=None,
    fontsize=("26px", "22px"),
):
    card_body = [
        html.H2(
            title,
            className="card-title",
            style={
                "margin": "0px",
                "font-size": fontsize[0],
                "fontWeight": "600",
                "font-family": "Calibri",
                "display": "flex",
                "justify-content": "space-around",
                "margin-bottom": "5px",
                "color": "black",
            },
        ),
        html.H3(
            f"{format_nombre(value)} €",
            className="card-value",
            style={
                "margin": "0px",
                "font-family": "Calibri",
                "font-size": fontsize[1],
                "fontWeight": "400",
                "color": (
                    "red"
                    if color and value < 0
                    else "green" if color and value > 0 else "black"
                ),
            },
        ),
    ]

    if plot and figure:
        card_body.append(
            html.Div(
                [
                    html.Br(),
                    html.Div(
                        dcc.Graph(figure=figure),
                        style={"width": "100%", "display": "inline-block"},
                    ),
                ]
            )
        )

    return html.Div(
        dbc.Card(
            [
                dbc.CardBody(
                    card_body,
                    style={"textAlign": "center"},
                ),
            ],
            style={
                "font-family": "Calibri",
                "paddingBlock": "1px",
                "backgroundColor": backgroundColor,
                "border": "none",
                "borderRadius": "20px",
                "margin": "10px",
                "display": "flex",
                "justify-content": "space-around",
                "margin-bottom": "10px",
            },
        ),
        style={
            "display": "inline-block",
            "vertical-align": "top",
        },
    )


def generate_all_kpi_cards(summary: dict):
    return dbc.Row(
        [
            dbc.Col(
                generate_summary_card(
                    "\U0001f973  Chiffre d'affaire",
                    summary["ca_total"],
                    plot=summary["plot"],
                    figure=summary["fig_repartition_ca"],
                ),
                width=3,
            ),
            dbc.Col(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                generate_summary_card(
                                    "\U0001fa99  Marge brute",
                                    summary["marge_brute"],
                                    backgroundColor="beige",
                                ),
                                width="auto",
                            ),
                            dbc.Col(
                                generate_summary_card(
                                    "\U0001f680 Résultat",
                                    summary["resultat"],
                                    backgroundColor="beige",
                                    color=True,
                                ),
                                width="auto",
                            ),
                            dbc.Col(
                                generate_summary_card(
                                    "\U0001f4b6  Trésorerie disponible",
                                    summary["treso"],
                                    color=True,
                                    backgroundColor="beige",
                                ),
                                width="auto",
                            ),
                        ],
                        align="center",
                        justify="evenly",
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                generate_summary_card(
                                    "\U0001f911 Salaires bruts",
                                    summary["salaires_brut"],
                                    backgroundColor="lightblue",
                                ),
                                width="auto",
                            ),
                            dbc.Col(
                                generate_summary_card(
                                    "\U0001f3d7\ufe0f Charges sociales",
                                    summary["cotisations_sociales"],
                                    backgroundColor="lightblue",
                                ),
                                width="auto",
                            ),
                            dbc.Col(
                                generate_summary_card(
                                    "\U0001f9fe Notes de frais",
                                    summary["notes_de_frais"],
                                    backgroundColor="lightblue",
                                ),
                                width="auto",
                            ),
                        ],
                        align="center",
                        justify="evenly",
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                generate_summary_card(
                                    "Report Année Préc.",
                                    summary["report"],
                                    color=True,
                                    backgroundColor="lightgrey",
                                    fontsize=("24px", "22px"),
                                ),
                                width="auto",
                            ),
                            dbc.Col(
                                generate_summary_card(
                                    "\U0001fac2 Contrib. Coopérative",
                                    summary["contribution_coop"],
                                    backgroundColor="lightgrey",
                                    fontsize=("24px", "22px"),
                                ),
                                width="auto",
                            ),
                        ],
                        align="center",
                        justify="evenly",
                    ),
                ]
            ),
        ],
        style={
            "backgroundColor": "lavender",
            "margin-bottom": "10px",
            "margin-top": "10px",
            "borderRadius": "20px",
        },
    )
