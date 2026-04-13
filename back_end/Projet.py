from datetime import datetime
import uuid


class Projet:
    CHAMPS_LISTES = [
        "type_etude",
        "type_donnees_entrees",
        "type_calculs",
        "logiciels_utilises",
        "livrable",
    ]
    CHAMPS_UNIQUES = ["client", "statut", "type_activites", "type_contrat"]
    CHAMPS_TEXTE = [
        "collaborateur_referent",
        "mots_cles",
        "commentaire",
        "directory",
        "date_debut",
        "date_fin",
    ]
    CHAMPS_UTILISATEUR = CHAMPS_LISTES + CHAMPS_TEXTE + CHAMPS_UNIQUES

    def __init__(self, id_utilisateur: str):
        self.id = str(uuid.uuid4())
        self.id_utilisateur = id_utilisateur
        self.date_creation = datetime.now().strftime("%Y-%m-%d")
        self.nom = ""

        for champ in self.CHAMPS_LISTES:
            setattr(self, champ, [])
        for champ in self.CHAMPS_TEXTE:
            setattr(self, champ, "")
        for champ in self.CHAMPS_UNIQUES:
            setattr(self, champ, "")  # Valeur unique (str), pas une liste

    def to_dict(self) -> dict:
        return {
            "nom": getattr(self, "nom", ""),
            **{
                k: getattr(self, k)
                for k in self.CHAMPS_TEXTE + self.CHAMPS_LISTES + self.CHAMPS_UNIQUES
            },
            "id": self.id,
            "id_utilisateur": self.id_utilisateur,
            "date_creation": self.date_creation,
        }
