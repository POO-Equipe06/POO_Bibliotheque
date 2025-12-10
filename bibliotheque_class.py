# Main library class

import csv
from datetime import date
from document_classes import Livre, BandeDessinee, Dictionnaire, Journal
from adherent_class import Adherent
from emprunt_class import Emprunt


class Bibliotheque:

    def __init__(self, nom: str = "Ma Bibliothèque"):
        self.nom = nom
        self.documents = []
        self.adherents = []
        self.emprunts = []

    # ─────────────────────────────────
    # Document management
    # ─────────────────────────────────

    def ajouter_document(self, document):
        self.documents.append(document)
        return True

    def retirer_document(self, doc_id: int) -> bool:
        for doc in self.documents:
            if doc.id == doc_id:
                self.documents.remove(doc)
                return True
        return False

    def trouver_document(self, doc_id: int):
        for doc in self.documents:
            if doc.id == doc_id:
                return doc
        return None

    def lister_documents(self) -> list:
        return self.documents

    def lister_livres_disponibles(self) -> list:
        livres = [doc for doc in self.documents if isinstance(doc, Livre)]
        return [livre for livre in livres if livre.est_disponible]

    # ─────────────────────────────────
    # Member management
    # ─────────────────────────────────

    def ajouter_adherent(self, adherent: Adherent) -> bool:
        # Check if member already exists
        for adh in self.adherents:
            if adh.nom == adherent.nom and adh.prenom == adherent.prenom:
                return False
        self.adherents.append(adherent)
        return True

    def retirer_adherent(self, adherent_id: int) -> bool:
        for adh in self.adherents:
            if adh.id == adherent_id:
                self.adherents.remove(adh)
                return True
        return False

    def trouver_adherent(self, adherent_id: int):
        for adh in self.adherents:
            if adh.id == adherent_id:
                return adh
        return None

    def lister_adherents(self) -> list:
        return self.adherents

    # ─────────────────────────────────
    # Borrowing management
    # ─────────────────────────────────

    def creer_emprunt(self, adherent_id: int, livre_id: int) -> tuple:
        # Check member exists
        adherent = self.trouver_adherent(adherent_id)
        if not adherent:
            return False, "Adhérent non trouvé"

        # Check book exists
        livre = self.trouver_document(livre_id)
        if not livre:
            return False, "Livre non trouvé"

        # Check if it's a book
        if not isinstance(livre, Livre):
            return False, "Document n'est pas un livre"

        # Check if book is available
        if not livre.est_disponible:
            return False, "Livre n'est pas disponible"

        # Create borrowing
        emprunt = Emprunt(adherent_id, livre_id)
        self.emprunts.append(emprunt)

        # Mark book as borrowed
        livre.est_disponible = False
        adherent.ajouter_emprunt(livre_id)

        return True, f"Emprunt créé: {emprunt}"

    def retourner_livre(self, emprunt_id: int) -> tuple:
        emprunt = None
        for e in self.emprunts:
            if e.id == emprunt_id:
                emprunt = e
                break
        if not emprunt:
            return False, "Emprunt non trouvé"
        if not emprunt.est_actif():
            return False, "Livre déjà retourné"
        emprunt.retourner_livre()

        livre = self.trouver_document(emprunt.livre_id)
        if livre:
            livre.est_disponible = True

        adherent = self.trouver_adherent(emprunt.adherent_id)
        if adherent:
            adherent.retirer_emprunt(emprunt.livre_id)

        return True, f"Livre retourné: {emprunt}"

    def lister_emprunts(self, filtre="tous") -> list:
        if filtre == "actifs":
            return [e for e in self.emprunts if e.est_actif()]
        elif filtre == "retournes":
            return [e for e in self.emprunts if not e.est_actif()]
        else:
            return self.emprunts

    def lister_emprunts_en_retard(self, delai_jours: int = 30) -> list:
        return [e for e in self.emprunts if e.est_en_retard(delai_jours)]

    # ─────────────────────────────────
    # File persistence (CSV)
    # ─────────────────────────────────

    def sauvegarder(self):
        # Save adherents
        self._sauvegarder_adherents()
        # Save documents
        self._sauvegarder_documents()
        # Save borrowings
        self._sauvegarder_emprunts()

    def charger(self):
        self._charger_adherents()
        self._charger_documents()
        self._charger_emprunts()

    def _sauvegarder_adherents(self):  # Save members to CSV
        try:
            with open("adherents.csv", "w", newline="", encoding="utf-8") as f:
                for adh in self.adherents:
                    f.write(adh.to_csv() + "\n")
        except Exception as e:
            print(f"Erreur sauvegarde adhérents: {e}")

    def _charger_adherents(self):  # Load members to CSV
        try:
            with open("adherents.csv", "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        adh = Adherent.from_csv(line)
                        if adh:
                            self.adherents.append(adh)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Erreur chargement adhérents: {e}")

    def _sauvegarder_documents(self):  # Save documents to CSV
        try:
            with open("documents.csv", "w", newline="", encoding="utf-8") as f:
                for doc in self.documents:
                    doc_type = type(doc).__name__
                    if isinstance(doc, Livre):
                        f.write(f"Livre,{doc.id},{doc.titre},{doc.auteur},{doc.est_disponible}\n")
                    elif isinstance(doc, BandeDessinee):
                        f.write(f"BD,{doc.id},{doc.titre},{doc.auteur},{doc.dessinateur}\n")
                    elif isinstance(doc, Dictionnaire):
                        f.write(f"Dictionnaire,{doc.id},{doc.titre},{doc.langue}\n")
                    elif isinstance(doc, Journal):
                        f.write(f"Journal,{doc.id},{doc.titre},{doc.date_parution.strftime('%Y-%m-%d')}\n")
        except Exception as e:
            print(f"Erreur sauvegarde documents: {e}")

    def _charger_documents(self):
        try:
            with open("documents.csv", "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        parts = line.strip().split(",")
                        if len(parts) >= 4:
                            doc_type = parts[0]
                            doc_id = int(parts[1])
                            titre = parts[2]

                            if doc_type == "Livre":
                                doc = Livre(titre, parts[3], parts[4] if len(parts) > 4 else True)
                            elif doc_type == "BD":
                                doc = BandeDessinee(titre, parts[3], parts[4] if len(parts) > 4 else "")
                            elif doc_type == "Dictionnaire":
                                doc = Dictionnaire(titre, parts[3])
                            elif doc_type == "Journal":
                                doc = Journal(titre, parts[3])
                            else:
                                continue

                            doc.id = doc_id
                            self.documents.append(doc)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Erreur chargement documents: {e}")

    def _sauvegarder_emprunts(self):  # Save borrowings to CSV
        try:
            with open("emprunts.csv", "w", newline="", encoding="utf-8") as f:
                for emp in self.emprunts:
                    f.write(emp.to_csv() + "\n")
        except Exception as e:
            print(f"Erreur sauvegarde emprunts: {e}")

    def _charger_emprunts(self):  # Load borrowings from CSV
        try:
            with open("emprunts.csv", "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        emp = Emprunt.from_csv(line)
                        if emp:
                            self.emprunts.append(emp)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Erreur chargement emprunts: {e}")
