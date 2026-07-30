import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "check_markdown_links", ROOT / "ci" / "check_markdown_links.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_all_tracked_markdown_links_resolve():
    assert module.missing_links(ROOT) == []
