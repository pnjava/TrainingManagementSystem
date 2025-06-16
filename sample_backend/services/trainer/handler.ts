// trainer/handler.ts (generated)
import { db } from '@prs/core/db';
import { buildResponse } from '@prs/core/http';
import { TrainerSchema } from './model';
import * as custom from './custom';

export const create = async (event) => {
  const body = JSON.parse(event.body);
  const data = TrainerSchema.parse(body);
  const [id] = await db('trainer').insert(data).returning('id');
  if (custom.afterCreate) await custom.afterCreate(id, data);
  return buildResponse(201, { id });
};
