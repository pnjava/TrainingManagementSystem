from pathlib import Path

def feature_certificate_issuer(output: Path):
    feature_dir = output / 'feature' / 'certificate_issuer'
    feature_dir.mkdir(parents=True, exist_ok=True)
    (feature_dir / 'README.md').write_text('# Certificate Issuer')
