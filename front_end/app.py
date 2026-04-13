import customtkinter as ctk
from PIL import Image
from back_end.GestionnaireProjet import GestionnaireProjets
import config

_ASSETS = config.get_base_path() / "assets"

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

_HEADER_BG = "#1a1a3e"
_HEADER_ACTIVE = "#2d2d6b"
_APP_BG = "#f0f4f8"


class App(ctk.CTk):
    """Fenêtre principale de l'application."""

    def __init__(self, chemin_json: str):
        super().__init__()
        self.gestionnaire = GestionnaireProjets(chemin_json=chemin_json)

        self.title("Gestion de Projets — SAFRAN")
        self.geometry("1350x820")
        self.minsize(1050, 650)

        self._build_header()
        self._build_content()
        self.show_liste()

    # ── Construction ───────────────────────────────────────────────────────────

    def _build_header(self):
        header = ctk.CTkFrame(self, height=56, fg_color=_HEADER_BG, corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)

        # Logo
        _logo_img = ctk.CTkImage(
            light_image=Image.open(_ASSETS / "logo.png"),
            dark_image=Image.open(_ASSETS / "logo.png"),
            size=(120, 36),
        )
        ctk.CTkLabel(header, image=_logo_img, text="").pack(side="left", padx=22)

        # Séparateur
        ctk.CTkFrame(header, width=1, fg_color="#3a3a6e").pack(
            side="left", fill="y", pady=14, padx=12
        )

        self._btn_projets = ctk.CTkButton(
            header,
            text="Projets",
            width=110,
            height=36,
            fg_color="transparent",
            hover_color=_HEADER_ACTIVE,
            text_color="white",
            font=ctk.CTkFont(size=13),
            command=self.show_liste,
        )
        self._btn_projets.pack(side="left", padx=4)

        self._btn_formulaire = ctk.CTkButton(
            header,
            text="Formulaire",
            width=110,
            height=36,
            fg_color="transparent",
            hover_color=_HEADER_ACTIVE,
            text_color="white",
            font=ctk.CTkFont(size=13),
            command=self.show_formulaire_new,
        )
        self._btn_formulaire.pack(side="left", padx=4)

    def _build_content(self):
        self._content = ctk.CTkFrame(self, fg_color=_APP_BG, corner_radius=0)
        self._content.pack(fill="both", expand=True)

        # Import différé pour éviter les imports circulaires
        from front_end.views.liste_view import ListeView
        from front_end.views.formulaire_view import FormulaireView

        self._liste_view = ListeView(self._content, self.gestionnaire, app=self)
        self._formulaire_view = FormulaireView(
            self._content, self.gestionnaire, app=self
        )

    # ── Navigation ─────────────────────────────────────────────────────────────

    def show_liste(self):
        self._formulaire_view.pack_forget()
        self._liste_view.pack(fill="both", expand=True)
        self._liste_view.refresh()
        self._btn_projets.configure(fg_color=_HEADER_ACTIVE)
        self._btn_formulaire.configure(fg_color="transparent")

    def show_formulaire_new(self):
        self._liste_view.pack_forget()
        self._formulaire_view.load_projet(None, mode="nouveau")
        self._formulaire_view.pack(fill="both", expand=True)
        self._btn_projets.configure(fg_color="transparent")
        self._btn_formulaire.configure(fg_color=_HEADER_ACTIVE)

    def show_formulaire_edit(self, projet_data: dict, mode: str = "modifier"):
        """Ouvre le formulaire pré-rempli (modifier ou dupliquer)."""
        self._liste_view.pack_forget()
        self._formulaire_view.load_projet(projet_data, mode=mode)
        self._formulaire_view.pack(fill="both", expand=True)
        self._btn_projets.configure(fg_color="transparent")
        self._btn_formulaire.configure(fg_color=_HEADER_ACTIVE)
