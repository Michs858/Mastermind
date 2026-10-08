import random
import tkinter as tk
from tkinter import messagebox

from mastermind_highscores import HighscorePanel


MAKS_FORSOG = 10
INTRO_TEKST = (
    f"Regler: Gæt den skjulte kode på 4 tal fra 1 til 8 inden for {MAKS_FORSOG} forsøg. "
    "Et tal kan godt være med flere gange. Efter hvert gæt får du at vide, "
    "hvor mange rigtige tal der står på forkert plads, og hvor mange der står på den rigtige plads."
)
FARVER = {
    1: ("Rød", "#e53935"),
    2: ("Grøn", "#43a047"),
    3: ("Gul", "#fdd835"),
    4: ("Lilla", "#8e5cf6"),
    5: ("Magenta", "#d81b60"),
    6: ("Cyan", "#00acc1"),
    7: ("Orange", "#fb8c00"),
    8: ("Grå", "#757575"),
}


def generer_kode():
    return random.choices(range(1, 9), k=4)


def tael_farver_i_kode(kode, gaet):
    forkerte_kode_tal = [
        kode_tal for kode_tal, gaet_tal in zip(kode, gaet) if kode_tal != gaet_tal
    ]
    forkerte_gaet_tal = [
        gaet_tal for kode_tal, gaet_tal in zip(kode, gaet) if kode_tal != gaet_tal
    ]
    return sum(
        min(forkerte_kode_tal.count(tal), forkerte_gaet_tal.count(tal))
        for tal in set(forkerte_gaet_tal)
    )


def tael_rigtige_pladser(kode, gaet):
    return sum(farve_kode == farve_gaet for farve_kode, farve_gaet in zip(kode, gaet))


class MastermindApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mastermind")
        self.root.geometry("780x650")
        self.root.minsize(700, 560)
        self.root.configure(bg="#f4f1e8")

        self.kode = generer_kode()
        self.forsog = 0

        self._byg_vindue()
        self.entry.focus_set()

    def _byg_vindue(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        titel = tk.Label(
            self.root,
            text="MASTERMIND",
            font=("Segoe UI", 24, "bold"),
            bg="#f4f1e8",
            fg="#263238",
        )
        titel.grid(row=0, column=0, pady=(18, 4))

        indhold = tk.Frame(self.root, bg="#f4f1e8")
        indhold.grid(row=1, column=0, sticky="nsew", padx=24, pady=12)
        indhold.columnconfigure(0, weight=3)
        indhold.columnconfigure(1, weight=2)
        indhold.rowconfigure(1, weight=1)

        self.status = tk.Label(
            indhold,
            text=INTRO_TEKST,
            font=("Segoe UI", 11),
            bg="#f4f1e8",
            fg="#37474f",
            wraplength=650,
        )
        self.status.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 14))

        venstre = tk.Frame(indhold, bg="#ffffff", padx=16, pady=14)
        venstre.grid(row=1, column=0, sticky="nsew", padx=(0, 12))
        venstre.columnconfigure(0, weight=1)

        tk.Label(
            venstre,
            text="Vælg farver",
            font=("Segoe UI", 13, "bold"),
            bg="#ffffff",
            fg="#263238",
        ).grid(row=0, column=0, sticky="w")

        self.palette = tk.Frame(venstre, bg="#ffffff")
        self.palette.grid(row=1, column=0, sticky="w", pady=8)
        for tal, (_, farvekode) in FARVER.items():
            knap = tk.Button(
                self.palette,
                text=str(tal),
                command=lambda farve=tal: self._indsæt_farve(farve),
                bg=farvekode,
                fg=self._tekstfarve(tal),
                activebackground=farvekode,
                width=5,
                height=2,
                relief="flat",
                font=("Segoe UI", 13, "bold"),
                cursor="hand2",
                takefocus=False,
            )
            knap.grid(row=(tal - 1) // 4, column=(tal - 1) % 4, padx=4, pady=4)

        tk.Label(
            venstre,
            text="Dit gæt (4 tal fra 1 til 8):",
            bg="#ffffff",
            fg="#37474f",
            font=("Segoe UI", 10),
        ).grid(row=2, column=0, sticky="w", pady=(10, 3))

        input_row = tk.Frame(venstre, bg="#ffffff")
        input_row.grid(row=3, column=0, sticky="w")
        self.gæt_var = tk.StringVar()
        self.entry = tk.Entry(
            input_row,
            textvariable=self.gæt_var,
            width=10,
            font=("Consolas", 18),
            justify="center",
            relief="solid",
            bd=1,
        )
        self.entry.grid(row=0, column=0, ipady=5)
        self.entry.bind("<Return>", self._tryk_enter)
        self.entry.bind("<BackSpace>", self._tryk_backspace)

        tk.Button(
            input_row,
            text="Slet",
            command=self._slet_input,
            bg="#d32f2f",
            fg="#ffffff",
            activebackground="#b71c1c",
            activeforeground="#ffffff",
            font=("Segoe UI", 10),
            padx=10,
        ).grid(row=0, column=1, padx=(7, 0), ipady=5)

        self.submit_button = tk.Button(
            venstre,
            text="Gæt",
            command=self._indsend_gaet,
            bg="#2e7d32",
            fg="#ffffff",
            activebackground="#1b5e20",
            activeforeground="#ffffff",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            padx=20,
            pady=7,
            cursor="hand2",
        )
        self.submit_button.grid(row=4, column=0, sticky="w", pady=(10, 12))

        self.hemmelig_frame = tk.Frame(venstre, bg="#ffffff")
        self.hemmelig_frame.grid(row=5, column=0, sticky="w")

        tk.Label(
            venstre,
            text="Dine gæt",
            font=("Segoe UI", 13, "bold"),
            bg="#ffffff",
            fg="#263238",
        ).grid(row=6, column=0, sticky="w", pady=(8, 5))

        self.historik = tk.Frame(venstre, bg="#ffffff")
        self.historik.grid(row=7, column=0, sticky="nsew")

        self.highscore_panel = HighscorePanel(indhold)

    @staticmethod
    def _tekstfarve(tal):
        return "#202124" if tal in (3, 6, 7, 8) else "#ffffff"

    def _indsæt_farve(self, farve):
        if len(self.gæt_var.get()) < 4:
            self.entry.insert(tk.END, str(farve))
            self.entry.focus_set()

    def _slet_input(self):
        self.gæt_var.set("")
        self.entry.focus_set()

    def _tryk_enter(self, _):
        self._indsend_gaet()
        return "break"

    def _tryk_backspace(self, _):
        self._slet_input()
        return "break"

    def _indsend_gaet(self):
        tekst = self.gæt_var.get()
        if len(tekst) != 4:
            messagebox.showwarning(
                "Ugyldigt gæt", "Dit gæt skal bestå af præcis 4 tal.", parent=self.root
            )
            return
        if any(tegn not in "12345678" for tegn in tekst):
            messagebox.showwarning(
                "Ugyldigt gæt",
                "Brug kun tallene 1, 2, 3, 4, 5, 6, 7 eller 8.",
                parent=self.root,
            )
            return

        gaet = [int(tegn) for tegn in tekst]
        self.forsog += 1
        self._vis_gaet(gaet)
        antal_farver = tael_farver_i_kode(self.kode, gaet)
        rigtige_pladser = tael_rigtige_pladser(self.kode, gaet)
        self.gæt_var.set("")

        if gaet == self.kode:
            self.status.configure(text=f"Du gættede koden på {self.forsog} forsøg!")
            self.submit_button.configure(state=tk.DISABLED)
            self._registrer_highscore()
            return

        if self.forsog >= MAKS_FORSOG:
            self.status.configure(text="Du har ikke flere forsøg tilbage. Koden var:")
            self._vis_hemmelig_kode()
            self.submit_button.configure(state=tk.DISABLED)
            messagebox.showinfo(
                "Spillet er slut",
                "Du har brugt alle 10 forsøg. Den rigtige kode vises i vinduet.",
                parent=self.root,
            )
            self._spil_igen()
            return

        self.status.configure(
            text=(
                f"Rigtige tal på forkert plads: {antal_farver}  |  "
                f"Farver placeret rigtigt: {rigtige_pladser}  |  "
                f"Forsøg tilbage: {MAKS_FORSOG - self.forsog}"
            )
        )

    def _vis_gaet(self, gaet):
        række = tk.Frame(self.historik, bg="#ffffff")
        række.pack(fill="x", pady=2)
        tk.Label(
            række,
            text=f"{self.forsog:>2}.",
            width=3,
            anchor="w",
            font=("Segoe UI", 10),
            bg="#ffffff",
            fg="#455a64",
        ).pack(side="left")

        for tal in gaet:
            self._farvefelt(række, tal, small=True).pack(side="left", padx=2)

        tk.Label(
            række,
            text=(
                f"  Forkert plads: {tael_farver_i_kode(self.kode, gaet)}"
                f"   Rigtig plads: {tael_rigtige_pladser(self.kode, gaet)}"
            ),
            font=("Segoe UI", 9),
            bg="#ffffff",
            fg="#455a64",
        ).pack(side="left", padx=(5, 0))

    def _farvefelt(self, parent, tal, small=False):
        _, farvekode = FARVER[tal]
        return tk.Label(
            parent,
            text=str(tal),
            width=3 if small else 5,
            height=1 if small else 2,
            bg=farvekode,
            fg=self._tekstfarve(tal),
            font=("Segoe UI", 10 if small else 12, "bold"),
            relief="solid",
            bd=1,
            highlightthickness=0,
            padx=3,
            pady=2,
        )

    def _vis_hemmelig_kode(self):
        tk.Label(
            self.hemmelig_frame,
            text="Den rigtige kode:",
            bg="#ffffff",
            fg="#263238",
            font=("Segoe UI", 10, "bold"),
        ).pack(side="left", padx=(0, 5))
        for tal in self.kode:
            self._farvefelt(self.hemmelig_frame, tal).pack(side="left", padx=2)

    def _registrer_highscore(self):
        
        HighscorePanel.registrer_score(self.forsog)
        self._spil_igen()

    def _spil_igen(self):
        if messagebox.askyesno("Spil igen?", "Vil du starte et nyt spil?", parent=self.root):
            self._nyt_spil()
        else:
            self.root.destroy()

    def _nyt_spil(self):
        self.kode = generer_kode()
        self.forsog = 0
        self.status.configure(
            text=INTRO_TEKST,
            fg="#37474f",
        )
        self.submit_button.configure(state=tk.NORMAL)
        self.gæt_var.set("")
        for widget in self.historik.winfo_children():
            widget.destroy()
        for widget in self.hemmelig_frame.winfo_children():
            widget.destroy()
        self.entry.focus_set()


if __name__ == "__main__":
    vindue = tk.Tk()
    app = MastermindApp(vindue)
    vindue.mainloop()
