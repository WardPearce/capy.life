<script lang="ts">
  import { navigate } from "svelte-navigator";
  import CapybaraCard from "../components/CapybaraCard.svelte";
</script>

<main>
  <h3 style="margin-bottom: .5em;">Submit a capybara</h3>
  <CapybaraCard editable={true} />

  <button
    style="margin-top: 1em;"
    on:click={() => navigate("/", { replace: true })}>Back</button
  >
</main>
