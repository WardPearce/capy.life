<script lang="ts">
  import CapybaraCard from "../components/CapybaraCard.svelte";
</script>

<main>
  <h2 style="margin-bottom: 0.5em; margin-top: 1em;">Submit a capybara</h2>
  <CapybaraCard editable={true} />
</main>

<style>
  :global(body) {
    overflow: auto;
  }
</style>
