#PyQt6 Graphical User Interface for Library Management System

import sys
from datetime import date
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QComboBox, QListWidget, QListWidgetItem,
    QDialog, QMessageBox, QTabWidget, QSpinBox, QScrollArea)
from PyQt6.QtCore import Qt
from document_classes import Livre, BandeDessinee, Dictionnaire, Journal
from adherent_class import Adherent
from bibliotheque_class import Bibliotheque


class LibraryApp(QMainWindow): #Main application window

    def __init__(self):
        super().__init__()
        self.bibliotheque = Bibliotheque("Ma Bibliothèque")
        self.bibliotheque.charger()

        self.setWindowTitle("📚 Gestion de Bibliothèque")
        self.setGeometry(100, 100, 1200, 800)

        # Create tabs
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Create tab pages
        self.tab_documents = self.create_documents_tab()
        self.tab_adherents = self.create_adherents_tab()
        self.tab_emprunts = self.create_emprunts_tab()

        self.tabs.addTab(self.tab_documents, "📖 Documents")
        self.tabs.addTab(self.tab_adherents, "👥 Adhérents")
        self.tabs.addTab(self.tab_emprunts, "📤 Emprunts")

    # ─────────────────────────────────
    # DOCUMENTS TAB
    # ─────────────────────────────────

    def create_documents_tab(self):
        """Create documents management tab"""
        widget = QWidget()
        layout = QVBoxLayout()

        title = QLabel("Gestion des Documents")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        # Refresh, Delete  and save buttons
        top_button_layout = QHBoxLayout()

        btn_refresh_docs = QPushButton("🔄 Actualiser")
        btn_refresh_docs.clicked.connect(self.actualiser_documents)
        top_button_layout.addWidget(btn_refresh_docs)

        btn_delete_doc = QPushButton("🗑️ Supprimer sélectionné")
        btn_delete_doc.clicked.connect(self.supprimer_document)
        top_button_layout.addWidget(btn_delete_doc)

        btn_save = QPushButton("💾 Sauvegarder")
        btn_save.clicked.connect(self.sauvegarder)
        top_button_layout.addWidget(btn_save)

        top_button_layout.addStretch()
        layout.addLayout(top_button_layout)

        # Scroll area for document types
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()

        # ──────────────────────────────
        # LIVRE section
        # ──────────────────────────────
        livre_layout = QHBoxLayout()
        livre_layout.addWidget(QLabel("📕 Livre:"))

        self.livre_titre_input = QLineEdit()
        self.livre_titre_input.setPlaceholderText("Titre")
        livre_layout.addWidget(self.livre_titre_input)

        self.livre_auteur_input = QLineEdit()
        self.livre_auteur_input.setPlaceholderText("Auteur")
        livre_layout.addWidget(self.livre_auteur_input)

        btn_add_livre = QPushButton("➕ Ajouter Livre")
        btn_add_livre.clicked.connect(lambda: self.ajouter_document_type("Livre"))
        livre_layout.addWidget(btn_add_livre)

        scroll_layout.addLayout(livre_layout)

        # ──────────────────────────────
        # BANDE DESSINEE section
        # ──────────────────────────────
        bd_layout = QHBoxLayout()
        bd_layout.addWidget(QLabel("💭 Bande Dessinée:"))

        self.bd_titre_input = QLineEdit()
        self.bd_titre_input.setPlaceholderText("Titre")
        bd_layout.addWidget(self.bd_titre_input)

        self.bd_auteur_input = QLineEdit()
        self.bd_auteur_input.setPlaceholderText("Scénario")
        bd_layout.addWidget(self.bd_auteur_input)

        self.bd_dessinateur_input = QLineEdit()
        self.bd_dessinateur_input.setPlaceholderText("Dessinateur")
        bd_layout.addWidget(self.bd_dessinateur_input)

        btn_add_bd = QPushButton("➕ Ajouter BD")
        btn_add_bd.clicked.connect(lambda: self.ajouter_document_type("BD"))
        bd_layout.addWidget(btn_add_bd)

        scroll_layout.addLayout(bd_layout)

        # ──────────────────────────────
        # DICTIONNAIRE section
        # ──────────────────────────────
        dico_layout = QHBoxLayout()
        dico_layout.addWidget(QLabel("📗 Dictionnaire:"))

        self.dico_titre_input = QLineEdit()
        self.dico_titre_input.setPlaceholderText("Titre")
        dico_layout.addWidget(self.dico_titre_input)

        self.dico_langue_input = QLineEdit()
        self.dico_langue_input.setPlaceholderText("Langue")
        dico_layout.addWidget(self.dico_langue_input)

        btn_add_dico = QPushButton("➕ Ajouter Dictionnaire")
        btn_add_dico.clicked.connect(lambda: self.ajouter_document_type("Dictionnaire"))
        dico_layout.addWidget(btn_add_dico)

        scroll_layout.addLayout(dico_layout)

        # ──────────────────────────────
        # JOURNAL section
        # ──────────────────────────────
        journal_layout = QHBoxLayout()
        journal_layout.addWidget(QLabel("📰 Journal:"))

        self.journal_titre_input = QLineEdit()
        self.journal_titre_input.setPlaceholderText("Titre")
        journal_layout.addWidget(self.journal_titre_input)

        self.journal_date_input = QLineEdit()
        self.journal_date_input.setPlaceholderText("Date (YYYY-MM-DD)")
        journal_layout.addWidget(self.journal_date_input)

        btn_add_journal = QPushButton("➕ Ajouter Journal")
        btn_add_journal.clicked.connect(lambda: self.ajouter_document_type("Journal"))
        journal_layout.addWidget(btn_add_journal)

        scroll_layout.addLayout(journal_layout)

        scroll_layout.addStretch()
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)

        # List of documents
        layout.addWidget(QLabel("Tous les documents:"))
        self.doc_list = QListWidget()
        layout.addWidget(self.doc_list)

        widget.setLayout(layout)
        return widget

    def ajouter_document_type(self, doc_type: str):
        try:
            if doc_type == "Livre":
                titre = self.livre_titre_input.text().strip()
                auteur = self.livre_auteur_input.text().strip()
                if not titre:
                    QMessageBox.warning(self, "Erreur", "Titre requis!")
                    return

                auteur = auteur or "Inconnu"
                document = Livre(titre, auteur)
                self.livre_titre_input.clear()
                self.livre_auteur_input.clear()

            elif doc_type == "BD":
                titre = self.bd_titre_input.text().strip()
                auteur = self.bd_auteur_input.text().strip()
                dessinateur = self.bd_dessinateur_input.text().strip()
                if not titre:
                    QMessageBox.warning(self, "Erreur", "Titre requis!")
                    return

                auteur = auteur or "Inconnu"
                dessinateur = dessinateur or "Inconnu"
                document = BandeDessinee(titre, auteur, dessinateur)
                self.bd_titre_input.clear()
                self.bd_auteur_input.clear()
                self.bd_dessinateur_input.clear()

            elif doc_type == "Dictionnaire":
                titre = self.dico_titre_input.text().strip()
                langue = self.dico_langue_input.text().strip()
                if not titre:
                    QMessageBox.warning(self, "Erreur", "Titre requis!")
                    return

                langue = langue or "Français"
                document = Dictionnaire(titre, langue)
                self.dico_titre_input.clear()
                self.dico_langue_input.clear()
            else:  # Journal
                titre = self.journal_titre_input.text().strip()
                date_str = self.journal_date_input.text().strip()

                if not titre:
                    QMessageBox.warning(self, "Erreur", "Titre requis!")
                    return

                document = Journal(titre, date_str or date.today())
                self.journal_titre_input.clear()
                self.journal_date_input.clear()

            self.bibliotheque.ajouter_document(document)
            QMessageBox.information(self, "Succès", f"Document ajouté: {document}")
            self.actualiser_documents()
            self.actualiser_combos_emprunts()

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur: {e}")

    def supprimer_document(self):
        item = self.doc_list.currentItem()
        if not item:
            QMessageBox.warning(self, "Erreur", "Sélectionnez un document!")
            return

        # Extract ID from display text
        try:
            text = item.text()
            doc_id = int(text.split("#")[1].split("]")[0])
            if self.bibliotheque.retirer_document(doc_id):
                QMessageBox.information(self, "Succès", "Document supprimé!")
                self.actualiser_documents()
                self.actualiser_combos_emprunts()
            else:
                QMessageBox.warning(self, "Erreur", "Impossible de supprimer!")
        except:
            QMessageBox.critical(self, "Erreur", "Erreur de suppression!")

    def actualiser_documents(self):
        self.doc_list.clear()
        for doc in self.bibliotheque.lister_documents():
            self.doc_list.addItem(str(doc))

    # ─────────────────────────────────
    # ADHERENTS TAB
    # ─────────────────────────────────

    def create_adherents_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Title
        title = QLabel("Gestion des Adhérents")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        # Add member section
        add_layout = QHBoxLayout()
        add_layout.addWidget(QLabel("Nom:"))
        self.adh_nom_input = QLineEdit()
        self.adh_nom_input.setPlaceholderText("Nom")
        add_layout.addWidget(self.adh_nom_input)

        add_layout.addWidget(QLabel("Prénom:"))
        self.adh_prenom_input = QLineEdit()
        self.adh_prenom_input.setPlaceholderText("Prénom")
        add_layout.addWidget(self.adh_prenom_input)

        add_layout.addWidget(QLabel("Email:"))
        self.adh_email_input = QLineEdit()
        self.adh_email_input.setPlaceholderText("Email (optionnel)")
        add_layout.addWidget(self.adh_email_input)

        btn_add_adh = QPushButton("➕ Ajouter")
        btn_add_adh.clicked.connect(self.ajouter_adherent)
        add_layout.addWidget(btn_add_adh)

        layout.addLayout(add_layout)

        # List of members
        layout.addWidget(QLabel("Tous les adhérents:"))
        self.adh_list = QListWidget()
        layout.addWidget(self.adh_list)

        # Refresh, Delete  and save buttons
        button_layout = QHBoxLayout()

        btn_refresh_adh = QPushButton("🔄 Actualiser")
        btn_refresh_adh.clicked.connect(self.actualiser_adherents)
        button_layout.addWidget(btn_refresh_adh)

        btn_delete_adh = QPushButton("🗑️ Supprimer sélectionné")
        btn_delete_adh.clicked.connect(self.supprimer_adherent)
        button_layout.addWidget(btn_delete_adh)

        btn_save = QPushButton("💾 Sauvegarder")
        btn_save.clicked.connect(self.sauvegarder)
        button_layout.addWidget(btn_save)

        layout.addLayout(button_layout)

        widget.setLayout(layout)
        return widget

    def ajouter_adherent(self):
        try:
            nom = self.adh_nom_input.text().strip()
            prenom = self.adh_prenom_input.text().strip()
            email = self.adh_email_input.text().strip()
            if not nom or not prenom:
                QMessageBox.warning(self, "Erreur", "Nom et prénom requis!")
                return
            adherent = Adherent(nom, prenom, email)

            if self.bibliotheque.ajouter_adherent(adherent):
                QMessageBox.information(self, "Succès", f"Adhérent ajouté: {adherent}")
                self.adh_nom_input.clear()
                self.adh_prenom_input.clear()
                self.adh_email_input.clear()
                self.actualiser_adherents()
                self.actualiser_combos_emprunts()
            else:
                QMessageBox.warning(self, "Erreur", "Adhérent déjà existant!")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur: {e}")

    def supprimer_adherent(self):
        item = self.adh_list.currentItem()
        if not item:
            QMessageBox.warning(self, "Erreur", "Sélectionnez un adhérent!")
            return
        try:
            text = item.text()
            adh_id = int(text.split("#")[1].split("]")[0])
            if self.bibliotheque.retirer_adherent(adh_id):
                QMessageBox.information(self, "Succès", "Adhérent supprimé!")
                self.actualiser_adherents()
                self.actualiser_combos_emprunts()
            else:
                QMessageBox.warning(self, "Erreur", "Impossible de supprimer!")
        except:
            QMessageBox.critical(self, "Erreur", "Erreur de suppression!")

    def actualiser_adherents(self):
        self.adh_list.clear()
        for adh in self.bibliotheque.lister_adherents():
            self.adh_list.addItem(str(adh))

    # ─────────────────────────────────
    # EMPRUNTS TAB
    # ─────────────────────────────────

    def create_emprunts_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Title
        title = QLabel("Gestion des Emprunts")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        # Create borrowing section
        borrow_layout = QHBoxLayout()

        borrow_layout.addWidget(QLabel("Adhérent:"))
        self.emp_adh_combo = QComboBox()
        borrow_layout.addWidget(self.emp_adh_combo)

        borrow_layout.addWidget(QLabel("Livre:"))
        self.emp_livre_combo = QComboBox()
        borrow_layout.addWidget(self.emp_livre_combo)

        btn_create_emp = QPushButton("📤 Créer Emprunt")
        btn_create_emp.clicked.connect(self.creer_emprunt)
        borrow_layout.addWidget(btn_create_emp)

        layout.addLayout(borrow_layout)

        # List of borrowings
        layout.addWidget(QLabel("Emprunts actifs:"))
        self.emp_list = QListWidget()
        layout.addWidget(self.emp_list)

        # Refresh, Hand Back and save buttons
        button_layout = QHBoxLayout()

        btn_refresh_emp = QPushButton("🔄 Actualiser")
        btn_refresh_emp.clicked.connect(self.actualiser_emprunts)
        button_layout.addWidget(btn_refresh_emp)

        btn_return_book = QPushButton("📥 Retourner livre")
        btn_return_book.clicked.connect(self.retourner_livre)
        button_layout.addWidget(btn_return_book)

        btn_save = QPushButton("💾 Sauvegarder")
        btn_save.clicked.connect(self.sauvegarder)
        button_layout.addWidget(btn_save)

        layout.addLayout(button_layout)

        widget.setLayout(layout)
        return widget

    def actualiser_combos_emprunts(self):
        # Store selected values
        current_adh = self.emp_adh_combo.currentData() if self.emp_adh_combo.count() > 0 else None
        current_livre = self.emp_livre_combo.currentData() if self.emp_livre_combo.count() > 0 else None

        # Clear and populate adherent combo
        self.emp_adh_combo.clear()
        for adh in self.bibliotheque.lister_adherents():
            self.emp_adh_combo.addItem(adh.get_nom_complet(), adh.id)

        # Clear and populate livre combo (only available books)
        self.emp_livre_combo.clear()
        for livre in self.bibliotheque.lister_livres_disponibles():
            self.emp_livre_combo.addItem(f"{livre.titre} ({livre.auteur})", livre.id)

    def creer_emprunt(self):
        try:
            if self.emp_adh_combo.count() == 0 or self.emp_livre_combo.count() == 0:
                QMessageBox.warning(self, "Erreur", "Veuillez ajouter des adhérents et des livres!")
                return
            adh_id = self.emp_adh_combo.currentData()
            livre_id = self.emp_livre_combo.currentData()

            success, message = self.bibliotheque.creer_emprunt(adh_id, livre_id)
            if success:
                QMessageBox.information(self, "Succès", message)
                self.actualiser_emprunts()
                self.actualiser_combos_emprunts()
            else:
                QMessageBox.warning(self, "Erreur", message)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur: {e}")

    def retourner_livre(self):
        item = self.emp_list.currentItem()
        if not item:
            QMessageBox.warning(self, "Erreur", "Sélectionnez un emprunt!")
            return

        try:
            text = item.text()
            emp_id = int(text.split("#")[1].split("]")[0])

            success, message = self.bibliotheque.retourner_livre(emp_id)

            if success:
                QMessageBox.information(self, "Succès", message)
                self.actualiser_emprunts()
                self.actualiser_combos_emprunts()
            else:
                QMessageBox.warning(self, "Erreur", message)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur: {e}")

    def actualiser_emprunts(self):
        self.emp_list.clear()
        for emp in self.bibliotheque.lister_emprunts("actifs"):
            self.emp_list.addItem(str(emp))

    # ─────────────────────────────────
    # General methods
    # ─────────────────────────────────

    def sauvegarder(self):
        try:
            self.bibliotheque.sauvegarder()
            QMessageBox.information(self, "Succès", "Données sauvegardées!")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur de sauvegarde: {e}")


def main():
    app = QApplication(sys.argv)
    window = LibraryApp()
    window.show()

    # Refresh all displays at startup
    window.actualiser_documents()
    window.actualiser_adherents()
    window.actualiser_emprunts()
    window.actualiser_combos_emprunts()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()