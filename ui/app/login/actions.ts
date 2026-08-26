"use server";

import { signIn } from "@/auth";
import { AuthError } from "next-auth";
import z from "zod";
import { AuthSchema } from "./schema";

export async function authenticate(
  prevState: string | undefined,
  formData: z.infer<typeof AuthSchema>,
) {
  console.log({ values: formData });

  try {
    await signIn("credentials", formData);
  } catch (error) {
    if (error instanceof AuthError) {
      switch (error.type) {
        case "CredentialsSignin":
          return "Invalid credentials";
        default:
          return "Somethign went wrong";
      }
    }
    throw error;
  }
}
