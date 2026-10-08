import json
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, simpledialog


HIGHSCORE_FIL = Path(__file__).with_name("mastermind_highscores.json")


def laes_highscores():
    if not HIGHSCORE_FIL.exists():
        return []

    with HIGHSCORE_FIL.open(encoding="utf-8") as fil:
        highscores = json.load(fil)

    if not isinstance(highscores, list):
        raise ValueError("Highscorefilen har et ugyldigt format.")

    for score in highscores:
        if (
            not isinstance(score, dict)
            or not isinstance(score.get("navn"), str)
            or type(score.get("forsog")) is not int
            or score["forsog"] < 1
        ):
            raise ValueError("Highscorefilen indeholder en ugyldig score.")

    return sorted(highscores, key=lambda score: score["forsog"])


def gem_highscore(navn, forsog):
    highscores = laes_highscores()
    highscores.append({"navn": navn, "forsog": forsog})
    highscores.sort(key=lambda score: score["forsog"])

    with HIGHSCORE_FIL.open("w", encoding="utf-8") as fil:
        json.dump(highscores, fil, ensure_ascii=False, indent=2)

    return highscores


class HighscorePanel:
    def __init__(self, parent):
        self.parent = parent
        self.highscores = []

        panel = tk.Frame(parent, bg="#ffffff", padx=16, pady=14)
        panel.grid(row=1, column=1, sticky="nsew")
        panel.columnconfigure(0, weight=1)

        tk.Label(
            panel,
            text="Highscore",
            font=("Segoe UI", 13, "bold"),
            bg="#ffffff",
            fg="#263238",
        ).grid(row=0, column=0, sticky="w")
        tk.Label(
            panel,
            text="Færrest forsøg øverst",
            font=("Segoe UI", 9),
            bg="#ffffff",
            fg="#607d8b",
        ).grid(row=1, column=0, sticky="w", pady=(2, 8))

        self.highscore_list = tk.Listbox(
            panel,
            height=15,
            font=("Segoe UI", 10),
            relief="flat",
            bg="#f7f8f6",
            fg="#263238",
            activestyle="none",
        )
        self.highscore_list.grid(row=2, column=0, sticky="nsew")
        panel.rowconfigure(2, weight=1)

        self.vis_highscores()

    def vis_highscores(self):
        self.highscore_list.delete(0, tk.END)
        try:
            self.highscores = laes_highscores()
        except (OSError, json.JSONDecodeError, ValueError) as fejl:
            self.highscores = []
            messagebox.showerror(
                "Highscore kunne ikke indlæses",
                f"Highscorelisten kunne ikke læses:\n{fejl}",
                parent=self.parent,
            )

        if not self.highscores:
            self.highscore_list.insert(tk.END, "Ingen highscores endnu")
            return

        for placering, score in enumerate(self.highscores, start=1):
            self.highscore_list.insert(
                tk.END, f"{placering:>2}. {score['navn']} – {score['forsog']} forsøg"
            )

    def registrer_score(self, forsog):
        navn = simpledialog.askstring(
            "Highscore",
            f"Du gennemførte på {forsog} forsøg!\nSkriv dit navn:",
            parent=self.parent,
        )
        if navn is not None and navn.strip():
            try:
                gem_highscore(navn.strip(), forsog)
            except (OSError, json.JSONDecodeError, ValueError) as fejl:
                messagebox.showerror(
                    "Highscore kunne ikke gemmes",
                    f"Scoren kunne ikke gemmes:\n{fejl}",
                    parent=self.parent,
                )
            self.vis_highscores()
