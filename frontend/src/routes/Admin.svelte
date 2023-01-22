<script lang="ts">
  import { onMount } from "svelte";
  import { navigate } from "svelte-navigator";
  import { CapyAPi } from "../lib/capy";
  import type { StatsModel } from "../lib/client";
  import { loggedIn } from "../store";

  let admin: { username: string; isRoot: boolean };
  loggedIn.subscribe((event) => (admin = event));

  async function logout() {
    try {
      await CapyAPi.default.adminLogoutLogout();
    } catch (error) {}
    loggedIn.set({ username: "", isRoot: false });
    navigate("/", { replace: true });
  }

  let stats: StatsModel = null;
  onMount(async () => {
    try {
      stats = await CapyAPi.default.adminStatsStats();
    } catch {
      await logout();
    }
  });
</script>

<main>
  <h1 style="margin-top: 1em;">Welcome {admin.username}</h1>

  <h2 style="margin-bottom: 0.5em; margin-top: 1em;">Statistics</h2>
  {#if stats}
    <p>{stats.remaining}/{stats.remaining} Capybaras remaining</p>
  {/if}

  {#if admin.isRoot}
    <h2 style="margin-top: 1em;">Admins</h2>
    <ul>
      <li>Greg (1049963929310330900) <button class="deny">remove</button></li>
    </ul>

    <form style="margin-top: 1em;">
      <h3>Add admin</h3>
      <input type="text" placeholder="Username" />
      <input style="margin-top: .5em;" type="text" placeholder="Discord ID" />
      <button style="margin-top: .5em;" type="submit">Add</button>
    </form>
  {/if}

  <h2 style="margin-top: 1em;">To approve</h2>
  <div class="to-approve">
    <img src="https://capy.life/api/capy/C1JnUlnM8y-NXmroj-cz8" />
    <div class="stats">
      <h3>Name</h3>
      <p>Greg</p>

      <button>Approve</button>
      <button>Approve but change name</button>
      <button class="deny">Deny</button>
    </div>
  </div>
</main>

<style>
  :global(body) {
    overflow: auto;
  }
  main {
    display: block;
    padding: 0 3em;
  }
  .to-approve {
    display: flex;
    margin-top: 1em;
  }

  .to-approve img {
    width: 300px;
  }

  .to-approve .stats {
    margin-left: 1em;
  }

  .to-approve button {
    margin-top: 1em;
  }

  .deny {
    background-color: rgb(129, 26, 26);
    border: none;
  }

  .deny:hover {
    background-color: rgb(226, 21, 21);
  }

  ul li {
    display: flex;
    align-items: center;
    column-gap: 1em;
  }

  @media only screen and (max-width: 930px) {
    .to-approve {
      flex-direction: column;
    }
  }

  @media only screen and (max-width: 930px) {
    .to-approve img {
      width: 100%;
      margin-bottom: 1em;
    }
  }
</style>
