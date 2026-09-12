"use server";

import { api } from "@/lib/axios";
import z from "zod";

const SIGNIN_URL = "/auth/signin";

export async function signin({ email, password }: signInParams) {
  return api.post<z.infer<typeof >(SIGNIN_URL, {
    email: email,
    password: password,
  });
}
