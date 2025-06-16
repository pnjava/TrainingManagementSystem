from pathlib import Path

def feature_approval_workflow(output: Path):
    feature_dir = output / 'feature' / 'approval_workflow'
    feature_dir.mkdir(parents=True, exist_ok=True)
    (feature_dir / 'README.md').write_text('# Approval Workflow')
