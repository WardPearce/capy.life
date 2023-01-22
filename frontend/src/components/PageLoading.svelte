<script lang="ts">
  import { SyncLoader } from "svelte-loading-spinners";
</script>

<main>
  <SyncLoader color="var(--capyLight)" size={100} />
  <h3>this may take a moment</h3>
</main>

<style>
  main {
    margin-top: 0;
    display: flex;
    align-items: center;
    flex-direction: column;
    margin-top: 8em;
    text-align: center;
  }
  p {
    margin-top: 1em;
    font-weight: bold;
    text-transform: lowercase;
  }
  h3 {
    margin-top: 6em;
  }
</style>
