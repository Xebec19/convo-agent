"use server";

import { api } from "@/lib/axios";

const SIGNIN_URL = "/auth/signin";

type signInParams = {
  email: string;
  password: string;
};

export async function signin({ email, password }: signInParams) {
  return api.post(SIGNIN_URL, {
    email: email,
    password: password,
  });
}
