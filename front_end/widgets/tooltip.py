import tkinter as tk
import customtkinter as ctk


class Tooltip:
    """Affiche une bulle d'aide au survol d'un widget."""

    def __init__(self, widget, text: str, delay: int = 500):
        self.widget = widget
        self.text = text
        self.delay = delay
        self._job = None
        self._popup = None

        widget.bind("<Enter>", self._schedule)
        widget.bind("<Leave>", self._cancel)
        widget.bind("<ButtonPress>", self._cancel)

    def _schedule(self, _event=None):
        self._cancel()
        self._job = self.widget.after(self.delay, self._show)

    def _cancel(self, _event=None):
        if self._job:
            self.widget.after_cancel(self._job)
            self._job = None
        if self._popup:
            self._popup.destroy()
            self._popup = None

    def _show(self):
        x = self.widget.winfo_rootx() + self.widget.winfo_width() // 2
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 4

        self._popup = tk.Toplevel(self.widget)
        self._popup.wm_overrideredirect(True)
        self._popup.attributes("-topmost", True)

        lbl = tk.Label(
            self._popup,
            text=self.text,
            background="#1a1a3e",
            foreground="white",
            font=("Segoe UI", 10),
            padx=8,
            pady=4,
            relief="flat",
        )
        lbl.pack()

        self._popup.update_idletasks()
        w = self._popup.winfo_width()
        self._popup.geometry(f"+{x - w // 2}+{y}")
