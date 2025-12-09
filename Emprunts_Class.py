# emprunts_classes.py

from datetime import date
import itertools

# Importation des fonctions de validation (safe_date) et des types de base.
# Nous importons 'safe_date' de document_classes.py pour la gestion des dates.
from document_classes import safe_date

# Importation des classes Document et Adherent nécessaires à Emprunt.
# NOTE : Vous devrez vous assurer que ces classes sont disponibles lors de l'exécution.
# Nous allons les définir localement ici pour les besoins de l'exemple et de la structure demandée,
# en utilisant les attributs minimaux requis.

# -----------------------------------------------------------------------
# 📚 Classe de gestion des Emprunts
# -----------------------------------------------------------------------

class Emprunt:
    _id_gen = itertools.count()  # Générateur d’ID unique pour les emprunts

    def __init__(self, adherent, livre, date_emprunt=None):
        self.id = next(Emprunt._id_gen)

        # Le type doit être Adherent et Document/Livre (vérification non implémentée ici)
        self.adherent = adherent
        self.livre = livre

        # La date d'emprunt est obligatoire (safe_date utilise la date d'aujourd'hui par défaut)
        self.date_emprunt = safe_date(date_emprunt)

        # La date de retour est initialement None (l'emprunt est actif)
        self.date_retour = None

    def est_actif(self) -> bool:
        """Vérifie si l'emprunt est encore actif (non retourné)."""
        return self.date_retour is None

    def retourner(self) -> None:
        """Enregistre le retour du livre à la date du jour (si non déjà retourné)."""
        if self.est_actif():
            self.date_retour = date.today()
            # Dans une application réelle, on mettrait à jour self.livre.est_dispo = True
            print(f"Livre '{self.livre.titre}' retourné le {self.date_retour.strftime('%d/%m/%Y')}.")
        else:
            print("Cet emprunt est déjà terminé.")

    def __str__(self):
        statut = "Actif" if self.est_actif() else "Terminé"
        date_ret = (
            self.date_retour.strftime('%d/%m/%Y')
            if self.date_retour else "—"
        )
        return (
            f"[Emprunt #{self.id}] Adhérent: {self.adherent.id} | Livre: {self.livre.id} '{self.livre.titre}'\n"
            f"  → Emprunt: {self.date_emprunt.strftime('%d/%m/%Y')} | Retour: {date_ret} | Statut: {statut}"
        )