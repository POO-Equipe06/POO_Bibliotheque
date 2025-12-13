# 📚 POO_Bibliotheque

> **Système de Gestion de Bibliothèque (Library Management System)**  
> *Projet réalisé dans le cadre du cours 420-2PR-BB - Programmation Orientée Objet*

---

## 📋 Description du Projet

**POO_Bibliotheque** est une application desktop complète permettant la gestion efficace d'une bibliothèque. Développée en **Python** avec une interface graphique moderne via **PyQT6**, cette application met en pratique les concepts fondamentaux de la programmation orientée objet (POO) tels que l'héritage, le polymorphisme et l'encapsulation.

Ce projet répond aux exigences du **TP1 – Bibliothèque** et offre une solution conviviale pour gérer les documents, les membres et les emprunts.

### 🌟 Fonctionnalités Principales

*   **Gestion des Documents** : Ajout et suppression de divers types de documents (Livres, Bandes Dessinées, Dictionnaires, Journaux).
*   **Gestion des Adhérents** : Enregistrement et suivi des membres de la bibliothèque.
*   **Système d'Emprunts** : Création d'emprunts avec validation automatique (vérification de la disponibilité, sélection via listes déroulantes).
*   **Persistance des Données** : Sauvegarde et chargement automatique des données via des fichiers CSV (`adherents.csv`, `documents.csv`, `emprunts.csv`).
*   **Interface Graphique (GUI)** : Interface claire et intuitive divisée en onglets pour une navigation fluide.

---

## 👥 L'Équipe (Équipe 06)

Ce projet est le fruit d'une collaboration entre les membres de l'**Équipe 06** :

*   **Kadmiri Mouad**
*   **Leblanc Jean-Marie**

---

## 🛠️ Installation et Utilisation

### Prérequis

*   Python 3.x installé
*   Bibliothèque PyQT6

### Étapes d'installation

1.  **Cloner le dépôt :**
    ```bash
    git clone https://github.com/POO-Equipe06/POO_Bibliotheque.git
    cd POO_Bibliotheque
    ```

2.  **Installer les dépendances :**
    ```bash
    pip install PyQt6
    ```

3.  **Lancer l'application :**
    ```bash
    python main.py
    ```

---

## 📂 Structure du Projet

Le code est organisé de manière modulaire pour respecter les bonnes pratiques de la POO :

*   `main.py` : Point d'entrée de l'application et gestion de l'interface graphique (GUI).
*   `bibliotheque_class.py` : Classe centrale gérant la logique métier (listes, interactions, sauvegarde).
*   `document_classes.py` : Contient la classe mère `Document` et ses sous-classes (`Livre`, `BandeDessinee`, `Dictionnaire`, `Journal`).
*   `adherent_class.py` : Gestion des membres de la bibliothèque.
*   `emprunt_class.py` : Gestion des transactions d'emprunt et des dates de retour.

---

## 🙏 Remerciements

Nous tenons à exprimer notre gratitude envers notre **professeur, Raouf Babari,** pour ses conseils avisés, son encadrement tout au long de ce cours de Programmation Orientée Objet, et pour nous avoir guidés dans la réalisation de ce travail pratique.

---

*Fait avec 💻 et ☕ par l'Équipe 06.*
