from pathlib import Path
from .build_meta_model import DataClassModel


def render_openapi(model: DataClassModel, output: Path, templates: Path):
    lines = ["openapi: 3.1.0", "info:", "  title: API", "  version: 1.0.0", "paths:"]
    for table in model.tables:
        lines.append(f"  /{table.name}s:")
        lines.append("    post:")
        lines.append(f"      summary: create {table.name}")
        lines.append("      responses:")
        lines.append("        '201':")
        lines.append("          description: Created")
    with open(output / 'openapi.yaml', 'w') as f:
        f.write('\n'.join(lines))
