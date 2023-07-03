<script lang="ts">
  import { onMount } from "svelte";
  import { SyncLoader } from "svelte-loading-spinners";
  import PageLoading from "../components/PageLoading.svelte";
  import { CapyAPi } from "../lib/capy";
  import type {
    ListAdminsModel,
    StatsModel,
    ToApproveModel,
  } from "../lib/client";
  import { timeout } from "../lib/timeout";
  import { loggedIn } from "../store";
  let admin: { username: string; isRoot: boolean };
  loggedIn.subscribe((event) => (admin = event));

  let stats: StatsModel = null;
  let currentAdmins: ListAdminsModel = null;
  let toApprove: ToApproveModel = null;
  let toApproveLoading = false;
  let pageLoading = true;
  onMount(async () => {
    pageLoading = true;
    try {
      stats = await CapyAPi.admin.adminStatsStats();
      currentAdmins = await CapyAPi.admin.adminListListAdmins();
      await getCapybaraToApprove();
    } catch {
      window.location.href = `${import.meta.env.VITE_API_ENDPOINT}/admin/login`;
    }
    pageLoading = false;
  });

  async function getCapybaraToApprove() {
    toApproveLoading = true;
    toApprove = await CapyAPi.admin.adminToApproveToApprove();
    toApproveLoading = false;
  }

  async function filterCapy(capyId: string) {
    toApprove.to_approve = toApprove.to_approve.filter(
      (capy) => capy._id !== capyId
    );

    if (toApprove.to_approve.length === 0) {
      // Wait 500ms before fetching more capybaras to approve.
      await timeout(500);
      await getCapybaraToApprove();
    }
  }

  async function approveCapy(capyId: string, changeName: boolean = false) {
    stats.total++;
    stats.remaining++;
    await filterCapy(capyId);
    await CapyAPi.admin.adminApproveApproveCapy(capyId, changeName ? 1 : 0);
  }

  async function denyCapy(capyId: string) {
    await filterCapy(capyId);
    await CapyAPi.admin.adminDenyDenyCapy(capyId);
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

{#if pageLoading}
  <PageLoading />
{:else}
  <main>
    <h1 style="margin-top: 1em;">Welcome {admin.username}</h1>

    {#if stats}
      <h2 style="margin-bottom: 0.5em; margin-top: 1em;">Statistics</h2>
      <p>{stats.remaining}/{stats.total} Capybaras remaining</p>
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
    {#if toApproveLoading}
      <SyncLoader color="var(--capyLight)" size={40} />
    {:else if !toApprove || toApprove.to_approve.length == 0}
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
            <p>{capy.name}</p>

            <button on:click={() => approveCapy(capy._id, false)}
              >Approve</button
            >
            <button on:click={() => approveCapy(capy._id, true)}
              >Approve but change name</button
            >
            <button class="deny" on:click={() => denyCapy(capy._id)}
              >Deny</button
            >
          </div>
        </div>
      {/each}
    {/if}
  </main>
{/if}

<style>
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
