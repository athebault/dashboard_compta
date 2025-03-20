import plotly.express as px
from .kpi_computation import calcule_kpi
from .utils import format_nombre


def create_figures(kpi):

    ca_par_client = kpi["ca_par_client"]
    total_charges = kpi["total_charges"]
    repartition_charges = kpi["repartition_charges"]
    repartition_notes_frais = kpi["repartition_notes_frais"]
    notes_de_frais = kpi["notes_de_frais"]

    fig_repartition_ca = generate_repartition_ca(ca_par_client)
    fig_ca_par_client = generate_ca_par_client(ca_par_client)
    fig_repartition_charges = generate_repartition_charges(
        repartition_charges, total_charges
    )
    fig_repartition_note_frais = generate_repartition_note_frais(
        repartition_notes_frais, notes_de_frais
    )

    return {
        "fig_repartition_ca": fig_repartition_ca,
        "fig_ca_par_client": fig_ca_par_client,
        "fig_repartition_charges": fig_repartition_charges,
        "fig_repartition_note_frais": fig_repartition_note_frais,
    }


def generate_repartition_ca(ca_par_client):
    # Chiffre d'affaire par type d'activité
    fig_repartition_ca = px.pie(
        ca_par_client.groupby("Type", as_index=False).sum(),
        names="Type",
        values="Valeur",
        title="\U0001f4b0 Répartition du chiffre d'affaire",
        custom_data=[
            ca_par_client.groupby("Type")["Valeur"].sum().apply(format_nombre)
        ],
    )
    fig_repartition_ca.update_traces(
        hovertemplate="<b>%{label}</b><br>CA généré: %{customdata} €"
    )
    fig_repartition_ca.update_layout(
        legend=dict(orientation="h", yanchor="top", y=-0.3, xanchor="right", x=1),
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=200,
    )

    return fig_repartition_ca


def generate_ca_par_client(ca_par_client):
    # Chiffre d'affaire par client
    fig_ca_par_client = px.bar(
        ca_par_client.groupby("Client", as_index=False).sum().sort_values(by="Valeur"),
        x="Valeur",
        y="Client",
        color="Type",
        title="CA par client",
        custom_data=[
            ca_par_client.groupby("Client")["Valeur"]
            .sum()
            .sort_values()
            .apply(format_nombre)
        ],
    )
    fig_ca_par_client.update_traces(
        hovertemplate="<b>%{label}</b><br>CA généré: %{customdata} €"
    )

    return fig_ca_par_client


def generate_repartition_charges(repartition_charges, total_charges):
    # Répartition des charges
    fig_repartition_charges = px.pie(
        repartition_charges.groupby("type_charge", as_index=False).sum(),
        names="type_charge",
        values="Valeur",
        title=f"<b>\U0001f4b8 Répartition des charges</b><br>Total : {format_nombre(total_charges)} €",
        custom_data=[
            repartition_charges.groupby("type_charge")["Valeur"]
            .sum()
            .apply(format_nombre)
        ],
    )
    fig_repartition_charges.update_traces(
        hovertemplate="<b>%{label}</b><br>Montant: %{customdata} €"
    )
    fig_repartition_charges.update_layout(
        legend=dict(orientation="h", yanchor="top", y=0.1, xanchor="right", x=1),
        height=450,
        width=500,
    )

    return fig_repartition_charges


def generate_repartition_note_frais(repartition_notes_frais, notes_de_frais):
    # Répartition des notes de frais
    fig_repartition_note_frais = px.pie(
        repartition_notes_frais.groupby("ecriture", as_index=False).sum(),
        names="ecriture",
        values="Valeur",
        title=f"<b>\U0001f9fe Répartition des notes de frais</b><br>Total : {format_nombre(round(notes_de_frais))} €",
        custom_data=[
            repartition_notes_frais.groupby("ecriture")["Valeur"]
            .sum()
            .apply(format_nombre)
        ],
    )
    fig_repartition_note_frais.update_traces(
        hovertemplate="<b>%{label}</b><br>Montant: %{customdata} €"
    )
    fig_repartition_note_frais.update_layout(
        legend=dict(orientation="h", yanchor="top", y=0.01, xanchor="right", x=1),
        height=650,
        width=500,
    )

    return fig_repartition_note_frais
