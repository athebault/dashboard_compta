# utils/parse_contents.py

import base64
import io
import pandas as pd
from dash import html


def parse_contents(contents):
    """Décodage du fichier uploadé et conversion en DataFrame pandas"""
    try:
        content_type, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)  # Décodage du contenu base64
        df = pd.read_excel(io.BytesIO(decoded), skiprows=2)  # Lecture du fichier

        # S'assurer que la première colonne a un nom correct
        colonnes = df.columns.tolist()
        colonnes[0] = "Soldes, comptes et écritures"
        df.columns = colonnes

        return df

    except Exception as e:
        return html.Div([f"Erreur lors du chargement du fichier : {str(e)}"])
