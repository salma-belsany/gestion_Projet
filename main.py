from front_end.views.startup_dialog import demander_chemin_json
from front_end.app import App


def main():
    chemin = demander_chemin_json()
    if not chemin:
        return

    app = App(chemin_json=chemin)
    app.mainloop()


if __name__ == "__main__":
    main()
