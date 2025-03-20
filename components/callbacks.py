import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

from dash import Input, Output, State, html, dcc
from utils.data_processing import prepare_data
from utils.generate_figures import create_figures, generate_repartition_ca
from utils.kpi_computation import calcule_kpi
from utils.parse_content import parse_contents
from .generate_summary_cards import generate_all_kpi_cards
from .accordeons import (
    build_accordion_ca,
    build_accordion_charges,
    build_accordion_notes_frais,
)


def register_callbacks(app):

    # Callback : chargement du fichier Excel
    @app.callback(
        [Output("data-store", "data"), Output("output-data-upload", "children")],
        [Input("upload-data", "contents")],
        prevent_initial_call=True,
    )
    def update_data(contents):
        if contents is None:
            return None, "Aucun fichier chargé."

        df = parse_contents(contents)
        if isinstance(df, pd.DataFrame):
            return df.to_dict("records"), dbc.Container(
                html.P("✅ Fichier chargé avec succès !")
            )
        else:
            return None, html.Div("⛔ Erreur de chargement de fichier")

    # Callback : génération dynamique des KPI
    @app.callback(
        Output("kpi_cards", "children"),
        Input("data-store", "data"),
        prevent_initial_call=True,
    )
    def update_kpi_display(data, plot=True):
        # (Re)charge les données depuis le fichier local
        if data is None:
            return html.Div("⚠️ Aucune donnée disponible."), None, None, None

        # Preparation des données
        data = pd.DataFrame(data)
        data_long = prepare_data(data)

        # Calcule les KPI
        kpi = calcule_kpi(data_long)

        # Extraire les valeurs
        ca_total = kpi["ca_total"]
        marge_brute = kpi["marge_brute"]
        resultat = round(
            kpi["ca_total"]
            + kpi["salaires_brut"]
            + kpi["cotisations_sociales"]
            + kpi["notes_de_frais"]
            - kpi["contribution_coop"]
        )
        treso = kpi["report"] + resultat
        salaires_brut = kpi["salaires_brut"]
        cotisations_sociales = kpi["cotisations_sociales"]
        notes_de_frais = kpi["notes_de_frais"]
        report = kpi["report"]
        contribution_coop = kpi["contribution_coop"]

        fig_repartition_ca = generate_repartition_ca(kpi["ca_par_client"])

        # Résumé mis à jour pour les KPI (pour layout.py)
        summary = {
            "ca_total": ca_total,
            "ca_prestations": kpi["ca_prestations"],
            "ca_formations": kpi["ca_formations"],
            "marge_brute": marge_brute,
            "resultat": resultat,
            "treso": treso,
            "salaires_brut": salaires_brut,
            "cotisations_sociales": cotisations_sociales,
            "notes_de_frais": notes_de_frais,
            "note_frais_moyenne": kpi["note_frais_moyenne"],
            "report": report,
            "contribution_coop": contribution_coop,
            "plot": plot,
            "fig_repartition_ca": fig_repartition_ca,
        }

        kpi_cards = generate_all_kpi_cards(summary)

        # Génère les composants KPI en HTML
        return kpi_cards

    # Callback : génération dynamique des accordéons
    @app.callback(
        Output("accordion_ca", "children"),
        Output("accordion_charges", "children"),
        Output("accordion_notes_frais", "children"),
        Input("data-store", "data"),
        prevent_initial_call=True,
    )
    def update_kpis_and_accordions(data, plot=True):
        if data is None:
            return html.Div("⚠️ Aucune donnée disponible."), None, None, None

        # Preparation des données
        data = pd.DataFrame(data)
        data_long = prepare_data(data)

        # Recalculer les KPI
        kpi = calcule_kpi(data_long)

        # Générer les figures
        figures = create_figures(kpi)

        # Créer les accordéons mis à jour
        accordion_ca = build_accordion_ca(figures["fig_ca_par_client"])
        accordion_charges = build_accordion_charges(figures["fig_repartition_charges"])
        accordion_notes_frais = build_accordion_notes_frais(
            figures["fig_repartition_note_frais"], kpi["note_frais_moyenne"]
        )

        return accordion_ca, accordion_charges, accordion_notes_frais

    # Callback : graphique principal selon granularité
    @app.callback(
        Output("graphique_ca", "figure"),
        [Input("data-store", "data"), Input("granularite", "value")],
        prevent_initial_call=True,
    )
    def update_main_graph(data, granularite):
        if data is None:
            return px.bar(title="⚠️ Aucune donnée disponible")

        df = pd.DataFrame(data)
        data_long = prepare_data(df)

        if granularite not in ["Mois", "Trimestre", "Année"]:
            return px.bar(title="Granularité non valide")

        categories = [
            "CA",
            "Notes de frais",
            "Achat matières premières",
            "Salaires brut",
        ]
        df_agg = (
            data_long[data_long["categorie"].isin(categories)]
            .groupby([granularite, "categorie"])["Valeur"]
            .sum()
            .reset_index()
        )

        if df_agg.empty:
            return px.bar(title="Pas de données pour ces critères")

        df_agg[granularite] = df_agg[granularite].astype(str)

        fig = px.bar(
            df_agg,
            x=granularite,
            y="Valeur",
            color="categorie",
            barmode="group",
            title="Évolution des finances",
            labels={"Valeur": "Montant (€)", "categorie": "Catégorie"},
        )
        fig.update_layout(xaxis_tickangle=-45)
        return fig
