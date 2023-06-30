<script lang="ts">
  import { navigate } from "svelte-navigator";
  import { SyncLoader } from "svelte-loading-spinners";

  import { onMount } from "svelte";
  import { CapyAPi } from "../lib/capy";
  import { loggedIn } from "../store";

  function timeout(ms: number) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  onMount(async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get("code");
    if (!code) navigate("/", { replace: true });
    else {
      try {
        const admin = await CapyAPi.admin.adminAuthAuth(code);
        loggedIn.set({
          username: admin.username,
          isRoot: admin.is_root,
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
