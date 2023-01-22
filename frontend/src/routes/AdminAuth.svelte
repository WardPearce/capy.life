<script lang="ts">
  import { navigate } from "svelte-navigator";
  import { onMount } from "svelte";
  import { CapyAPi } from "../lib/capy";
  import { loggedIn } from "../store";

  onMount(async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get("code");
    if (!code) navigate("/", { replace: true });
    else {
      try {
        const admin = await CapyAPi.default.discordAuthDiscordAuth(code);
        loggedIn.set({
          username: admin.username,
          isRoot: admin.is_root,
        });
        navigate("/admin", { replace: true });
      } catch {
        navigate("/", { replace: true });
      }
    }
  });
</script>
