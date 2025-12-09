# adherent_classes.py

from datetime import date
import itertools

# Importation des fonctions de validation depuis le fichier de référence
# Note: Nous supposons que document_classes.py est accessible dans le même répertoire.
from document_classes import safe_str, safe_date


# ───────────────────────────────
# 👤 Classe de gestion des Adhérents (Membres)
# ───────────────────────────────

class Adherent:
    _id_gen = itertools.count()  # Générateur d’ID unique pour les adhérents

    def __init__(self, nom: str, prenom: str, date_inscription=None):
        # Attribution d'un ID unique
        self.id = next(Adherent._id_gen)

        # Utilisation de safe_str pour garantir des chaînes de caractères valides
        self.nom = safe_str(nom)
        self.prenom = safe_str(prenom)

        # Utilisation de safe_date pour la date d'inscription (fallback: aujourd'hui)
        # On suppose que safe_date a le même comportement de fallback (date.today())
        # que dans document_classes.py si 'date_inscription' est None.
        self.date_inscription = safe_date(date_inscription)

    def __str__(self):
        # Formatage de la date en JJ/MM/AAAA pour la lisibilité
        date_fmt = self.date_inscription.strftime('%d/%m/%Y')
        return (
            f"[Adhérent #{self.id}] {self.prenom} {self.nom.upper()} "
            f"— Inscrit le : {date_fmt}"
        )


# ───────────────────────────────
# 🧪 Exemple de test (Optionnel)
# ───────────────────────────────

if __name__ == "__main__":
    # Testez la création de quelques adhérents
    adherents = [
        Adherent("Tremblay", "Sophie"),
        Adherent("Lévesque", "Marc", date(2025, 10, 15)),
        Adherent("", "Jean"),  # Test nom vide
        Adherent("Dupont", "Marie", "2024-03-01"),  # Test date en string
        Adherent("Invalide", "Date", "mauvaise_date")  # Test date invalide -> fallback today
    ]

    print("👥 Adhérents créés :")
    for a in adherents:
        print("  →", a)