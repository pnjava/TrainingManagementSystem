import { APIGatewayProxyEvent } from 'aws-lambda';
import { RDSDataClient, ExecuteStatementCommand } from '@aws-sdk/client-rds-data';
import { Logger } from '@aws-lambda-powertools/logger';

const client = new RDSDataClient({});
const logger = new Logger({ serviceName: 'approve-trainer' });
const CLUSTER_ARN = process.env.CLUSTER_ARN as string;
const SECRET_ARN = process.env.SECRET_ARN as string;
const DB_NAME = process.env.DB_NAME as string;

export const handler = async (event: APIGatewayProxyEvent) => {
  const id = event.pathParameters?.id || '';
  if (!/^T-\d{3}$/.test(id)) {
    return { statusCode: 400, body: 'Invalid id' };
  }
  const now = new Date().toISOString();
  await client.send(
    new ExecuteStatementCommand({
      resourceArn: CLUSTER_ARN,
      secretArn: SECRET_ARN,
      database: DB_NAME,
      sql: 'UPDATE trainers SET approved=true, approved_at=:ts WHERE id=:id',
      parameters: [
        { name: 'ts', value: { stringValue: now } },
        { name: 'id', value: { stringValue: id } },
      ],
    }),
  );
  return {
    statusCode: 200,
    body: JSON.stringify({ id, approved: true }),
  };
};
