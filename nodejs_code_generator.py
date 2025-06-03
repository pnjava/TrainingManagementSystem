import json
import os
import textwrap

PROJECT_STRUCTURE = {
    'config': [],
    'src': ['models', 'controllers', 'routes', 'services'],
}

PACKAGE_JSON = '''{
  "name": "generated-microservice",
  "version": "1.0.0",
  "main": "app.js",
  "scripts": {
    "start": "node app.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "sequelize": "^6.37.0",
    "pg": "^8.11.1"
  }
}'''

APP_JS_HEADER = '''const express = require('express');
const app = express();
app.use(express.json());

const db = require('./config/database');

db.authenticate()
  .then(() => console.log('Database connected'))
  .catch(err => console.error('DB connection error:', err));
'''

APP_JS_FOOTER = '''const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
'''

DATABASE_JS = '''const { Sequelize } = require('sequelize');
require('dotenv').config();

const sequelize = new Sequelize(process.env.DB_NAME, process.env.DB_USER, process.env.DB_PASSWORD, {
  host: process.env.DB_HOST,
  dialect: 'postgres'
});

module.exports = sequelize;
'''

ENV_CONTENT = 'DB_NAME=yourdbname\nDB_USER=youruser\nDB_PASSWORD=yourpassword\nDB_HOST=localhost\nPORT=3000\n'

DOCKERFILE_CONTENT = '''FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
CMD ["npm", "start"]
'''

README_TEMPLATE = '''# Generated Node.js Microservice

This project was generated automatically.\n
## Setup

```bash
npm install
npm start
```

Ensure you have a PostgreSQL database configured using the `.env` file.
'''

def camel_case(name: str) -> str:
    return name[0].upper() + name[1:]

def generate_model(entity):
    """Return Sequelize model definition for an entity."""
    name = camel_case(entity['name'])
    fields = []
    for field in entity.get('fields', []):
        line = f"  {field['name']}: {{ type: Sequelize.{field['type'].upper()}"
        if field.get('primary'):
            line += ", primaryKey: true"
        line += " }"
        fields.append(line)
    fields_str = ',\n'.join(fields)
    return (
        "const Sequelize = require('sequelize');\n"
        "const sequelize = require('../../config/database');\n\n"
        f"const {name} = sequelize.define('{entity['name']}', {{\n"
        f"{fields_str}\n}});\n\n"
        f"module.exports = {name};\n"
    )

def generate_controller(entity):
    functions = []
    name = camel_case(entity['name'])
    lower = entity['name'].lower()
    if 'create' in entity.get('operations', []):
        functions.append(textwrap.dedent(f"""\nexports.create{ name } = async (req, res) => {{
  try {{
    const item = await { name }.create(req.body);
    res.status(201).json(item);
  }} catch (err) {{
    res.status(500).json({{ error: err.message }});
  }}
}};"""))
    if 'read' in entity.get('operations', []):
        functions.append(textwrap.dedent(f"""\nexports.getAll{ name }s = async (req, res) => {{
  try {{
    const items = await { name }.findAll();
    res.json(items);
  }} catch (err) {{
    res.status(500).json({{ error: err.message }});
  }}
}};\n
exports.get{ name }ById = async (req, res) => {{
  try {{
    const item = await { name }.findByPk(req.params.id);
    if (!item) return res.status(404).json({{}});
    res.json(item);
  }} catch (err) {{
    res.status(500).json({{ error: err.message }});
  }}
}};"""))
    if 'update' in entity.get('operations', []):
        functions.append(textwrap.dedent(f"""\nexports.update{ name } = async (req, res) => {{
  try {{
    const [updated] = await { name }.update(req.body, {{ where: {{ id: req.params.id }} }});
    if (!updated) return res.status(404).json({{}});
    const item = await { name }.findByPk(req.params.id);
    res.json(item);
  }} catch (err) {{
    res.status(500).json({{ error: err.message }});
  }}
}};"""))
    if 'delete' in entity.get('operations', []):
        functions.append(textwrap.dedent(f"""\nexports.delete{ name } = async (req, res) => {{
  try {{
    const deleted = await { name }.destroy({{ where: {{ id: req.params.id }} }});
    if (!deleted) return res.status(404).json({{}});
    res.status(204).end();
  }} catch (err) {{
    res.status(500).json({{ error: err.message }});
  }}
}};"""))
    return f"const {{ { name } }} = require('../models/{ name }');\n" + '\n'.join(functions) + '\n'

