import z from "zod";

export const response = z.object({
  status: z.boolean(),
  data: z.any(),
  message: z.string(),
});
