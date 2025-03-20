# components/accordions.py

from dash import html, dcc
import dash_bootstrap_components as dbc
from utils.utils import format_nombre
from utils.data_processing import prepare_data
from utils.kpi_computation import calcule_kpi
from utils.generate_figures import create_figures


def build_accordion_ca(fig_ca_par_client):
    return dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    dbc.Row(
                        [
                            html.Div(
                                [dcc.Graph(figure=fig_ca_par_client)],
                                style={"display": "inline-block"},
                            ),
                        ],
                        align="center",
                        style={
                            "font-family": "Calibri",
                            "font-size": "20px",
                            "justify-content": "space-around",
                            "margin-bottom": "20px",
                            "margin": "5px",
                        },
                    ),
                ],
                title=html.H3("📊 Vue détaillée du chiffre d'affaire annuel"),
            )
        ],
        start_collapsed=True,
    )


def build_accordion_charges(fig_repartition_charges):
    return dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    dbc.Row(
                        [
                            html.Div(
                                dcc.Graph(figure=fig_repartition_charges),
                                style={"width": "100%", "display": "inline-block"},
                            ),
                        ],
                        align="center",
                        style={
                            "font-family": "Calibri",
                            "font-size": "20px",
                            "display": "flex",
                            "justify-content": "space-around",
                            "margin-bottom": "10px",
                        },
                    ),
                ],
                title=html.H3("💰 Vue détaillée des charges"),
            )
        ],
        start_collapsed=True,
    )


def build_accordion_notes_frais(fig_repartition_note_frais, note_frais_moyenne):
    return dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    dbc.Row(
                        [
                            html.Div(
                                [
                                    html.P(
                                        f"Valeur moyenne des notes de frais mensuelles : {format_nombre(note_frais_moyenne)} €",
                                        style={
                                            "font-size": "22px",
                                            "textAlign": "center",
                                        },
                                    ),
                                    html.Br(),
                                ]
                            ),
                            html.Div(
                                [dcc.Graph(figure=fig_repartition_note_frais)],
                                style={"width": "100%", "display": "inline-block"},
                            ),
                        ],
                        align="center",
                        style={
                            "font-family": "Calibri",
                            "font-size": "20px",
                            "display": "flex",
                            "justify-content": "space-around",
                            "margin-bottom": "10px",
                        },
                    ),
                ],
                title=html.H3("🧾 Vue détaillée des notes de frais"),
            )
        ],
        start_collapsed=True,
    )


