<script lang="ts">
  import { onMount } from "svelte";
  import { get } from "svelte/store";
  import { loggedIn } from "../store";
  import RouteTransition from "./RouteTransition.svelte";
  export let component;
  export let delayMs = null;
  export let componentProps = null;
  export let requiresAuth = false;
  let loadedComponent = null;
  let timeout;
  let showFallback = !delayMs;
  let props;
  $: {
    // eslint-disable-next-line no-shadow
    const { component, requiresAuth, componentProps, delayMs, ...restProps } =
      $$props;
    props = restProps;
  }
  onMount(() => {
    if (requiresAuth && get(loggedIn).username === "") {
      window.location.href = `${import.meta.env.VITE_API_ENDPOINT}/admin/login`;
    }

    if (delayMs) {
      timeout = setTimeout(() => {
        showFallback = true;
      }, delayMs);
    }
    component().then((module) => {
      loadedComponent = module.default;
    });
    return () => clearTimeout(timeout);
  });
</script>

{#if loadedComponent}
  <RouteTransition>
    <svelte:component this={loadedComponent} {...props} {...componentProps} />
  </RouteTransition>
{:else if showFallback}
  <slot />
{/if}
