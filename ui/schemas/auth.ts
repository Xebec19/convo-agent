import z from "zod";

export const SigninResponseSchema = z.object({
  id: z.number().transform((input) => String(input)),
  name: z.string(),
  email: z.email(),
  image: z.string().default(""),
});
