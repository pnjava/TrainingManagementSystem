import shutil
from pathlib import Path


def copy_shared_runtime(output: Path, runtime_dir: Path):
    dest = output / 'services' / '_shared'
    dest.mkdir(parents=True, exist_ok=True)
    for file in runtime_dir.glob('*.ts'):
        shutil.copy(file, dest / file.name)
