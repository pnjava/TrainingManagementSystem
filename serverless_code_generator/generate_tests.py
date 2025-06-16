from pathlib import Path
from .build_meta_model import DataClassModel


def generate_tests(model: DataClassModel, output: Path, templates: Path):
    content = (
        "import { create } from '../handler';\n"
        "test('create', async () => {\n"
        "  const event = { body: '{}' } as any;\n"
        "  const res = await create(event);\n"
        "  expect(res.statusCode).toBe(201);\n"
        "});\n"
    )
    for table in model.tables:
        test_dir = output / 'services' / table.name / 'tests'
        test_dir.mkdir(parents=True, exist_ok=True)
        with open(test_dir / f'{table.name}.test.ts', 'w') as f:
            f.write(content)
