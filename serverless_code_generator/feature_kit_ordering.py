from pathlib import Path

def feature_kit_ordering(output: Path):
    feature_dir = output / 'feature' / 'kit_ordering'
    feature_dir.mkdir(parents=True, exist_ok=True)
    (feature_dir / 'README.md').write_text('# Kit Ordering')
