import { create } from '../handler';
test('create', async () => {
  const event = { body: '{}' } as any;
  const res = await create(event);
  expect(res.statusCode).toBe(201);
});
