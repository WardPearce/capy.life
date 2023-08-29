<script lang="ts">
  import { SyncLoader } from "svelte-loading-spinners";
</script>

<main>
  <SyncLoader color="var(--capyLight)" size={100} />
</main>

<style>
  main {
    margin-top: 0;
    display: flex;
    align-items: center;
    flex-direction: column;
    text-align: center;
  }
</style>
