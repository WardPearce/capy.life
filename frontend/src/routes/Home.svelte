<script lang="ts">
  import { onMount } from "svelte";

  import CapybaraCard from "../components/CapybaraCard.svelte";
  import PageLoading from "../components/PageLoading.svelte";
  import { CapyAPi } from "../lib/capy";
  import type { CapybaraModel } from "../lib/client";

  let capybaras: Array<CapybaraModel | null> = [];
  let daysAgo = 0;
  let loading = false;

  async function loadMore() {
    if (loading) return;

    loading = true;

    try {
      const capybara = await CapyAPi.default.getTodayCapybara(daysAgo);
      capybaras = [...capybaras, capybara];
      loading = false;
    } catch (error) {
      capybaras = [...capybaras, null];
      loading = false;
    }

    daysAgo++;
  }

  onMount(async () => {
    await loadMore();
  });
</script>

<main>
  {#each capybaras as capy}
    {#if !capy}
      <div class="unable-to-load">
        <h3>Problem loading this capybara</h3>
        <p>Maybe our API is down or we're out of capybaras. Come back later.</p>
      </div>
    {:else}
      <div class="capybara-display">
        <h3 style="margin-bottom: .5em;margin-top:1em;">
          {#if capy.days_ago == 0}
            Today's capybara
          {:else if capy.days_ago < 25}
            Capybara from {capy.days_ago}
            {capy.days_ago > 1 ? "days" : "day"} ago
          {:else}
            Capybara from {new Date(capy.used.toString()).toLocaleDateString(
              "en-US",
              {
                year: "numeric",
                month: "short",
                day: "numeric",
              }
            )}
          {/if}
        </h3>

        <div id={capy._id} />

        <CapybaraCard
          editable={false}
          imgSrc={capy.image}
          name={capy.name}
          fighterClass={capy.class}
          muncherLvl={capy.muncher_lvl}
          relationship_status={capy.relationship_status}
          weaponOfChoice={capy.weapon}
        />
      </div>
    {/if}
  {/each}

  {#if loading}
    <div class="loading"><PageLoading /></div>
  {:else}
    <button class="button" style="margin-bottom: 5em;" on:click={loadMore}
      >Load more</button
    >
  {/if}
</main>

<style>
  .capybara-display {
    margin-bottom: 1em;
  }

  .unable-to-load {
    text-align: center;
    margin-top: 5em;
    width: 100%;
  }
</style>
