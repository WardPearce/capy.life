<script lang="ts">
  import { onMount } from "svelte";
  import { navigate } from "svelte-navigator";
  import { CapyAPi } from "../lib/capy";
  import type {
    ListAdminsModel,
    StatsModel,
    ToApproveModel,
  } from "../lib/client";
  import { loggedIn } from "../store";

  let admin: { username: string; isRoot: boolean };
  loggedIn.subscribe((event) => (admin = event));

  async function logout() {
    try {
      await CapyAPi.admin.adminLogoutLogout();
    } catch (error) {}
    loggedIn.set({ username: "", isRoot: false });
    navigate("/", { replace: true });
  }

  let stats: StatsModel = null;
  let currentAdmins: ListAdminsModel = null;
  let toApprove: ToApproveModel = null;
  onMount(async () => {
    try {
      stats = await CapyAPi.admin.adminStatsStats();
    } catch {
      await logout();
    }

    currentAdmins = await CapyAPi.admin.adminListListAdmins();
    toApprove = await CapyAPi.admin.adminToApproveToApprove();
  });

  async function approveCapy(capyId: string, changeName: boolean = false) {
    await CapyAPi.admin.adminApproveApproveCapy(capyId, changeName ? 1 : 0);
    toApprove = await CapyAPi.admin.adminToApproveToApprove();
  }

  async function denyCapy(capyId: string) {
    await CapyAPi.admin.adminDenyDenyCapy(capyId);
    toApprove = await CapyAPi.admin.adminToApproveToApprove();
  }

  async function removeAdmin(discordId: string) {
    await CapyAPi.admin.adminRemoveRemoveAdmin(discordId);
    currentAdmins = await CapyAPi.admin.adminListListAdmins();
  }

  let addUsername: string;
  let addDiscordId: string;
  async function addAdmin() {
    await CapyAPi.admin.adminAddAddAdmin({
      username: addUsername,
      _id: addDiscordId,
    });

    addUsername = "";
    addDiscordId = "";

    currentAdmins = await CapyAPi.admin.adminListListAdmins();
  }
</script>

<main>
  <h1 style="margin-top: 1em;">Welcome {admin.username}</h1>

  <h2 style="margin-bottom: 0.5em; margin-top: 1em;">Statistics</h2>
  {#if stats}
    <p>{stats.remaining}/{stats.remaining} Capybaras remaining</p>
  {/if}

  {#if admin.isRoot && currentAdmins !== null}
    <h2 style="margin-top: 1em;">Admins</h2>
    <ul>
      {#each currentAdmins.admins as admin}
        {#if !admin.is_root}
          <li>
            {admin.username} ({admin._id})
            <button class="deny" on:click={() => removeAdmin(admin._id)}
              >remove</button
            >
          </li>
        {/if}
      {/each}
    </ul>

    <form style="margin-top: 1em;" on:submit|preventDefault={addAdmin}>
      <h3>Add admin</h3>
      <input bind:value={addUsername} type="text" placeholder="Username" />
      <input
        bind:value={addDiscordId}
        style="margin-top: .5em;"
        type="text"
        placeholder="Discord ID"
      />
      <button style="margin-top: .5em;" type="submit">Add</button>
    </form>
  {/if}

  <h2 style="margin-top: 1em;">To approve</h2>
  {#if !toApprove || toApprove.to_approve.length == 0}
    <h4>nothing to approve</h4>
  {:else}
    {#each toApprove.to_approve as capy}
      <div class="to-approve">
        <img
          src={capy.image}
          referrerpolicy="no-referrer"
          alt="Capybara to approve"
        />
        <div class="stats">
          <h3>Name</h3>
          <p>Greg</p>

          <button on:click={() => approveCapy(capy._id, false)}>Approve</button>
          <button on:click={() => approveCapy(capy._id, true)}
            >Approve but change name</button
          >
          <button class="deny" on:click={() => denyCapy(capy._id)}>Deny</button>
        </div>
      </div>
    {/each}
  {/if}
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
    margin: 1em 0;
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
