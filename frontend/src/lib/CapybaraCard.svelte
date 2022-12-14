<script lang="ts">
  import { SyncLoader } from "svelte-loading-spinners";
  import Image from "./Image.svelte";

  export let imgSrc: string | null = null;
  export let name: string | null = null;
  export let fighterClass: string | null = null;
  export let muncherLvl: string | null = null;
  export let weaponOfChoice: string | null = null;
  export let isSingle: boolean | null = null;
  export let editable = true;

  let fileInput;
  let filePreview = null;

  function previewImage(e) {
    const imgReader = new FileReader();
    imgReader.readAsDataURL(e.target.files[0]);
    imgReader.onload = (e) => (filePreview = e.target.result);
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
  <div class="capybara-stats">
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
        <h2>Name<i class="las la-praying-hands" /></h2>
        {#if !editable}
          {#if !name}
            <SyncLoader color="var(--capyLight)" size={50} />
          {:else}
            <h3>{name}</h3>
          {/if}
        {:else}
          <input type="text" />
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
          <input type="text" />
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
          <input type="text" />
        {/if}
      </li>
      <li>
        <h2>Relationship status<i class="las la-heart" /></h2>
        {#if !editable}
          {#if isSingle === true || isSingle === false}
            <h3>
              {isSingle ? "Single" : "Taken"}
            </h3>
          {:else}
            <SyncLoader color="var(--capyLight)" size={50} />
          {/if}
        {:else}
          <input type="text" />
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
          <input type="text" />
        {/if}
      </li>
      {#if editable}
        <li style="padding-right: 1em;">
          <button class="button-alt" type="submit" style="margin-top: 1em;"
            >Create</button
          >
        </li>
      {/if}
    </ul>
  </div>
</div>
