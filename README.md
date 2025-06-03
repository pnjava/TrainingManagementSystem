# Node.js Microservice Code Generator

This repository contains a simple Python script that generates a Node.js
microservice scaffold based on a JSON data model. It creates Sequelize
models, Express controllers, routes, and basic project files.

## Usage

1. Prepare a JSON model file describing your entities. See
   `sample_model.json` for an example format.
2. Run the generator and specify an output directory:

```bash
python nodejs_code_generator.py sample_model.json output_project
```

3. Install dependencies and start the generated service:

```bash
cd output_project
npm install
npm start
```

The generated project includes a `.env` file template for PostgreSQL
configuration and a `Dockerfile` for container builds.
