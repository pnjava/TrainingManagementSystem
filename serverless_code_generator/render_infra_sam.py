from pathlib import Path
from .build_meta_model import DataClassModel


def render_infra_sam(model: DataClassModel, output: Path, templates: Path):
    lines = [
        "AWSTemplateFormatVersion: '2010-09-09'",
        'Transform: AWS::Serverless-2016-10-31',
        'Resources:'
    ]
    for table in model.tables:
        lines.append(f"  {table.name.capitalize()}Function:")
        lines.append('    Type: AWS::Serverless::Function')
        lines.append('    Properties:')
        lines.append(f"      Handler: services/{table.name}/handler.create")
        lines.append('      Runtime: nodejs20.x')
    with open(output / 'template.yaml', 'w') as f:
        f.write('\n'.join(lines))
