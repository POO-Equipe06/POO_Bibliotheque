"""
emprunt_class.py
Classe pour gérer les transactions d'emprunt de livres. Suit quel adhérent a emprunté quel livre et quand.
"""

from datetime import date, timedelta


class Emprunt:
    # Représente une transaction d'emprunt de livre

    _id_counter = 0  # Auto-increment ID

    def __init__(self, adherent_id: int, livre_id: int, date_emprunt: date = None):
        # Initialiser une transaction d'emprunt
        Emprunt._id_counter += 1
        self.id = Emprunt._id_counter
        self.adherent_id = adherent_id
        self.livre_id = livre_id
        self.date_emprunt = date_emprunt or date.today()
        self.date_retour = None  # Si la valeur est None, le livre est toujours emprunté.

    def retourner_livre(self, date_retour: date = None):
        # Marquer le livre comme retourné
        self.date_retour = date_retour or date.today()

    def est_actif(self) -> bool:
        # Vérifier si l'emprunt est toujours actif (livre non retourné)
        return self.date_retour is None

    def jours_emprunt(self) -> int:
        # Calculer le nombre de jours d'emprunt
        if self.est_actif():
            return (date.today() - self.date_emprunt).days
        else:
            return (self.date_retour - self.date_emprunt).days

    def est_en_retard(self, delai_jours: int = 30) -> bool:
        # Vérifier si le livre est en retard (emprunté depuis plus de jours_de_délai)
        return self.est_actif() and self.jours_emprunt() > delai_jours

    def __str__(self):
        # Représentation textuelle
        status = "🟢 Actif" if self.est_actif() else "🔴 Retourné"
        date_ret = f" → {self.date_retour.strftime('%d/%m/%Y')}" if self.date_retour else ""
        return (
            f"[Emprunt #{self.id}] Adhérent #{self.adherent_id} "
            f"emprunte Livre #{self.livre_id} "
            f"({self.date_emprunt.strftime('%d/%m/%Y')}{date_ret}) {status}"
        )

    def to_csv(self) -> str:
        # Convertir au format CSV
        date_ret = self.date_retour.strftime("%Y-%m-%d") if self.date_retour else ""
        return (
            f"{self.id},{self.adherent_id},{self.livre_id},"
            f"{self.date_emprunt.strftime('%Y-%m-%d')},{date_ret}"
        )

    @staticmethod
    def from_csv(line: str):
        # Créer un Emprunt à partir d'une ligne CSV
        parts = line.strip().split(",")
        if len(parts) >= 4:
            try:
                emprunt_id = int(parts[0])
                adherent_id = int(parts[1])
                livre_id = int(parts[2])
                date_emprunt = date.fromisoformat(parts[3])

                emprunt = Emprunt(adherent_id, livre_id, date_emprunt)
                emprunt.id = emprunt_id

                if len(parts) > 4 and parts[4]:
                    emprunt.date_retour = date.fromisoformat(parts[4])

                if Emprunt._id_counter < emprunt_id:
                    Emprunt._id_counter = emprunt_id

                return emprunt
            except:
                return None
        return None
