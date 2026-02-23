import subprocess
from pathlib import Path

import pytest

import tesseract_bin

HELLO_PNG = Path(__file__).parent / "hello.png"

needs_tesseract = pytest.mark.skipif(
    not Path(tesseract_bin.TESSERACT_PATH).exists(),
    reason="tesseract binary not found (install the built wheel to run this test)",
)


@needs_tesseract
def test_ocr_hello():
    result = subprocess.run(
        [tesseract_bin.TESSERACT_PATH, str(HELLO_PNG), "stdout"],
        capture_output=True,
        text=True,
        env={"TESSDATA_PREFIX": tesseract_bin.TESSDATA_PREFIX},
    )
    assert result.returncode == 0
    assert "Hello, World!" in result.stdout.strip()
