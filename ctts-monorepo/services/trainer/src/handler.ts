import { DynamoDBClient, ScanCommand } from '@aws-sdk/client-dynamodb';
import { unmarshall } from '@aws-sdk/util-dynamodb';
import { Logger } from '@aws-lambda-powertools/logger';
import { Trainer } from './model';

const client = new DynamoDBClient({});
const logger = new Logger({ serviceName: 'trainer-handler' });
const TABLE = process.env.TABLE as string;

export const get = async () => {
  logger.info('Fetching trainers');
  const data = await client.send(new ScanCommand({ TableName: TABLE }));
  const items = data.Items ? data.Items.map((i) => unmarshall(i)) : [];

  let trainers: Trainer[];
  if (items.length === 0) {
    trainers = [
      { id: 'T-001', name: 'Alice', status: 'Pending' },
      { id: 'T-002', name: 'Bob', status: 'Pending' },
    ];
  } else {
    trainers = items.map((i: any) => ({
      id: i.pk,
      name: i.name,
      status: i.approved ? 'Approved' : 'Pending',
    }));
  }

  return {
    statusCode: 200,
    body: JSON.stringify(trainers),
  };
};
