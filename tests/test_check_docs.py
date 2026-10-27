"""Exercise broken links and boundaries when extracting standalone documents."""

import importlib.util
from pathlib import Path
import tempfile
import unittest


SPEC = importlib.util.spec_from_file_location(
    "check_docs", Path(__file__).resolve().parents[1] / "tools/check_docs.py"
)
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


class DocumentationChecks(unittest.TestCase):
    def check(self, content, extra=None):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text(content)
            for name, value in (extra or {}).items():
                (root / name).write_text(value)
            return CHECKER.check(root)

    def test_standalone_file_and_anchor(self):
        self.assertEqual(self.check("[Rules](rules.md#file-ownership)", {
            "rules.md": "# Rules\n\n## File ownership\n"
        }), [])

    def test_missing_file(self):
        self.assertTrue(any("missing file" in x for x in self.check("[Old](missing.md)")))

    def test_old_repository_relative_link(self):
        self.assertTrue(any("escapes" in x for x in self.check("[Old](../../.claude/rules/models.md)")))

    def test_missing_anchor(self):
        self.assertTrue(any("missing heading" in x for x in self.check("[Bad](#absent)")))

    def test_code_example_is_not_a_link(self):
        self.assertEqual(self.check("```text\n[Example](not-a-file.md)\n```\n"), [])

    def test_private_path_is_rejected(self):
        self.assertTrue(any("machine-specific" in x for x in self.check("/home/example/private")))


if __name__ == "__main__":
    unittest.main()
