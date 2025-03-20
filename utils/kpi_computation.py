# utils/kpi_computation.py

import pandas as pd
from .data_processing import categorise_charges
from config import (
    code_ca_prestation,
    code_ca_formation,
    code_matieres_premieres,
    code_note_frais,
    code_salaires,
    code_cotisation_sociales,
    code_charges_except,
    code_charges,
    max_contrib,
)


# Fonction permettant de calculer les indicateurs clés
def calcule_kpi(data_long, max_contrib=max_contrib):

    # CHIFFRE D'AFFAIRE
    ca_prestations = round(
        data_long[data_long["ecriture"].astype(str).str.startswith(code_ca_prestation)][
            "Valeur"
        ].sum()
    )
    ca_formations = round(
        data_long[data_long["ecriture"].astype(str).str.startswith(code_ca_formation)][
            "Valeur"
        ].sum()
    )

    # CA total
    ca_total = ca_prestations + ca_formations

    # CA par client
    ca_par_client = (
        data_long[data_long["Client"] != "Inconnu"]
        .groupby(["Client", "Type"])[["Valeur"]]
        .sum()
        .reset_index()
        .sort_values(by="Valeur", ascending=False)
    )

    # MATIERES PREMIERES
    matieres_premieres = round(
        data_long[
            data_long["ecriture"].astype(str).str.startswith(code_matieres_premieres)
        ]["Valeur"].sum()
    )

    # MARGE BRUTE
    marge_brute = ca_total + matieres_premieres

    # CONTRIBUTION COOPERATIVE
    contribution_coop = round(min(0.11 * marge_brute, max_contrib))

    # SALAIRES
    salaires_brut = round(
        data_long[data_long["ecriture"].astype(str).str.startswith(code_salaires)][
            "Valeur"
        ].sum()
    )

    # COTISATIONS SOCIALES
    cotisations_sociales = round(
        data_long[
            data_long["ecriture"].astype(str).str.startswith(code_cotisation_sociales)
        ]["Valeur"].sum()
    )

    # CHARGES
    df_charges = data_long.loc[data_long["ecriture"].str.startswith((code_charges))]

    # Total Charges
    total_charges = round(df_charges["Valeur"].sum())

    # Charges par poste
    df_charges2 = df_charges.copy()
    df_charges2["type_charge"] = df_charges2["ecriture"].apply(
        lambda x: categorise_charges(x)
    )
    repartition_charges = (
        df_charges2.groupby("type_charge")["Valeur"].sum().abs().reset_index()
    )

    # CHARGES EXCEPTIONNELLES
    charges_exceptionnelles = data_long[
        data_long["ecriture"].astype(str).str.startswith(code_charges_except)
    ]["Valeur"].sum()

    # FRAIS PROFESSIONNELS
    notes_de_frais = data_long[
        data_long["ecriture"].astype(str).str.startswith(code_note_frais)
    ]["Valeur"].sum()

    # Notes de frais par poste
    notes_frais = data_long[
        data_long["ecriture"].astype(str).str.startswith(code_note_frais)
    ]
    repartition_notes_frais = (
        data_long[data_long["ecriture"].str.startswith(code_note_frais, na=False)]
        .groupby("ecriture")["Valeur"]
        .sum()
        .abs()
        .reset_index()
    )

    # Note de frais mensuelle moyenne
    note_frais_moyenne = round(
        notes_frais.groupby("Mois")["Valeur"].sum().mean()
        if not notes_frais.empty
        else 0
    )

    # REPORT année précédente
    report_n = data_long[data_long["ecriture"] == "Report"]["Valeur"].sum()
    provision_salaire_n = data_long.loc[
        data_long["ecriture"].str.startswith("64143000"), "Valeur"
    ].sum()
    provision_charges_n = data_long.loc[
        data_long["ecriture"].str.startswith("64583000"), "Valeur"
    ].sum()
    provision_def_n = data_long.loc[
        data_long["ecriture"].str.startswith("79172000"), "Valeur"
    ].sum()

    report = round(
        report_n + provision_salaire_n + provision_charges_n + provision_def_n
    )

    kpi = {
        "report": report,
        "note_frais_moyenne": note_frais_moyenne,
        "repartition_notes_frais": repartition_notes_frais,
        "ca_prestations": ca_prestations,
        "ca_formations": ca_formations,
        "ca_par_client": ca_par_client,
        "ca_total": ca_total,
        "total_charges": total_charges,
        "charges_exceptionnelles": charges_exceptionnelles,
        "repartition_charges": repartition_charges,
        "cotisations_sociales": cotisations_sociales,
        "notes_de_frais": notes_de_frais,
        "contribution_coop": contribution_coop,
        "salaires_brut": salaires_brut,
        "marge_brute": marge_brute,
        "matieres_premieres": matieres_premieres,
        "notes_de_frais": notes_de_frais,
    }

    return kpi