def generate_routes(entity):
    name = camel_case(entity['name'])
    lower = entity['name'].lower()
    lines = ["const express = require('express');", "const router = express.Router();", f"const controller = require('../controllers/{ name }Controller');", ""]
    if 'create' in entity.get('operations', []):
        lines.append(f"router.post('/', controller.create{ name });")
    if 'read' in entity.get('operations', []):
        lines.append(f"router.get('/', controller.getAll{ name }s);")
        lines.append(f"router.get('/:id', controller.get{ name }ById);")
    if 'update' in entity.get('operations', []):
        lines.append(f"router.put('/:id', controller.update{ name });")
    if 'delete' in entity.get('operations', []):
        lines.append(f"router.delete('/:id', controller.delete{ name });")
    lines.append("module.exports = router;")
    return '\n'.join(lines)

def ensure_structure(base_path):
    for folder, subfolders in PROJECT_STRUCTURE.items():
        path = os.path.join(base_path, folder)
        os.makedirs(path, exist_ok=True)
        for sub in subfolders:
            os.makedirs(os.path.join(path, sub), exist_ok=True)

def generate_project(data, output_path):
    ensure_structure(output_path)

    with open(os.path.join(output_path, 'package.json'), 'w') as f:
        f.write(PACKAGE_JSON)
    with open(os.path.join(output_path, '.env'), 'w') as f:
        f.write(ENV_CONTENT)
    with open(os.path.join(output_path, 'Dockerfile'), 'w') as f:
        f.write(DOCKERFILE_CONTENT)
    with open(os.path.join(output_path, 'README.md'), 'w') as f:
        f.write(README_TEMPLATE)
    with open(os.path.join(output_path, 'config', 'database.js'), 'w') as f:
        f.write(DATABASE_JS)

    app_routes = []
    for entity in data.get('entities', []):
        name = camel_case(entity['name'])
        model_path = os.path.join(output_path, 'src', 'models', f'{ name }.js')
        with open(model_path, 'w') as f:
            f.write(generate_model(entity))
        controller_path = os.path.join(output_path, 'src', 'controllers', f'{ name }Controller.js')
        with open(controller_path, 'w') as f:
            f.write(generate_controller(entity))
        routes_path = os.path.join(output_path, 'src', 'routes', f'{ name }Routes.js')
        with open(routes_path, 'w') as f:
            f.write(generate_routes(entity))
        service_path = os.path.join(output_path, 'src', 'services', f'{ name }Service.js')
        with open(service_path, 'w') as f:
            f.write(f"// Business logic for { name } goes here\n")
        app_routes.append(f"app.use('/{entity['name'].lower()}', require('./src/routes/{ name }Routes'));")

    with open(os.path.join(output_path, 'app.js'), 'w') as f:
        f.write(APP_JS_HEADER)
        f.write('\n'.join(app_routes))
        f.write('\n\n')
        f.write(APP_JS_FOOTER)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Generate Node.js microservice scaffold.')
    parser.add_argument('model', help='Path to JSON data model file')
    parser.add_argument('output', help='Directory to output generated project')
    args = parser.parse_args()

    with open(args.model) as f:
        data = json.load(f)
    generate_project(data, args.output)
    print(f"Project generated in {args.output}")

if __name__ == '__main__':
    main()
