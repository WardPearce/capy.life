<script lang="ts">
  import { navigate } from "svelte-navigator";
  import InfiniteScroll from "svelte-infinite-scroll";
  import { onMount } from "svelte";

  import CapybaraCard from "../components/CapybaraCard.svelte";
  import { CapyAPi } from "../lib/capy";
  import type { CapybaraModel } from "../lib/client";

  let capybaras: Array<CapybaraModel | null> = [];
  let daysAgo = 0;

  async function loadMore() {
    try {
      const capybara = await CapyAPi.default.getTodayCapybara(daysAgo);
      capybaras = [...capybaras, capybara];
    } catch (error) {
      capybaras = [...capybaras, null];
    }

    document.getElementById("content").style.height =
      document.getElementById("content").clientHeight * 2 + "px";

    daysAgo++;
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
          <h2 style="margin-bottom: .5em;margin-top:1em;">
            {#if capy.days_ago == 0}
              Today's capybara
            {:else if capy.days_ago < 25}
              Capybara from {capy.days_ago}
              {capy.days_ago > 1 ? "days" : "day"} ago
            {:else}
              Capybara from {new Date(capy.used).toLocaleDateString("en-US", {
                weekday: "long",
                year: "numeric",
                month: "short",
                day: "numeric",
              })}
            {/if}
          </h2>

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
  </div>
  <InfiniteScroll threshold={1} on:loadMore={loadMore} />
</main>

<style>
  .capybara-display {
    margin-bottom: 1em;
  }

  #content {
    min-height: 110vh;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  main {
    max-height: 100vh;
    flex: 1;
    overflow: scroll;
  }

  .unable-to-load {
    text-align: center;
    width: 100%;
    min-height: 100vh;
  }
</style>
