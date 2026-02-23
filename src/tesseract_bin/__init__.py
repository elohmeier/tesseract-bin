import os
import sys
from pathlib import Path

_DATA_DIR = Path(__file__).parent / "data"
TESSERACT_PATH = str(_DATA_DIR / "bin" / "tesseract")
TESSDATA_PREFIX = str(_DATA_DIR / "share" / "tessdata")


def tesseract():
    env = os.environ.copy()
    env.setdefault("TESSDATA_PREFIX", TESSDATA_PREFIX)
    if sys.platform == "win32":
        import subprocess

        raise SystemExit(subprocess.call([TESSERACT_PATH] + sys.argv[1:], env=env))
    else:
        os.execvpe(TESSERACT_PATH, [TESSERACT_PATH] + sys.argv[1:], env)
