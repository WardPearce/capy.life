<script lang="ts">
  import { SyncLoader } from "svelte-loading-spinners";
  import { navigate } from "svelte-navigator";

  import { onMount } from "svelte";
  import { CapyAPi } from "../lib/capy";
  import { timeout } from "../lib/timeout";
  import { loggedIn } from "../store";

  onMount(async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get("code");
    if (!code) navigate("/", { replace: true });
    else {
      try {
        const admin = await CapyAPi.admin.adminAuthAuth(code);
        loggedIn.set({
          username: admin.username,
          isRoot: admin.is_root ? true : false,
        });
        // Wait a second before redirecting.
        await timeout(1000);
        navigate("/admin", { replace: true });
      } catch {
        navigate("/", { replace: true });
      }
    }
  });
</script>

<main>
  <SyncLoader color="var(--capyLight)" size={100} />
  <h2>Loading account...</h2>
</main>

<style>
  main {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 2em;
  }
</style>
