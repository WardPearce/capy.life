<script lang="ts">
  import CapybaraCard from "./lib/CapybaraCard.svelte";
  import Carousel from "svelte-carousel";

  let submitCapy = false;
</script>

<nav>
  <h1 on:click={() => (submitCapy = false)} on:keydown={() => {}}>capy.life</h1>
  <p>the official daily capybara website</p>
</nav>

<main>
  {#if !submitCapy}
    <Carousel dots={false} infinite={false} autoplay={false}>
      <div class="capybara-display">
        {#if !submitCapy}
          <h3 style="margin-bottom: .5em;">Capybara of the day</h3>
        {/if}

        <CapybaraCard
          editable={false}
          imgSrc="https://capy.life/api/capy/9ZhXTT7iE8eiYIzR-OEYa"
        />
      </div>
    </Carousel>
  {:else}
    <CapybaraCard editable={true} />
  {/if}

  {#if !submitCapy}
    <button
      class="button-large"
      style="margin-top: 1em;"
      on:click={() => (submitCapy = !submitCapy)}>Submit a Capybara!</button
    >
  {:else}
    <button style="margin-top: 1em;" on:click={() => (submitCapy = false)}
      >Back</button
    >
  {/if}
</main>
