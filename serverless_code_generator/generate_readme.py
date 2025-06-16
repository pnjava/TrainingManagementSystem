from pathlib import Path
from .build_meta_model import DataClassModel


def generate_readme(model: DataClassModel, output: Path, templates: Path):
    content = f"# {len(model.tables)} Entities API\n\nGenerated project.\n"
    with open(output / 'README.md', 'w') as f:
        f.write(content)
