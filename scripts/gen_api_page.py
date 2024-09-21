"""Generate the API reference page."""  # noqa: INP001

from __future__ import annotations

import os
import sys
from pathlib import Path

import mkdocs_gen_files

src_path = Path(__file__).parent.parent.parent / "src"
sys.path.append(src_path.as_posix())

os.environ["SERVICE_NAME"] = ""
os.environ["TABLE_NAME"] = ""

from index import app  # noqa: E402

openapi = app.get_openapi_json_schema(openapi_version="3.1.0")

with mkdocs_gen_files.open("api/openapi.json", "w") as f:
    f.write(openapi)
