"""
adherent_class.py
Gère les informations d'un adhérent de la bibliothèque
    et les livres qu'il a actuellement empruntés.
    """

from datetime import date


class Adherent:
    # Représente un membre de la bibliothèque (adhérent)

    _id_counter = 0  # Auto-increment ID

    def __init__(self, nom: str, prenom: str, email: str = ""):
        # Initialise un membre (adhérent)
        Adherent._id_counter += 1
        self.id = Adherent._id_counter
        self.nom = str(nom).strip()
        self.prenom = str(prenom).strip()
        self.email = str(email).strip() if email else ""
        self.livres_empruntes = []  # Liste pour stocker les identifiants (ID) des livres empruntés
        self.date_inscription = date.today()

    def get_nom_complet(self) -> str:
        # Obtenir le nom complet
        return f"{self.prenom} {self.nom}"

    def ajouter_emprunt(self, livre_id: int):
        # Ajouter un livre emprunté
        if livre_id not in self.livres_empruntes:
            self.livres_empruntes.append(livre_id)

    def retirer_emprunt(self, livre_id: int):
        # Retirer un livre emprunté
        if livre_id in self.livres_empruntes:
            self.livres_empruntes.remove(livre_id)

    def nombre_emprunts(self) -> int:
        # Obtenir le nombre de livres empruntés
        return len(self.livres_empruntes)

    def __str__(self):
        # Représentation textuelle
        return f"[Adhérent #{self.id}] {self.get_nom_complet()} ({self.nombre_emprunts()} emprunt(s))"

    def to_csv(self) -> str:
        # Convertir au format CSV
        return f"{self.id},{self.nom},{self.prenom},{self.email},{self.date_inscription}"

    @staticmethod
    def from_csv(line: str):
        # Créer un Adhérent à partir d'une ligne CSV
        parts = line.strip().split(",")
        if len(parts) >= 3:
            adherent = Adherent(parts[1], parts[2], parts[3] if len(parts) > 3 else "")
            adherent.id = int(parts[0])
            if Adherent._id_counter < adherent.id:
                Adherent._id_counter = adherent.id
            return adherent
        return None
