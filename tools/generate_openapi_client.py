from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OPENAPI = REPO_ROOT / "openapi.yaml"
CONFIG = Path(__file__).resolve().parent / "openapi-python-client.yaml"

GEN_PKG_NAME = "collector_core_api_client"
DEST = REPO_ROOT / "collector_core" / "api_client"


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="openapi-client-") as tmp:
        build_dir = Path(tmp)

        run(
            [
                "poetry",
                "run",
                "openapi-python-client",
                "generate",
                "--path",
                str(OPENAPI),
                "--config",
                str(CONFIG),
                "--output-path",
                str(build_dir),
                "--overwrite",
            ]
        )

        src_pkg = build_dir / GEN_PKG_NAME
        if not src_pkg.exists():
            raise RuntimeError(f"Generated package not found: {src_pkg}")

        if DEST.exists():
            shutil.rmtree(DEST)
        shutil.copytree(src_pkg, DEST)

    run(["poetry", "run", "isort", str(DEST)])
    run(["poetry", "run", "black", str(DEST)])


if __name__ == "__main__":
    main()
