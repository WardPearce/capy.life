import { persisted } from "svelte-local-storage-store";

export const loggedIn = persisted(
    "loggedIn", { username: "", isRoot: false }
)
