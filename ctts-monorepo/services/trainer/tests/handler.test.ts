import { get } from '../src/handler';

jest.mock('@aws-sdk/client-rds-data', () => {
  return {
    RDSDataClient: jest.fn().mockImplementation(() => ({
      send: mockSend,
    })),
    ExecuteStatementCommand: class {},
  };
});

const mockSend = jest.fn();

process.env.CLUSTER_ARN = 'arn:cluster';
process.env.SECRET_ARN = 'arn:secret';
process.env.DB_NAME = 'ctts';

describe('get trainers', () => {
  it('returns fallback trainers when table empty', async () => {
    mockSend.mockResolvedValue({ records: [] });
    const res = await get();
    expect(JSON.parse(res.body)).toHaveLength(2);
  });
});
