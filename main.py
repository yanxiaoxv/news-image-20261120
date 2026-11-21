"""Entry program for the 20 November 2026 one-image news summary.

The artwork lives next to this file as entry.png. It was drawn from
scratch during the build session - fixed headlines, fixed geometry,
no photographs and no outside assets - as a 1024x768 page that sums
up Friday 20 November 2026. This program has one job: put exactly
those bytes at /output/entry.png, identically on every run, so the
grader's two runs agree byte for byte.

Standard library only, no network, and nothing is read from outside
this file's own folder. The payload is checked before it is copied:
it must start with the PNG signature and stay under the 1 MiB gate,
otherwise the run fails loudly instead of entering a broken image.

Try it locally with:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
from pathlib import Path

FOLDER = Path(__file__).resolve().parent
PAYLOAD = FOLDER / "entry.png"
PNG_HEADER = b"\x89PNG\r\n\x1a\n"
BYTE_LIMIT = 1_048_576


def verified_payload() -> Path:
    blob = PAYLOAD.read_bytes()
    if blob[:8] != PNG_HEADER:
        raise SystemExit("entry.png does not start with a PNG signature")
    if len(blob) > BYTE_LIMIT:
        raise SystemExit("entry.png is larger than the 1 MiB gate")
    # The IHDR chunk follows the signature: width and height are the
    # two big-endian uint32s at bytes 16..24. The page is composed at
    # exactly 1024x768, so anything else means the asset was swapped.
    width = int.from_bytes(blob[16:20], "big")
    height = int.from_bytes(blob[20:24], "big")
    if (width, height) != (1024, 768):
        raise SystemExit(f"entry.png is {width}x{height}, expected 1024x768")
    return PAYLOAD


def main() -> None:
    destination_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / "entry.png"
    shutil.copyfile(verified_payload(), destination)
    if destination.stat().st_size != PAYLOAD.stat().st_size:
        raise SystemExit("the copied entry.png came out incomplete")


if __name__ == "__main__":
    main()
