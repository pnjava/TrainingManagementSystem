import { RDSDataClient, ExecuteStatementCommand } from '@aws-sdk/client-rds-data';

const CLUSTER_ARN = process.env.CLUSTER_ARN;
const SECRET_ARN = process.env.SECRET_ARN;
const DB_NAME = process.env.DB_NAME || 'ctts';
if (!CLUSTER_ARN || !SECRET_ARN) {
  console.error('CLUSTER_ARN and SECRET_ARN env vars required');
  process.exit(1);
}

const client = new RDSDataClient({ region: 'us-east-1' });

(async () => {
  await client.send(
    new ExecuteStatementCommand({
      resourceArn: CLUSTER_ARN!,
      secretArn: SECRET_ARN!,
      database: DB_NAME,
      sql:
        'CREATE TABLE IF NOT EXISTS trainers (id varchar primary key, name text, approved boolean default false, approved_at timestamp)',
    }),
  );

  const countRes = await client.send(
    new ExecuteStatementCommand({
      resourceArn: CLUSTER_ARN!,
      secretArn: SECRET_ARN!,
      database: DB_NAME,
      sql: 'SELECT COUNT(*) FROM trainers',
    }),
  );
  const count = parseInt(countRes.records?.[0]?.[0]?.longValue ?? '0');

  if (count === 0) {
    await client.send(
      new ExecuteStatementCommand({
        resourceArn: CLUSTER_ARN!,
        secretArn: SECRET_ARN!,
        database: DB_NAME,
        sql: "INSERT INTO trainers(id, name) VALUES('T-001','Alice'),('T-002','Bob')",
      }),
    );
    console.log('Seeded');
  } else {
    console.log('Table already has data');
  }
})();
