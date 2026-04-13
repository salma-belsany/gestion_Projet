import customtkinter as ctk
from typing import List, Optional, Callable


class MultiSelectDropdown(ctk.CTkFrame):
    """
    Dropdown multi-sélection inline (sans fenêtre séparée).
    Un clic sur le bouton étend/rétracte la liste de cases à cocher
    directement dans le formulaire — aucun Toplevel, aucun grab.
    """

    def __init__(
        self,
        parent,
        options: List[str],
        placeholder: str = "Sélectionner...",
        on_change: Optional[Callable[[List[str]], None]] = None,
        **kwargs,
    ):
        kwargs.setdefault("fg_color", "transparent")
        super().__init__(parent, **kwargs)
        self.columnconfigure(0, weight=1)

        self.options = options
        self.placeholder = placeholder
        self.on_change = on_change
        self._selected: List[str] = []
        self._expanded: bool = False
        self._check_vars: dict = {}

        self._build()

    # ── Construction ───────────────────────────────────────────────────────────

    def _build(self):
        # Bouton principal
        self._button = ctk.CTkButton(
            self,
            text=self.placeholder,
            anchor="w",
            fg_color="white",
            text_color="#9ca3af",
            hover_color="#f9fafb",
            border_width=1,
            border_color="#d1d5db",
            height=35,
            font=ctk.CTkFont(size=12),
            command=self._toggle,
        )
        self._button.grid(row=0, column=0, sticky="ew")

        # Panneau déroulant (masqué par défaut)
        self._panel = ctk.CTkFrame(
            self,
            fg_color="white",
            border_width=1,
            border_color="#d1d5db",
            corner_radius=6,
        )
        # Ne pas afficher tout de suite (grid_forget implicite)

        # Cases à cocher (toutes visibles, pas de scroll interne —
        # le CTkScrollableFrame parent gère le défilement global)
        inner = ctk.CTkFrame(self._panel, fg_color="white")
        inner.pack(fill="both", expand=True, padx=4, pady=(4, 0))

        for opt in self.options:
            var = ctk.BooleanVar(value=False)
            self._check_vars[opt] = var
            ctk.CTkCheckBox(
                inner,
                text=opt,
                variable=var,
                fg_color="#2563eb",
                hover_color="#1d4ed8",
                border_color="#d1d5db",
                font=ctk.CTkFont(size=12),
            ).pack(anchor="w", padx=8, pady=3)

        # Barre OK / Effacer
        btn_row = ctk.CTkFrame(self._panel, fg_color="#f9fafb", height=40)
        btn_row.pack(fill="x", pady=(4, 0))
        btn_row.pack_propagate(False)

        ctk.CTkButton(
            btn_row,
            text="OK",
            command=self._confirm,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            height=28,
            width=60,
            font=ctk.CTkFont(size=12),
        ).pack(side="right", padx=8, pady=6)

        ctk.CTkButton(
            btn_row,
            text="Effacer",
            command=self._clear,
            fg_color="#6b7280",
            hover_color="#4b5563",
            height=28,
            width=72,
            font=ctk.CTkFont(size=12),
        ).pack(side="right", padx=(0, 4), pady=6)

    # ── Toggle ─────────────────────────────────────────────────────────────────

    def _toggle(self):
        if self._expanded:
            self._collapse()
        else:
            self._expand()

    def _expand(self):
        # Synchronise les cases avec la sélection courante
        for opt, var in self._check_vars.items():
            var.set(opt in self._selected)
        self._panel.grid(row=1, column=0, sticky="ew", pady=(2, 0))
        self._expanded = True

    def _collapse(self):
        self._panel.grid_forget()
        self._expanded = False

    # ── Actions ────────────────────────────────────────────────────────────────

    def _confirm(self):
        self._selected = [opt for opt, var in self._check_vars.items() if var.get()]
        self._refresh_label()
        if self.on_change:
            self.on_change(self._selected)
        self._collapse()

    def _clear(self):
        for var in self._check_vars.values():
            var.set(False)

    # ── Label ──────────────────────────────────────────────────────────────────

    def _refresh_label(self):
        if not self._selected:
            self._button.configure(text=self.placeholder, text_color="#9ca3af")
        elif len(self._selected) <= 2:
            self._button.configure(
                text=", ".join(self._selected), text_color="#1f2937"
            )
        else:
            self._button.configure(
                text=f"{len(self._selected)} sélectionné(s)", text_color="#1f2937"
            )

    # ── API publique ───────────────────────────────────────────────────────────

    def get(self) -> List[str]:
        return self._selected.copy()

    def set(self, values: List[str]):
        self._selected = [v for v in (values or []) if v in self.options]
        self._refresh_label()
        if self._expanded:
            for opt, var in self._check_vars.items():
                var.set(opt in self._selected)

    def reset(self):
        self._selected = []
        self._refresh_label()
        if self._expanded:
            self._collapse()
