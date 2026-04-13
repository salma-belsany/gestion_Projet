import customtkinter as ctk
from tkcalendar import Calendar
from typing import Optional, Callable
from datetime import datetime


class DatePickerButton(ctk.CTkFrame):
    """
    Calendrier inline — s'ouvre/se ferme directement dans le formulaire,
    sans fenêtre séparée (même comportement que MultiSelectDropdown).
    """

    DATE_FORMAT = "%d/%m/%Y"

    def __init__(
        self,
        parent,
        placeholder: str = "jj/mm/aaaa",
        on_change: Optional[Callable[[str], None]] = None,
        **kwargs,
    ):
        kwargs.setdefault("fg_color", "transparent")
        super().__init__(parent, **kwargs)
        self.columnconfigure(0, weight=1)

        self.placeholder = placeholder
        self.on_change = on_change
        self._value: str = ""
        self._expanded: bool = False

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

        # Panneau calendrier (masqué par défaut)
        self._panel = ctk.CTkFrame(
            self,
            fg_color="white",
            border_width=1,
            border_color="#d1d5db",
            corner_radius=6,
        )

        now = datetime.now()
        self._cal = Calendar(
            self._panel,
            selectmode="day",
            year=now.year, month=now.month, day=now.day,
            date_pattern="dd/mm/yyyy",
            background="#1a1a3e",
            foreground="white",
            headersbackground="#2d2d6b",
            headersforeground="white",
            selectbackground="#2563eb",
            selectforeground="white",
            weekendbackground="white",
            weekendforeground="#374151",
            othermonthwebackground="#f9fafb",
            othermonthbackground="#f9fafb",
            normalbackground="white",
            normalforeground="#1f2937",
            bordercolor="#e5e7eb",
            font=("Segoe UI", 10),
        )
        self._cal.pack(padx=6, pady=(6, 0))

        # Barre boutons
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
        # Positionne le calendrier sur la date courante si définie
        if self._value:
            try:
                dt = datetime.strptime(self._value, self.DATE_FORMAT)
                self._cal.selection_set(dt)
            except ValueError:
                pass
        self._panel.grid(row=1, column=0, sticky="ew", pady=(2, 0))
        self._expanded = True

    def _collapse(self):
        self._panel.grid_forget()
        self._expanded = False

    # ── Actions ────────────────────────────────────────────────────────────────

    def _confirm(self):
        self._value = self._cal.get_date()
        self._button.configure(text=self._value, text_color="#1f2937")
        if self.on_change:
            self.on_change(self._value)
        self._collapse()

    def _clear(self):
        self._value = ""
        self._button.configure(text=self.placeholder, text_color="#9ca3af")
        self._collapse()

    # ── API publique ───────────────────────────────────────────────────────────

    def get(self) -> str:
        return self._value

    def set(self, value: str):
        """Accepte jj/mm/aaaa ou yyyy-mm-dd (format JSON)."""
        if not value:
            self._value = ""
            self._button.configure(text=self.placeholder, text_color="#9ca3af")
            return
        try:
            dt = datetime.strptime(value, "%Y-%m-%d")
            value = dt.strftime(self.DATE_FORMAT)
        except ValueError:
            pass
        self._value = value
        self._button.configure(text=self._value, text_color="#1f2937")

    def reset(self):
        self.set("")
