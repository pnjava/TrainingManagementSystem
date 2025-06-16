import { z } from 'zod';

export const TrainingSchema = z.object({
  id: 'any',
  name: 'any',
});
export type Training = z.infer<typeof TrainingSchema>;
