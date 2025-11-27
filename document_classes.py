from datetime import date, datetime
import itertools

# ───────────────────────────────
# 🔧 Fonctions de validation safe
# ───────────────────────────────

def safe_str(value, fallback="Inconnu") -> str:
    try:
        s = str(value).strip()
        return s if s else fallback
    except:
        return fallback

def safe_bool(value, fallback=True) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        v = value.strip().lower()
        if v in ("true", "1", "oui", "yes"):
            return True
        if v in ("false", "0", "non", "no"):
            return False
    if isinstance(value, (int, float)):
        return value != 0
    return fallback

def safe_date(value, fallback=None) -> date:
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except:
            pass
    return fallback or date.today()

# ───────────────────────────────
# 📘 Classe de base : Document
# ───────────────────────────────

class Document:
    _id_gen = itertools.count()   # Générateur d’ID unique

    def __init__(self, titre: str):
        self.id = next(Document._id_gen)
        self.titre = safe_str(titre)

    def __str__(self):
        return f"[{self.__class__.__name__} #{self.id}] '{self.titre}'"



# ───────────────────────────────
# 🟦 Sous-classes
# ───────────────────────────────

class Livre(Document):
    def __init__(self, titre: str, auteur: str, est_disponible=True):
        super().__init__(titre)
        self.auteur = safe_str(auteur)
        self.est_disponible = safe_bool(est_disponible)

    def __str__(self):
        statut = "✅ Disponible" if self.est_disponible else "❌ Emprunté"
        return f"[Livre #{self.id}] '{self.titre}' par {self.auteur} — {statut}"


class BandeDessinee(Document):
    def __init__(self, titre: str, auteur: str, dessinateur: str):
        super().__init__(titre)
        self.auteur = safe_str(auteur)
        self.dessinateur = safe_str(dessinateur)

    def __str__(self):
        return (
            f"[BD #{self.id}] '{self.titre}' — "
            f"Scénario : {self.auteur}, Dessin : {self.dessinateur}"
        )


class Dictionnaire(Document):
    def __init__(self, titre: str, langue: str):
        super().__init__(titre)
        self.langue = safe_str(langue)

    def __str__(self):
        return f"[Dico #{self.id}] '{self.titre}' — {self.langue}"


class Journal(Document):
    def __init__(self, titre: str, date_parution):
        super().__init__(titre)
        self.date_parution = safe_date(date_parution)

    def __str__(self):
        return (
            f"[Journal #{self.id}] '{self.titre}' — "
            f"{self.date_parution.strftime('%d/%m/%Y')}"
        )

# ───────────────────────────────
# 🧪 Exemple de test
# ───────────────────────────────

if __name__ == "__main__":

    docs = [
        Livre("Le Petit Prince", "Antoine de Saint-Exupéry"),
        BandeDessinee("", "Goscinny", "Uderzo"),
        Dictionnaire("Larousse", ""),
        Journal("La Presse", date(2025, 12, 27)),
        Livre("", ""),                    # Test string vide
        Journal("Err", "2025-11-28"),     # Test date en string
        Journal("Invalid", "mauvaise"),   # Test date invalide -> fallback today
    ]

    print("📚 Documents créés :")
    for d in docs:
        print("  →", d)
