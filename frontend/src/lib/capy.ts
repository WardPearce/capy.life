import { CapyClient } from "./client";

export const CapyAPi = new CapyClient(
    {
        BASE: import.meta.env.VITE_API_ENDPOINT,
        WITH_CREDENTIALS: true,
        CREDENTIALS: "include"
    }
);
