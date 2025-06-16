from pathlib import Path
from .build_meta_model import DataClassModel


HANDLER_TEMPLATE = """// {table}/handler.ts (generated)
import {{ db }} from '@prs/core/db';
import {{ buildResponse }} from '@prs/core/http';
import {{ {Table}Schema }} from './model';
import * as custom from './custom';

export const create = async (event) => {{
  const body = JSON.parse(event.body);
  const data = {Table}Schema.parse(body);
  const [id] = await db('{table}').insert(data).returning('id');
  if (custom.afterCreate) await custom.afterCreate(id, data);
  return buildResponse(201, {{ id }});
}};
"""

CUSTOM_TEMPLATE = "// custom.ts - user overrides\n"


def render_crud_templates(model: DataClassModel, output: Path):
    for table in model.tables:
        service_dir = output / 'services' / table.name
        service_dir.mkdir(parents=True, exist_ok=True)
        content = HANDLER_TEMPLATE.format(table=table.name, Table=table.name.capitalize(), db='db', buildResponse='buildResponse')
        with open(service_dir / 'handler.ts', 'w') as f:
            f.write(content)
        custom = service_dir / 'custom.ts'
        if not custom.exists():
            with open(custom, 'w') as f:
                f.write(CUSTOM_TEMPLATE)
