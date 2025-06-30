import { DynamoDBClient, ScanCommand, PutItemCommand } from '@aws-sdk/client-dynamodb';

const TABLE = process.env.TABLE;
if (!TABLE) {
  console.error('TABLE env var required');
  process.exit(1);
}

const client = new DynamoDBClient({ region: 'us-east-1' });

(async () => {
  const data = await client.send(new ScanCommand({ TableName: TABLE }));
  if (!data.Items || data.Items.length === 0) {
    await client.send(
      new PutItemCommand({
        TableName: TABLE,
        Item: { pk: { S: 'T-001' }, name: { S: 'Alice' } },
      }),
    );
    await client.send(
      new PutItemCommand({
        TableName: TABLE,
        Item: { pk: { S: 'T-002' }, name: { S: 'Bob' } },
      }),
    );
    console.log('Seeded');
  } else {
    console.log('Table already has data');
  }
})();
