<script lang="ts">
  import { onMount } from "svelte";
  import InfiniteScroll from "svelte-infinite-scroll";

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
    const content = document.getElementById("content");
    content.style.minHeight = `${100 * (daysAgo + 1)}vh`;

    try {
      const capybara = await CapyAPi.default.getTodayCapybara(daysAgo);
      capybaras = [...capybaras, capybara];

      // Wait for dom to update.
      await new Promise((resolve) => setTimeout(resolve, 10));

      document.getElementById(capybara._id).scrollIntoView({
        behavior: "smooth",
      });

      daysAgo++;

      loading = false;
    } catch (error) {
      capybaras = [...capybaras, null];
      loading = false;
    }
  }

  onMount(async () => {
    document.getElementById("content").scrollTo(0, 0);
    await loadMore();
  });
</script>

<main>
  <div id="content">
    {#each capybaras as capy}
      {#if !capy}
        <div class="unable-to-load">
          <h3>Problem loading this capybara</h3>
          <p>
            Maybe our API is down or we're out of capybaras. Come back later.
          </p>
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
              Capybara from {new Date(capy.used).toLocaleDateString("en-US", {
                year: "numeric",
                month: "short",
                day: "numeric",
              })}
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
    {:else if daysAgo < 2}
      <div class="scroll-to-load">
        <h3>Scroll to load more</h3>
        <i class="las la-angle-down" />
      </div>
    {/if}
  </div>

  <InfiniteScroll threshold={1} on:loadMore={loadMore} />
</main>

<style>
  :global(body) {
    overflow: hidden;
  }

  .capybara-display {
    margin-bottom: 1em;
  }

  #content {
    min-height: 110vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 4em;
  }

  main {
    max-height: 100vh;
    flex: 1;
    overflow: scroll;
  }

  .unable-to-load {
    text-align: center;
    margin-top: 5em;
    width: 100%;
    min-height: 100vh;
  }

  .scroll-to-load {
    margin-top: 2em;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .scroll-to-load i {
    font-size: 2.5em;
  }
</style>
