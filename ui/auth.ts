import NextAuth from "next-auth";
import { authConfig } from "./auth.config";
import Credentials from "next-auth/providers/credentials";
import { z } from "zod";
import { signin } from "./services/auth";

export const { auth, signIn, signOut } = NextAuth({
  ...authConfig,
  providers: [
    Credentials({
      async authorize(credentials) {
        try {
          const parsedCredentials = z
            .object({ email: z.email(), password: z.string().min(6) })
            .parse(credentials);

          const response = await signin({
            email: parsedCredentials.email,
            password: parsedCredentials.password,
          });
        } catch (err: unknown) {
          console.error(err);
          return null;
        }
      },
    }),
  ],
});
