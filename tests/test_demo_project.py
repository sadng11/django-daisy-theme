import subprocess
import sys
from pathlib import Path
import pytest


def test_demo_check():
    manage_py = Path(__file__).resolve().parent.parent / "demo" / "manage.py"
    if not manage_py.exists():
        pytest.skip("Demo project not present in repository")
    result = subprocess.run(
        [sys.executable, str(manage_py), "check"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"System check failed: {result.stderr}\nOutput: {result.stdout}"
