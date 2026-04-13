# -*- mode: python ; coding: utf-8 -*-
import sys
from pathlib import Path
import customtkinter

ROOT = Path(SPECPATH)
CTK_PATH = Path(customtkinter.__file__).parent

a = Analysis(
    [str(ROOT / 'main.py')],
    pathex=[str(ROOT)],
    binaries=[],
    datas=[
        # Assets (icônes, logos)
        (str(ROOT / 'assets'), 'assets'),
        # customtkinter (thèmes + images internes)
        (str(CTK_PATH), 'customtkinter'),
        # Fichiers de données
        (str(ROOT / 'choix.json'), '.'),
        # Modules front/back
        (str(ROOT / 'front_end'), 'front_end'),
        (str(ROOT / 'back_end'), 'back_end'),
    ],
    hiddenimports=[
        'customtkinter',
        'PIL',
        'PIL._tkinter_finder',
        'openpyxl',
        'tkcalendar',
        'babel.numbers',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='GestionProjets',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,          # Pas de fenêtre console
    disable_windowed_traceback=False,
    icon=str(ROOT / 'assets' / 'logo.png'),  # Icône de l'exe
)
