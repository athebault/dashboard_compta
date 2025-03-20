# utils/data_processing.py
import re
import pandas as pd
from config import (
    code_ca,
    code_matieres_premieres,
    code_note_frais,
    code_salaires,
    code_cotisation_sociales,
)


# Extraction des noms de clients
def extract_client(var):
    if "FC_" in var:
        client = var.split("_")[-1]
        type = "prestation"
    else:
        pattern = r"\d{2}/\d{2}\s+(.*?)\d{3}"
        match = re.search(pattern, var)
        if match:
            client = match.group(1)
            type = "formation"
        else:
            client = "Inconnu"
            type = None
    return client, type


# Catégorisation des charges
def categorise_charges(ecriture):
    if ecriture.startswith(code_note_frais):
        type = "Note de frais"
    elif ecriture.startswith(code_cotisation_sociales):
        type = "Cotisations sociales"
    elif ecriture.startswith(code_matieres_premieres):
        type = "Matières premières"
    elif ecriture.startswith(("Contribution")):
        type = "Contribution coopérative"
    else:
        type = None

    return type


def prepare_data(df):

    # Nettoyage et mise en forme des données
    data = df.loc[:, ~df.columns.str.contains("^Unnamed")].dropna(how="all")
    data_long = (
        data.reset_index()
        .melt(
            id_vars="Soldes, comptes et écritures", var_name="Mois", value_name="Valeur"
        )
        .rename(columns={"Soldes, comptes et écritures": "ecriture"})
    )

    # Remplacement des NaN par 0
    data_long["Valeur"] = pd.to_numeric(data_long["Valeur"], errors="coerce").fillna(0)

    # Extraction des périodes
    mois_mapping = {
        "janv.": "01",
        "févr.": "02",
        "mars": "03",
        "avr.": "04",
        "mai": "05",
        "juin": "06",
        "juil.": "07",
        "août": "08",
        "sept.": "09",
        "oct.": "10",
        "nov.": "11",
        "déc.": "12",
    }
    data_long["Date"] = (
        data_long["Mois"].str.extract(r"(\D{3,5})-(\d{2})")[0].map(mois_mapping)
        + "-"
        + data_long["Mois"].str.extract(r"(\d{2})$")[0]
    )
    data_long["Date"] = pd.to_datetime(
        data_long["Date"], format="%m-%y", errors="coerce"
    )
    data_long = data_long.dropna(subset=["Date"])
    data_long["Année"] = data_long["Date"].dt.year
    data_long["Mois"] = data_long["Date"].dt.to_period("M")
    data_long["Trimestre"] = data_long["Date"].dt.to_period("Q")

    # Correction de l'application de la fonction sur la colonne "ecriture"
    data_long[["Client", "Type"]] = (
        data_long["ecriture"].apply(lambda x: extract_client(str(x))).apply(pd.Series)
    )

    # Attribution des catégories de lignes
    data_long["categorie"] = None
    data_long.loc[
        data_long["ecriture"].astype(str).str.startswith(code_ca), "categorie"
    ] = "CA"
    data_long.loc[
        data_long["ecriture"].astype(str).str.startswith(code_matieres_premieres),
        "categorie",
    ] = "Achat matières premières"
    data_long.loc[
        data_long["ecriture"].astype(str).str.startswith(code_note_frais), "categorie"
    ] = "Notes de frais"
    data_long.loc[
        data_long["ecriture"].astype(str).str.startswith(code_salaires), "categorie"
    ] = "Salaires brut"

    return data_long
