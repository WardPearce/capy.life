<script lang="ts">
  import { Circle, SyncLoader } from "svelte-loading-spinners";
  import { navigate } from "svelte-navigator";
  import Select from "svelte-select";

  import { CapyAPi } from "../lib/capy";
  import { ApiError, RelationshipEnum, type SubmitModal } from "../lib/client";
  import Image from "./Image.svelte";

  export let imgSrc: string | null = null;
  export let name: string | null = null;
  export let fighterClass: string | null = null;
  export let muncherLvl: number | null = null;
  export let weaponOfChoice: string | null = null;
  export let relationship_status: RelationshipEnum = null;
  export let editable = true;

  let submittingCapybara = false;
  let errorMsg = "";

  async function submitCapybara() {
    submittingCapybara = true;
    let payload: SubmitModal = {
      name: name,
      image: new File([await (await fetch(filePreview)).blob()], fileName),
    };
    if (relationship_status) payload.relationship_status = relationship_status;
    try {
      await CapyAPi.default.submitCapy(payload);
      navigate("/", { replace: true });
    } catch (error) {
      if (error instanceof ApiError) errorMsg = error.body.detail;
      else error = error.toString();
    }
    submittingCapybara = false;
  }

  let fileInput;
  let filePreview: string | null = null;
  let fileName: string | null = null;

  function previewImage(event: Event & { currentTarget: HTMLInputElement }) {
    fileName = event.currentTarget.files[0].name;
    const imgReader = new FileReader();
    imgReader.readAsDataURL(event.currentTarget.files[0]);
    imgReader.onload = (loadEvent) =>
      (filePreview = loadEvent.target.result as string);
  }
</script>

<div class="capybara-card">
  <div class="today-capybara">
    {#if !editable}
      <Image src={imgSrc} alt="Today's capybara" />
    {:else if !filePreview}
      <h3>No image selected</h3>
    {:else}
      <img src={filePreview} alt="Today's capybara" class="today-capybara" />
    {/if}
  </div>
  <form on:submit|preventDefault={submitCapybara} class="capybara-stats">
    <ul>
      {#if editable}
        <li>
          <h2>Image<i class="las la-camera" /></h2>
          <input
            type="file"
            name="capybara-image"
            accept="image/png,image/gif,image/jpeg,image/jpg"
            bind:this={fileInput}
            on:change={previewImage}
          />
        </li>
      {/if}
      <li>
        <h2>
          Name<i class="las la-praying-hands" />
          {#if editable}
            <span style="font-size: .5em;margin-left:1em;"> (Optional)</span>
          {/if}
        </h2>
        {#if !editable}
          {#if !name}
            <SyncLoader color="var(--capyLight)" size={50} />
          {:else}
            <h3>{name}</h3>
          {/if}
        {:else}
          <input type="text" bind:value={name} />
        {/if}
      </li>
      <li>
        <h2>Class<i class="las la-shield-alt" /></h2>
        {#if !editable}
          {#if !fighterClass}
            <SyncLoader color="var(--capyLight)" size={50} />
          {:else}
            <h3>{fighterClass}</h3>
          {/if}
        {:else}
          <p>randomly generated</p>
        {/if}
      </li>
      <li>
        <h2>Muncher lvl<i class="las la-apple-alt" /></h2>
        {#if !editable}
          {#if !muncherLvl}
            <SyncLoader color="var(--capyLight)" size={50} />
          {:else}
            <h3>{muncherLvl}</h3>
          {/if}
        {:else}
          <p>randomly generated</p>
        {/if}
      </li>
      <li>
        <h2>
          Relationship status<i class="las la-heart" />
          {#if editable}
            <span style="font-size: .5em;margin-left:1em;"> (Optional)</span>
          {/if}
        </h2>
        {#if !editable}
          {#if relationship_status}
            <h3>
              {relationship_status}
            </h3>
          {:else}
            <SyncLoader color="var(--capyLight)" size={50} />
          {/if}
        {:else}
          <Select
            items={Object.values(RelationshipEnum)}
            on:select={(event) => {
              relationship_status = event.detail.value;
            }}
          />
        {/if}
      </li>
      <li>
        <h2>Weapon of choice<i class="las la-laugh-wink" /></h2>
        {#if !editable}
          {#if !weaponOfChoice}
            <SyncLoader color="var(--capyLight)" size={50} />
          {:else}
            <h3>{weaponOfChoice}</h3>
          {/if}
        {:else}
          <p>randomly generated</p>
        {/if}
      </li>
      {#if editable}
        <li style="padding-right: 1em;">
          {#if errorMsg}
            <div style="background-color: var(--capyError);padding:.5em 1em;">
              <h3>Error</h3>
              <p>{errorMsg}</p>
            </div>
          {/if}
          <button
            disabled={!filePreview || submittingCapybara}
            class="button-alt"
            type="submit"
            style="margin-top: 1em;"
          >
            {#if submittingCapybara}
              <Circle color="var(--capyText)" size={20} />
              <p style="margin-left: 1em;">Submitting capybara...</p>
            {:else}
              Create
            {/if}
          </button>
        </li>
      {/if}
    </ul>
  </form>
</div>
