import tempfile
import unittest
from pathlib import Path

from file_organizer import category_for, available_destination, planned_moves


class FileOrganizerTests(unittest.TestCase):
    def test_category_is_case_insensitive(self):
        self.assertEqual(category_for(Path("PHOTO.JPG")), "Images")
        self.assertEqual(category_for(Path("notes.pdf")), "Documents")
        self.assertEqual(category_for(Path("unknown.xyz")), "Others")

    def test_existing_destination_gets_new_name(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            original = folder / "report.pdf"
            original.write_text("existing", encoding="utf-8")
            result = available_destination(original)
            self.assertEqual(result.name, "report_1.pdf")
            self.assertFalse(result.exists())

    def test_planned_moves_ignores_subfolders(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            (folder / "photo.png").write_text("image", encoding="utf-8")
            (folder / "nested").mkdir()
            (folder / "nested" / "inside.txt").write_text("text", encoding="utf-8")
            moves = planned_moves(folder)
            self.assertEqual(len(moves), 1)
            self.assertEqual(moves[0][1].parent.name, "Images")


if __name__ == "__main__":
    unittest.main()
