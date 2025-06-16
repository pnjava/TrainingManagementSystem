from pathlib import Path
from .build_meta_model import DataClassModel


def render_infra_cdk(model: DataClassModel, output: Path, templates: Path):
    cdk_dir = output / 'cdk'
    cdk_dir.mkdir(parents=True, exist_ok=True)
    with open(cdk_dir / 'cdk.ts', 'w') as f:
        f.write('export class AppStack {}\n')
