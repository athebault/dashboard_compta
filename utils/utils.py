## Fonction utilitaires ##
import locale

# Initialisation locale pour affichage en français
locale.setlocale(locale.LC_TIME, "French_France")
locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")


# Fonction permettant de formatter l'affichage des valeurs monétaires
def format_nombre(valeur):

    if isinstance(valeur, (int, float)):
        return locale.format_string("%d", round(valeur), grouping=True).replace(
            ",", " "
        )
    return valeur
