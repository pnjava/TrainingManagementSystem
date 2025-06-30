import { APIGatewayProxyEvent } from 'aws-lambda';
import { DynamoDBClient, PutItemCommand } from '@aws-sdk/client-dynamodb';
import { Logger } from '@aws-lambda-powertools/logger';

const client = new DynamoDBClient({});
const logger = new Logger({ serviceName: 'approve-trainer' });
const TABLE = process.env.TABLE as string;

export const handler = async (event: APIGatewayProxyEvent) => {
  const id = event.pathParameters?.id || '';
  if (!/^T-\d{3}$/.test(id)) {
    return { statusCode: 400, body: 'Invalid id' };
  }
  const now = new Date().toISOString();
  await client.send(
    new PutItemCommand({
      TableName: TABLE,
      Item: {
        pk: { S: id },
        approved: { BOOL: true },
        approvedAt: { S: now },
      },
    }),
  );
  return {
    statusCode: 200,
    body: JSON.stringify({ id, approved: true }),
  };
};
