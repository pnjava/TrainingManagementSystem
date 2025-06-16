import { z } from 'zod';

export const TrainerSchema = z.object({
  id: 'any',
  full_name: 'any',
});
export type Trainer = z.infer<typeof TrainerSchema>;
