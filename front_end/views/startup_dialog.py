import json
import os
import customtkinter as ctk
from PIL import Image
from tkinter import filedialog, messagebox
from pathlib import Path
import config

_CONFIG_FILE = Path(__file__).resolve().parents[2] / "user_config.json"
_ASSETS = config.get_base_path() / "assets"
_HEADER_BG = "#1a1a3e"


def _charger_config() -> dict:
    try:
        if _CONFIG_FILE.exists():
            with open(_CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except (json.JSONDecodeError, IOError):
        pass
    return {}


def _sauvegarder_config(data: dict):
    try:
        with open(_CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except IOError:
        pass


def demander_chemin_json() -> str:
    """
    Ouvre une fenêtre CTk autonome pour choisir le fichier JSON.
    Retourne le chemin choisi, ou "" si l'utilisateur annule.
    """

    result = {"path": ""}

    root = ctk.CTk()
    root.title("Gestion de Projets — SAFRAN")
    root.geometry("520x300")
    root.resizable(False, False)

    # Centre la fenêtre
    root.update_idletasks()
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw - 520) // 2
    y = (sh - 300) // 2
    root.geometry(f"520x300+{x}+{y}")

    path_var = ctk.StringVar()

    # ── Interface ──────────────────────────────────────────────────────────────

    header = ctk.CTkFrame(root, fg_color=_HEADER_BG, height=64, corner_radius=0)
    header.pack(fill="x")
    header.pack_propagate(False)
    _logo_img = ctk.CTkImage(
        light_image=Image.open(_ASSETS / "logo.png"),
        dark_image=Image.open(_ASSETS / "logo.png"),
        size=(120, 38),
    )
    ctk.CTkLabel(header, image=_logo_img, text="").pack(side="left", padx=20, pady=13)

    body = ctk.CTkFrame(root, fg_color="white", corner_radius=0)
    body.pack(fill="both", expand=True)

    ctk.CTkLabel(
        body,
        text="Sélectionnez votre fichier de projets (projets.json) :",
        font=ctk.CTkFont(size=13),
        text_color="#374151",
    ).pack(anchor="w", padx=24, pady=(20, 8))

    row = ctk.CTkFrame(body, fg_color="transparent")
    row.pack(fill="x", padx=24)
    row.columnconfigure(0, weight=1)

    ctk.CTkEntry(
        row,
        textvariable=path_var,
        placeholder_text="Chemin vers projets.json…",
        fg_color="white",
        border_color="#d1d5db",
        height=36,
        font=ctk.CTkFont(size=12),
    ).grid(row=0, column=0, sticky="ew", padx=(0, 8))

    def parcourir():
        path = filedialog.askopenfilename(
            parent=root,
            title="Sélectionner projets.json",
            filetypes=[("Fichier JSON", "*.json"), ("Tous les fichiers", "*.*")],
        )
        if not path:
            path = filedialog.asksaveasfilename(
                parent=root,
                title="Créer un nouveau projets.json",
                defaultextension=".json",
                filetypes=[("Fichier JSON", "*.json")],
                initialfile="projets.json",
            )
        if path:
            path_var.set(path)

    ctk.CTkButton(
        row,
        text="Parcourir",
        width=100,
        height=36,
        fg_color="#f3f4f6",
        text_color="#374151",
        hover_color="#e5e7eb",
        border_width=1,
        border_color="#d1d5db",
        font=ctk.CTkFont(size=12),
        command=parcourir,
    ).grid(row=0, column=1)

    ctk.CTkLabel(
        body,
        text="Si le fichier n'existe pas encore, il sera créé automatiquement.",
        font=ctk.CTkFont(size=11),
        text_color="#9ca3af",
    ).pack(anchor="w", padx=24, pady=(6, 0))

    def confirmer():
        path = path_var.get().strip()
        if not path:
            messagebox.showwarning("Chemin manquant",
                                   "Veuillez sélectionner ou saisir un chemin.", parent=root)
            return
        if not path.endswith(".json"):
            messagebox.showwarning("Format incorrect",
                                   "Le fichier doit être un .json", parent=root)
            return
        if not os.path.exists(path):
            try:
                os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
                with open(path, "w", encoding="utf-8") as f:
                    json.dump([], f)
            except IOError as e:
                messagebox.showerror("Erreur", f"Impossible de créer le fichier :\n{e}",
                                     parent=root)
                return
        cfg = _charger_config()
        cfg["dernier_json"] = path
        _sauvegarder_config(cfg)
        result["path"] = path
        root.destroy()

    def annuler():
        root.destroy()

    btn_bar = ctk.CTkFrame(body, fg_color="transparent")
    btn_bar.pack(side="bottom", fill="x", padx=24, pady=16)

    ctk.CTkButton(
        btn_bar,
        text="Annuler",
        width=100, height=36,
        fg_color="#f3f4f6", text_color="#374151", hover_color="#e5e7eb",
        font=ctk.CTkFont(size=12),
        command=annuler,
    ).pack(side="right", padx=(8, 0))

    ctk.CTkButton(
        btn_bar,
        text="Ouvrir",
        width=100, height=36,
        fg_color=_HEADER_BG, hover_color="#2d2d6b", text_color="white",
        font=ctk.CTkFont(size=12, weight="bold"),
        command=confirmer,
    ).pack(side="right")

    root.protocol("WM_DELETE_WINDOW", annuler)
    root.mainloop()  # s'arrête proprement quand root.destroy() est appelé

    return result["path"]
