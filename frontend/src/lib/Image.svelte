<script lang="ts">
  import { onMount } from "svelte";
  import { SyncLoader } from "svelte-loading-spinners";
  export let src;
  export let alt = "Document";

  let loaded = false;
  let failed = false;
  let loading = false;

  onMount(() => {
    const img = new Image();
    img.src = src;
    loading = true;

    img.onload = () => {
      loading = false;
      loaded = true;
    };
    img.onerror = () => {
      loading = false;
      failed = true;
    };
  });
</script>

{#if loaded}
  <img {src} {alt} />
{:else if failed}
  <h3>Can't load Capybara, API might be down.</h3>
{:else if loading}
  <SyncLoader color="var(--capyLight)" size={50} />
  <h3>Downloading Capybara.</h3>
{/if}
