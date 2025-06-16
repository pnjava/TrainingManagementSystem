from .utils import MetaModel, Table, Column
import re


def load_schema(db_url: str = None, schema_file: str = None) -> MetaModel:
    tables = []
    if db_url:
        from sqlalchemy import create_engine, inspect
        engine = create_engine(db_url)
        inspector = inspect(engine)
        for table_name in inspector.get_table_names():
            cols = []
            pk = None
            for col in inspector.get_columns(table_name):
                cols.append(Column(col['name'], str(col['type']), col.get('nullable', True)))
            pk_cols = inspector.get_pk_constraint(table_name).get('constrained_columns')
            if pk_cols:
                pk = pk_cols[0]
            tables.append(Table(table_name, cols, pk))
    elif schema_file:
        with open(schema_file) as f:
            sql = f.read()
        pattern = re.compile(r'CREATE TABLE (\w+)\s*\((.*?)\);', re.S | re.I)
        for match in pattern.finditer(sql):
            name = match.group(1)
            body = match.group(2)
            cols = []
            pk = None
            for line in body.split(','):
                parts = line.strip().split()
                if len(parts) < 2:
                    continue
                col_name = parts[0].strip('"')
                col_type = parts[1]
                nullable = 'NOT NULL' not in line.upper()
                if 'PRIMARY KEY' in line.upper():
                    pk = col_name
                cols.append(Column(col_name, col_type, nullable))
            tables.append(Table(name, cols, pk))
    else:
        raise ValueError('Either db_url or schema_file is required')
    return MetaModel(tables)
