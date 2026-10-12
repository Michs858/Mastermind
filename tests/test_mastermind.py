import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "mastermind_game", PROJECT_ROOT / "Mastermind_blocks-2.py"
)
if SPEC is None or SPEC.loader is None:
    raise ImportError("Could not load Mastermind_blocks-2.py")

mastermind = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mastermind)


class MastermindComparingGuessTests(unittest.TestCase):
    def test_counts_exact_positions(self):
        self.assertEqual(
            mastermind.tael_rigtige_pladser([1, 2, 3, 4], [1, 8, 3, 7]),
            2,
        )

    def test_wrong_counts_exact_positions(self):
            self.assertEqual(
                mastermind.tael_rigtige_pladser([1, 1, 1, 1], [2, 2, 2, 2]),
                0,
            )

    def test_counts_misplaced_colors_once_for_duplicates(self):
        self.assertEqual(
            mastermind.tael_farver_i_kode([1, 1, 2, 3], [1, 2, 1, 4]),
            2,
        )

    def test_exact_guess_has_no_misplaced_colors(self):
        self.assertEqual(
            mastermind.tael_farver_i_kode([1, 2, 3, 4], [1, 2, 3, 4]),
            0,
        )


class MastermindGameFlowTests(unittest.TestCase):
    def make_app(self, guess, code=(1, 2, 3, 4), attempts=0):
        app = mastermind.MastermindApp.__new__(mastermind.MastermindApp)
        app.kode = list(code)
        app.forsog = attempts
        app.gæt_var = unittest.mock.MagicMock()
        app.gæt_var.get.return_value = guess
        app.status = unittest.mock.MagicMock()
        app.submit_button = unittest.mock.MagicMock()
        app.root = unittest.mock.MagicMock()
        app.highscore_panel = unittest.mock.MagicMock()
        app._vis_gaet = unittest.mock.MagicMock()
        app._vis_hemmelig_kode = unittest.mock.MagicMock()
        app._spil_igen = unittest.mock.MagicMock()
        return app

    def test_rejects_guess_with_wrong_length(self):
        app = self.make_app("123")

        with patch.object(mastermind.messagebox, "showwarning") as showwarning:
            app._indsend_gaet()

        self.assertEqual(app.forsog, 0)
        app._vis_gaet.assert_not_called()
        showwarning.assert_called_once()

    def test_rejects_digits_outside_the_palette(self):
        app = self.make_app("1204")

        with patch.object(mastermind.messagebox, "showwarning") as showwarning:
            app._indsend_gaet()

        self.assertEqual(app.forsog, 0)
        app._vis_gaet.assert_not_called()
        showwarning.assert_called_once()

    def test_nonwinning_guess_shows_feedback_and_remaining_attempts(self):
        app = self.make_app("1235")

        app._indsend_gaet()

        self.assertEqual(app.forsog, 1)
        app.status.configure.assert_called_once_with(
            text=(
                "Rigtige tal på forkert plads: 0  |  "
                "Farver placeret rigtigt: 3  |  Forsøg tilbage: 9"
            )
        )
        app.highscore_panel.registrer_score.assert_not_called()

    def test_winning_guess_records_score_and_finishes_game(self):
        app = self.make_app("1234")

        app._indsend_gaet()

        app.status.configure.assert_called_once_with(
            text="Du gættede koden på 1 forsøg!"
        )
        app.submit_button.configure.assert_called_once_with(
            state=mastermind.tk.DISABLED
        )
        app.highscore_panel.registrer_score.assert_called_once_with(1)
        app._spil_igen.assert_called_once_with()

    def test_last_wrong_guess_reveals_code_and_finishes_game(self):
        app = self.make_app("1235", attempts=mastermind.MAKS_FORSOG - 1)

        with patch.object(mastermind.messagebox, "showinfo") as showinfo:
            app._indsend_gaet()

        self.assertEqual(app.forsog, mastermind.MAKS_FORSOG)
        app.status.configure.assert_called_once_with(
            text="Du har ikke flere forsøg tilbage. Koden var:"
        )
        app._vis_hemmelig_kode.assert_called_once_with()
        app.submit_button.configure.assert_called_once_with(
            state=mastermind.tk.DISABLED
        )
        showinfo.assert_called_once()
        app._spil_igen.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
