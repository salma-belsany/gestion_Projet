import customtkinter as ctk
from tkinter import messagebox
from typing import Optional, Dict, Any

import config
from front_end.widgets.multi_select_dropdown import MultiSelectDropdown
from front_end.widgets.date_picker import DatePickerButton

_PANEL_BG = "white"
_LABEL_COLOR = "#374151"
_SUBTLE = "#9ca3af"
_BORDER = "#e5e7eb"
_BLUE = "#2563eb"
_BLUE_HOVER = "#1d4ed8"


class FormulaireView(ctk.CTkScrollableFrame):
    """Vue formulaire — création / modification / duplication d'un projet.

    Structure :
        ┌──────────────────────────────────────────────┐
        │  Barre de titre + mode                       │
        ├──────────────────┬──────────────┬────────────┤
        │  Infos générales │ Caract. tech │ Statuts    │
        └──────────────────┴──────────────┴────────────┘
        [ Annuler ]                       [ Enregistrer ]
    """

    def __init__(self, parent, gestionnaire, app):
        super().__init__(parent, fg_color="#f0f4f8", corner_radius=0)
        self.gestionnaire = gestionnaire
        self.app = app
        self._mode = "nouveau"
        self._projet_id: Optional[str] = None
        self._choix: dict = config.charger_choix()

        # Stockage des widgets de saisie  { clé_champ: widget }
        self._inputs: Dict[str, Any] = {}
        # Variables pour les groupes de boutons radio  { clé_champ: StringVar }
        self._radio_vars: Dict[str, ctk.StringVar] = {}

        self._build()

    # ══════════════════════════════════════════════════════════════════════════
    # Construction de l'interface
    # ══════════════════════════════════════════════════════════════════════════

    def _build(self):
        # Barre titre
        title_bar = ctk.CTkFrame(self, fg_color="white", height=58, corner_radius=0)
        title_bar.pack(fill="x")
        title_bar.pack_propagate(False)
        ctk.CTkFrame(title_bar, height=1, fg_color=_BORDER).place(
            relx=0, rely=1.0, relwidth=1, anchor="sw"
        )

        self._title_label = ctk.CTkLabel(
            title_bar,
            text="Nouveau projet",
            font=ctk.CTkFont(family="Segoe UI", size=17, weight="bold"),
            text_color="#1f2937",
        )
        self._title_label.pack(side="left", padx=22, pady=14)

        # Zone des 3 panneaux
        panels_row = ctk.CTkFrame(self, fg_color="transparent")
        panels_row.pack(fill="both", expand=True, padx=14, pady=14)
        panels_row.columnconfigure((0, 1, 2), weight=1, uniform="col")
        panels_row.rowconfigure(0, weight=1)

        self._build_panel_general(panels_row)
        self._build_panel_technique(panels_row)
        self._build_panel_statut(panels_row)

        # Barre boutons bas
        btn_bar = ctk.CTkFrame(self, fg_color="white", height=62, corner_radius=0)
        btn_bar.pack(fill="x", pady=(8, 0))
        btn_bar.pack_propagate(False)
        ctk.CTkFrame(btn_bar, height=1, fg_color=_BORDER).place(
            relx=0, rely=0, relwidth=1
        )

        ctk.CTkButton(
            btn_bar,
            text="Annuler",
            width=110,
            height=38,
            fg_color="#f3f4f6",
            text_color="#374151",
            hover_color="#e5e7eb",
            font=ctk.CTkFont(size=13),
            command=self.app.show_liste,
        ).pack(side="right", padx=(6, 22), pady=12)

        ctk.CTkButton(
            btn_bar,
            text="Enregistrer",
            width=130,
            height=38,
            fg_color=_BLUE,
            hover_color=_BLUE_HOVER,
            text_color="white",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._enregistrer,
        ).pack(side="right", padx=6, pady=12)

    # ── Panneau 1 : Informations générales ─────────────────────────────────────

    def _build_panel_general(self, parent):
        panel = self._make_panel(
            parent, "Informations générales", "Identification du projet", col=0
        )
        self._entry(panel, "nom",                    "Nom :")
        self._entry(panel, "collaborateur_referent", "Collaborateur :")
        self._entry(panel, "directory",              "Directory :")
        self._entry(panel, "mots_cles",              "Mots clés :")
        self._dates(panel, "date_debut", "date_fin")

    # ── Panneau 2 : Caractéristiques techniques ────────────────────────────────

    def _build_panel_technique(self, parent):
        panel = self._make_panel(
            parent, "Caractéristiques techniques", "Sélection des paramètres", col=1
        )
        c = self._choix
        self._combobox(panel, "client",               "Client :",               c.get("Clients", []))
        self._multiselect(panel, "type_etude",        "Type d'études :",        c.get("Type d'études", []))
        self._multiselect(panel, "type_calculs",      "Type de calculs :",      c.get("Type de calculs", []))
        self._multiselect(panel, "type_donnees_entrees","Les données d'entrées :", c.get("Type de données d'entrées", []))
        self._multiselect(panel, "logiciels_utilises","Logiciels :",            c.get("Logiciels", []))
        self._multiselect(panel, "livrable",          "Livrables :",            c.get("Livrables", []))

    # ── Panneau 3 : Statuts et contrat ─────────────────────────────────────────

    def _build_panel_statut(self, parent):
        panel = self._make_panel(
            parent, "Statuts et contrat", "État et type de mission", col=2
        )
        c = self._choix
        self._radio_group(panel, "statut",         "Statut",           c.get("Statut", []))
        self._radio_group(panel, "type_activites", "Type d'activités", c.get("Type d'activitées", []))
        self._radio_group(panel, "type_contrat",   "Statut contrat",   c.get("Type de contrat", []))
        self._textarea(panel, "commentaire", "Commentaire :")

    # ══════════════════════════════════════════════════════════════════════════
    # Utilitaires de construction des widgets
    # ══════════════════════════════════════════════════════════════════════════

    def _make_panel(self, parent, title: str, subtitle: str, col: int) -> ctk.CTkFrame:
        panel = ctk.CTkFrame(parent, fg_color=_PANEL_BG, corner_radius=10)
        panel.grid(row=0, column=col, sticky="nsew", padx=5, pady=0)
        panel.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            panel, text=title,
            font=ctk.CTkFont(size=13, weight="bold"), text_color="#1f2937"
        ).pack(anchor="w", padx=16, pady=(16, 2))
        ctk.CTkLabel(
            panel, text=subtitle,
            font=ctk.CTkFont(size=11), text_color=_SUBTLE
        ).pack(anchor="w", padx=16, pady=(0, 4))
        ctk.CTkFrame(panel, height=1, fg_color=_BORDER).pack(
            fill="x", padx=10, pady=(0, 8)
        )
        return panel

    def _field_label(self, parent, text: str):
        ctk.CTkLabel(
            parent, text=text,
            font=ctk.CTkFont(size=12), text_color=_LABEL_COLOR, anchor="w"
        ).pack(fill="x", padx=16, pady=(6, 1))

    def _entry(self, parent, key: str, label: str):
        self._field_label(parent, label)
        w = ctk.CTkEntry(
            parent,
            fg_color="white",
            border_color="#d1d5db",
            height=35,
            font=ctk.CTkFont(size=12),
        )
        w.pack(fill="x", padx=16, pady=(0, 4))
        self._inputs[key] = w

    def _combobox(self, parent, key: str, label: str, options: list):
        self._field_label(parent, label)
        w = ctk.CTkComboBox(
            parent,
            values=options,
            fg_color="white",
            border_color="#d1d5db",
            button_color="#d1d5db",
            button_hover_color="#9ca3af",
            dropdown_fg_color="white",
            dropdown_hover_color="#f3f4f6",
            height=35,
            font=ctk.CTkFont(size=12),
            state="readonly",
        )
        w.set("Sélectionner...")
        w.pack(fill="x", padx=16, pady=(0, 4))
        self._inputs[key] = w

    def _multiselect(self, parent, key: str, label: str, options: list):
        self._field_label(parent, label)
        w = MultiSelectDropdown(parent, options=options)
        w.pack(fill="x", padx=16, pady=(0, 4))
        self._inputs[key] = w

    def _dates(self, parent, key_debut: str, key_fin: str):
        self._field_label(parent, "Date de début :")
        d1 = DatePickerButton(parent, placeholder="jj/mm/aaaa")
        d1.pack(fill="x", padx=16, pady=(0, 4))

        self._field_label(parent, "Date de fin :")
        d2 = DatePickerButton(parent, placeholder="jj/mm/aaaa")
        d2.pack(fill="x", padx=16, pady=(0, 4))

        self._inputs[key_debut] = d1
        self._inputs[key_fin]   = d2

    def _radio_group(self, parent, key: str, label: str, options: list):
        self._field_label(parent, label)
        var = ctk.StringVar(value="")
        self._radio_vars[key] = var

        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=16, pady=(0, 8))

        for opt in options:
            ctk.CTkRadioButton(
                frame, text=opt,
                variable=var, value=opt,
                fg_color=_BLUE, hover_color=_BLUE_HOVER,
                border_color="#d1d5db",
                font=ctk.CTkFont(size=12),
            ).pack(anchor="w", pady=2)

    def _textarea(self, parent, key: str, label: str):
        self._field_label(parent, label)
        w = ctk.CTkTextbox(
            parent,
            height=80,
            fg_color="white",
            border_color="#d1d5db",
            border_width=1,
            font=ctk.CTkFont(size=12),
        )
        w.pack(fill="x", padx=16, pady=(0, 10))
        self._inputs[key] = w

    # ══════════════════════════════════════════════════════════════════════════
    # Chargement / reset / collecte des données
    # ══════════════════════════════════════════════════════════════════════════

    def load_projet(self, projet_data: Optional[dict], mode: str = "nouveau"):
        """Prépare le formulaire selon le mode et les données fournies."""
        self._mode = mode
        self._projet_id = projet_data["id"] if projet_data and mode == "modifier" else None

        titles = {
            "nouveau":   "Nouveau projet",
            "modifier":  f"Modifier — {projet_data.get('nom', '') if projet_data else ''}",
            "dupliquer": f"Dupliquer — {projet_data.get('nom', '') if projet_data else ''}",
        }
        self._title_label.configure(text=titles.get(mode, "Projet"))

        self._reset()

        if projet_data:
            self._fill(projet_data)

        if mode == "dupliquer" and projet_data:
            w = self._inputs.get("nom")
            if isinstance(w, ctk.CTkEntry):
                w.delete(0, "end")
                w.insert(0, f"{projet_data.get('nom', '')} (copie)")

    def _reset(self):
        """Vide tous les champs."""
        for key, w in self._inputs.items():
            if isinstance(w, ctk.CTkEntry):
                w.delete(0, "end")
            elif isinstance(w, ctk.CTkComboBox):
                w.set("Sélectionner...")
            elif isinstance(w, (MultiSelectDropdown, DatePickerButton)):
                w.reset()
            elif isinstance(w, ctk.CTkTextbox):
                w.delete("1.0", "end")
        for var in self._radio_vars.values():
            var.set("")

    def _fill(self, data: dict):
        """Remplit les widgets avec les données d'un projet existant."""
        for key, w in self._inputs.items():
            # Rétro-compatibilité : ancienne clé Mots_cles
            val = data.get(key)
            if val is None and key == "mots_cles":
                val = data.get("Mots_cles", "")
            if val is None:
                val = [] if key in ("type_etude", "type_donnees_entrees",
                                    "type_calculs", "logiciels_utilises", "livrable") else ""

            if isinstance(w, ctk.CTkEntry):
                w.delete(0, "end")
                if val:
                    w.insert(0, str(val))
            elif isinstance(w, ctk.CTkComboBox):
                w.set(val if val else "Sélectionner...")
            elif isinstance(w, MultiSelectDropdown):
                w.set(val if isinstance(val, list) else [])
            elif isinstance(w, DatePickerButton):
                w.set(str(val) if val else "")
            elif isinstance(w, ctk.CTkTextbox):
                w.delete("1.0", "end")
                if val:
                    w.insert("1.0", str(val))

        for key, var in self._radio_vars.items():
            val = data.get(key, "")
            # Au cas où une ancienne donnée stockait une liste
            if isinstance(val, list):
                val = val[0] if val else ""
            var.set(val)

    def _collect(self) -> dict:
        """Récupère toutes les valeurs saisies dans le formulaire."""
        data: dict = {}

        for key, w in self._inputs.items():
            if isinstance(w, ctk.CTkEntry):
                data[key] = w.get().strip()
            elif isinstance(w, ctk.CTkComboBox):
                val = w.get()
                data[key] = "" if val == "Sélectionner..." else val
            elif isinstance(w, MultiSelectDropdown):
                data[key] = w.get()
            elif isinstance(w, DatePickerButton):
                data[key] = w.get()
            elif isinstance(w, ctk.CTkTextbox):
                data[key] = w.get("1.0", "end-1c").strip()

        for key, var in self._radio_vars.items():
            data[key] = var.get()

        return data

    # ══════════════════════════════════════════════════════════════════════════
    # Enregistrement
    # ══════════════════════════════════════════════════════════════════════════

    def _enregistrer(self):
        data = self._collect()

        if self._mode in ("nouveau", "dupliquer"):
            result, errors = self.gestionnaire.creer_projet(data)
        else:  # modifier
            result, errors = self.gestionnaire.modifier_projet(self._projet_id, data)

        if errors:
            messagebox.showerror("Erreur de validation", "\n".join(errors))
            return

        messagebox.showinfo(
            "Enregistrement réussi",
            f"Le projet « {result['nom']} » a été enregistré avec succès.",
        )
        self.app.show_liste()
