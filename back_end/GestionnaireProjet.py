import json
import uuid
import os
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

from back_end.Utilisateur import Utilisateur
from back_end.Projet import Projet
import config


class GestionnaireProjets:
    """Gestionnaire principal des projets avec persistance JSON."""

    def __init__(self, chemin_json: Optional[str] = None):
        self.utilisateur = Utilisateur()
        self.chemin_projets = chemin_json or str(config.PROJETS_JSON)
        self.projets: List[Dict[str, Any]] = self._charger_projets()

    # ── Persistance ────────────────────────────────────────────────────────────

    def _charger_projets(self) -> List[Dict[str, Any]]:
        try:
            if os.path.exists(self.chemin_projets):
                with open(self.chemin_projets, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        return data
        except (json.JSONDecodeError, IOError) as e:
            print(f"⚠️ Erreur chargement : {e}")
        return []

    def _sauvegarder_projets(self) -> bool:
        try:
            with open(self.chemin_projets, "w", encoding="utf-8") as f:
                json.dump(self.projets, f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"❌ Erreur sauvegarde : {e}")
            return False

    # ── Validation ─────────────────────────────────────────────────────────────

    def valider_projet_data(self, data: Dict[str, Any]) -> List[str]:
        erreurs = []
        if not data.get("nom", "").strip():
            erreurs.append("Le nom du projet est requis.")
        return erreurs

    # ── CRUD ───────────────────────────────────────────────────────────────────

    def creer_projet(
        self, data: Dict[str, Any]
    ) -> Tuple[Optional[Dict[str, Any]], List[str]]:
        """Crée un nouveau projet. Retourne (projet_dict, erreurs)."""
        erreurs = self.valider_projet_data(data)
        if erreurs:
            return None, erreurs

        projet = Projet(self.utilisateur.id_utilisateur)
        projet.nom = data.get("nom", "").strip()

        for champ in Projet.CHAMPS_UTILISATEUR:
            if champ in data and hasattr(projet, champ):
                setattr(projet, champ, data[champ])

        projet_dict = projet.to_dict()
        self.projets.append(projet_dict)
        self._sauvegarder_projets()
        return projet_dict, []

    def _appartient_a_utilisateur(self, projet: Dict[str, Any]) -> bool:
        """Vérifie que le projet appartient à l'utilisateur courant (insensible à la casse)."""
        projet_user = (projet.get("id_utilisateur") or "").lower()
        current_user = self.utilisateur.id_utilisateur.lower()
        return projet_user == current_user

    def modifier_projet(
        self, projet_id: str, data: Dict[str, Any]
    ) -> Tuple[Optional[Dict[str, Any]], List[str]]:
        """Modifie un projet existant. Retourne (projet_dict, erreurs)."""
        projet_data = self.trouver_projet(projet_id)
        if not projet_data:
            return None, ["Projet introuvable."]

        if not self._appartient_a_utilisateur(projet_data):
            return None, [
                f"Modification refusée : ce projet appartient à « {projet_data.get('id_utilisateur')} »."
            ]

        erreurs = self.valider_projet_data(data)
        if erreurs:
            return None, erreurs

        if data.get("nom"):
            projet_data["nom"] = data["nom"].strip()

        for champ in Projet.CHAMPS_UTILISATEUR:
            if champ in data:
                projet_data[champ] = data[champ]

        self._sauvegarder_projets()
        return projet_data, []

    def dupliquer_projet(
        self, projet_id: str, nouveau_nom: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Duplique un projet avec un nouvel ID."""
        original = self.trouver_projet(projet_id)
        if not original:
            return None

        copie = {
            **original,
            "id": str(uuid.uuid4()),
            "id_utilisateur": self.utilisateur.id_utilisateur,
            "date_creation": datetime.now().strftime("%Y-%m-%d"),
            "nom": nouveau_nom or f"{original['nom']} (copie)",
        }
        self.projets.append(copie)
        self._sauvegarder_projets()
        return copie

    def supprimer_projet(self, projet_id: str) -> Tuple[bool, str]:
        """Supprime un projet. Retourne (succès, message_erreur)."""
        projet = self.trouver_projet(projet_id)
        if not projet:
            return False, "Projet introuvable."

        if not self._appartient_a_utilisateur(projet):
            return False, (
                f"Suppression refusée : ce projet appartient à « {projet.get('id_utilisateur')} »."
            )

        self.projets = [p for p in self.projets if p["id"] != projet_id]
        ok = self._sauvegarder_projets()
        return ok, "" if ok else "Erreur lors de la sauvegarde."

    def trouver_projet(self, projet_id: str) -> Optional[Dict[str, Any]]:
        return next((p for p in self.projets if p["id"] == projet_id), None)

    # ── Utilitaires ────────────────────────────────────────────────────────────

    def rechercher_projets(self, terme: str) -> List[Dict[str, Any]]:
        t = terme.lower()
        return [
            p for p in self.projets
            if t in p.get("nom", "").lower()
            or t in p.get("mots_cles", "").lower()
            or t in p.get("Mots_cles", "").lower()  # rétro-compatibilité
        ]

    @property
    def nombre_projets(self) -> int:
        return len(self.projets)
