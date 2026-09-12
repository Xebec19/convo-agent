"use server";

import { api } from "@/lib/axios";
import { SigninResponseSchema } from "@/schemas/auth";
import { IResponse } from "@/schemas/response";
import z from "zod";

const SIGNIN_URL = "/auth/signin";

type signinParams = {
  email: string;
  password: string;
};

export async function signin({ email, password }: signinParams) {
  return api.post<IResponse<z.infer<typeof SigninResponseSchema>>>(SIGNIN_URL, {
    email: email,
    password: password,
  });
}
