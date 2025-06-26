import { handler } from '../src/handler';

test('returns summary', async () => {
  const res = await handler();
  const body = JSON.parse(res.body);
  expect(body).toHaveProperty('totalTrainers');
});
