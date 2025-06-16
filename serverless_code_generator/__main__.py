import click
from pathlib import Path

from .load_schema import load_schema
from .validate_schema import validate_schema
from .build_meta_model import build_meta_model
from .render_crud_templates import render_crud_templates
from .render_openapi import render_openapi
from .render_models import render_models
from .render_infra_sam import render_infra_sam
from .render_infra_cdk import render_infra_cdk
from .render_ci_github import render_ci_github
from .copy_shared_runtime import copy_shared_runtime
from .generate_readme import generate_readme
from .generate_tests import generate_tests
from .feature_approval_workflow import feature_approval_workflow
from .feature_certificate_issuer import feature_certificate_issuer
from .feature_kit_ordering import feature_kit_ordering
from .feature_evaluation_form import feature_evaluation_form

TEMPLATES = Path(__file__).parent / 'templates'
RUNTIME = Path(__file__).parent / 'runtime'

FEATURE_MAP = {
    'approval_workflow': feature_approval_workflow,
    'certificate_issuer': feature_certificate_issuer,
    'kit_ordering': feature_kit_ordering,
    'evaluation_form': feature_evaluation_form,
}

@click.command()
@click.option('--db-url', default=None)
@click.option('--schema-file', default=None)
@click.option('--dialect', type=click.Choice(['postgres', 'mysql']), default='postgres')
@click.option('--output', required=True, type=click.Path())
@click.option('--project-name', required=True)
@click.option('--features', default='')
@click.option('--cdk', is_flag=True, default=False)
def main(db_url, schema_file, dialect, output, project_name, features, cdk):
    output_path = Path(output)
    model = load_schema(db_url=db_url, schema_file=schema_file)
    validate_schema(model)
    dmodel = build_meta_model(model)
    render_crud_templates(dmodel, output_path)
    render_models(dmodel, output_path, TEMPLATES)
    render_openapi(dmodel, output_path, TEMPLATES)
    render_infra_sam(dmodel, output_path, TEMPLATES)
    render_ci_github(dmodel, output_path, TEMPLATES)
    generate_tests(dmodel, output_path, TEMPLATES)
    generate_readme(dmodel, output_path, TEMPLATES)
    copy_shared_runtime(output_path, RUNTIME)
    if cdk:
        render_infra_cdk(dmodel, output_path, TEMPLATES)
    for feature in [f.strip() for f in features.split(',') if f.strip()]:
        func = FEATURE_MAP.get(feature)
        if func:
            func(output_path)
    print('Generated project at ' + output)

if __name__ == '__main__':
    main()
