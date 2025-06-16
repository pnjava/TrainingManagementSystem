from pathlib import Path

def feature_evaluation_form(output: Path):
    feature_dir = output / 'feature' / 'evaluation_form'
    feature_dir.mkdir(parents=True, exist_ok=True)
    (feature_dir / 'README.md').write_text('# Evaluation Form')
