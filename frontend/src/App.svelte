<script lang="ts">
  import CapybaraCard from "./lib/CapybaraCard.svelte";

  let submitCapy = false;
</script>

<nav>
  <h1 on:click={() => (submitCapy = false)} on:keydown={() => {}}>capy.life</h1>
</nav>

<main>
  <CapybaraCard
    editable={submitCapy}
    imgSrc="https://capy.life/api/capy/Ta1PpP3ao0QBGyv3-W6lm"
  />

  {#if !submitCapy}
    <button
      class="button-large"
      style="margin-top: 2em;"
      on:click={() => (submitCapy = !submitCapy)}>Submit a Capybara!</button
    >
  {:else}
    <button style="margin-top: 2em;" on:click={() => (submitCapy = false)}
      >Back</button
    >
  {/if}
</main>
