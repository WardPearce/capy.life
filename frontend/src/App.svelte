<script lang="ts">
  import CapybaraCard from "./lib/CapybaraCard.svelte";
  import Carousel from "svelte-carousel";
  import { CapyAPi } from "./lib/capy";
  import type { CapybaraModel } from "./lib/client";

  let submitCapy = false;

  let capybaras: Array<CapybaraModel | null> = [null];
  let daysAgo = 0;

  async function handleNewCapy(event) {
    capybaras[event.detail] = await CapyAPi.default.getTodayCapybara(
      (daysAgo = 0)
    );
    daysAgo++;
  }
</script>

<nav>
  <h1 on:click={() => (submitCapy = false)} on:keydown={() => {}}>capy.life</h1>
  <p>the official daily capybara website</p>
</nav>

<main>
  {#if !submitCapy}
    <Carousel
      dots={false}
      infinite={false}
      autoplay={false}
      on:pageChange={(e) => handleNewCapy(e)}
    >
      {#each capybaras as capy}
        {#if !capy}
          <div style="text-align: center;width:100%;">
            <h3>Problem loading today's capybara</h3>
            <p>
              Maybe our API is down or we're out of capybaras. Come back later.
            </p>
          </div>
        {:else}
          <div class="capybara-display">
            <h3 style="margin-bottom: .5em;">
              {#if new Date(capy.used).toLocaleDateString() == new Date().toLocaleDateString()}
                Today's capybara
              {:else}
                {new Date(capy.used).toLocaleDateString("en-US", {
                  weekday: "long",
                  year: "numeric",
                  month: "long",
                  day: "numeric",
                })}
              {/if}
            </h3>

            <CapybaraCard
              editable={false}
              imgSrc={capy.image}
              name={capy.name}
              fighterClass={capy.class_}
              muncherLvl={capy.muncher_lvl}
              relationship_status={capy.relationship_status}
              weaponOfChoice={capy.weapon}
            />
          </div>
        {/if}
      {/each}
    </Carousel>
  {:else}
    <h3 style="margin-bottom: .5em;">Submit a capybara</h3>
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
