import re
from .utils import MetaModel


def validate_schema(model: MetaModel) -> None:
    errors = []
    snake = re.compile(r'^[a-z0-9_]+$')
    for table in model.tables:
        if not table.primary_key:
            errors.append(f'Table {table.name} missing primary key')
        if not snake.match(table.name):
            errors.append(f'Table {table.name} not snake_case')
        for col in table.columns:
            if not snake.match(col.name):
                errors.append(f'Column {table.name}.{col.name} not snake_case')
    if errors:
        msg = '\n'.join(errors)
        raise ValueError('Schema validation failed:\n' + msg)
