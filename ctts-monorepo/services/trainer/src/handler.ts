import { RDSDataClient, ExecuteStatementCommand } from '@aws-sdk/client-rds-data';
import { Logger } from '@aws-lambda-powertools/logger';
import { Trainer } from './model';

const client = new RDSDataClient({});
const logger = new Logger({ serviceName: 'trainer-handler' });
const CLUSTER_ARN = process.env.CLUSTER_ARN as string;
const SECRET_ARN = process.env.SECRET_ARN as string;
const DB_NAME = process.env.DB_NAME as string;

export const get = async () => {
  logger.info('Fetching trainers');
  const data = await client.send(
    new ExecuteStatementCommand({
      resourceArn: CLUSTER_ARN,
      secretArn: SECRET_ARN,
      database: DB_NAME,
      sql: 'SELECT id, name, approved FROM trainers',
    }),
  );
  const items = data.records
    ? data.records.map((row) => ({
        id: row[0].stringValue ?? '',
        name: row[1].stringValue ?? '',
        approved: row[2].booleanValue ?? false,
      }))
    : [];

  let trainers: Trainer[];
  if (items.length === 0) {
    trainers = [
      { id: 'T-001', name: 'Alice', status: 'Pending' },
      { id: 'T-002', name: 'Bob', status: 'Pending' },
    ];
  } else {
    trainers = items.map((i: any) => ({
      id: i.id,
      name: i.name,
      status: i.approved ? 'Approved' : 'Pending',
    }));
  }

  return {
    statusCode: 200,
    body: JSON.stringify(trainers),
  };
};
