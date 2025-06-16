from pathlib import Path
from .build_meta_model import DataClassModel


def render_models(model: DataClassModel, output: Path, templates: Path):
    for table in model.tables:
        service_dir = output / 'services' / table.name
        sql_dir = service_dir / 'sql'
        sql_dir.mkdir(parents=True, exist_ok=True)
        fields = '\n'.join([f"  {c.name}: 'any'," for c in table.columns])
        model_content = f"import {{ z }} from 'zod';\n\nexport const {table.name.capitalize()}Schema = z.object({{\n{fields}\n}});\nexport type {table.name.capitalize()} = z.infer<typeof {table.name.capitalize()}Schema>;\n"
        with open(service_dir / 'model.ts', 'w') as f:
            f.write(model_content)
        col_lines = []
        for c in table.columns:
            line = f"  {c.name} {c.type}"
            if not c.nullable:
                line += ' NOT NULL'
            if c.name == table.primary_key:
                line += ' PRIMARY KEY'
            col_lines.append(line)
        sql_content = 'CREATE TABLE {name} (\n{cols}\n);\n'.format(
            name=table.name,
            cols=',\n'.join(col_lines)
        )
        with open(sql_dir / 'create_table.sql', 'w') as f:
            f.write(sql_content)
