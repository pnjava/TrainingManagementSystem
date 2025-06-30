import { get } from '../src/handler';

jest.mock('@aws-sdk/client-dynamodb', () => {
  return {
    DynamoDBClient: jest.fn().mockImplementation(() => ({
      send: mockSend,
    })),
    ScanCommand: class {},
  };
});

const mockSend = jest.fn();

describe('get trainers', () => {
  it('returns fallback trainers when table empty', async () => {
    mockSend.mockResolvedValue({ Items: [] });
    const res = await get();
    expect(JSON.parse(res.body)).toHaveLength(2);
  });
});
