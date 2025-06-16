from pathlib import Path
from .build_meta_model import DataClassModel


def render_ci_github(model: DataClassModel, output: Path, templates: Path):
    wf_dir = output / '.github' / 'workflows'
    wf_dir.mkdir(parents=True, exist_ok=True)
    content = (
        "name: Deploy\n"
        "on:\n  push:\n    branches: [main]\n\n"
        "jobs:\n  build:\n    runs-on: ubuntu-latest\n    steps:\n"
        "      - uses: actions/checkout@v2\n"
        "      - uses: actions/setup-node@v3\n        with:\n          node-version: 20\n"
        "      - run: npm ci\n      - run: sam build --use-container\n      - run: sam deploy --no-confirm-changeset --stack-name dev\n"
    )
    with open(wf_dir / 'deploy.yml', 'w') as f:
        f.write(content)
