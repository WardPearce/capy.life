<script lang="ts">
  import { onMount } from "svelte";
  import { get } from "svelte/store";
  import { loggedIn } from "../store";
  import RouteTransition from "./RouteTransition.svelte";

  export let component: any;
  export let delayMs: number = null;
  export let componentProps: any = null;
  export let requiresAuth = false;

  let loadedComponent: any = null;
  let timeout: NodeJS.Timeout;
  let showFallback = !delayMs;
  let props: Record<any, any>;
  $: {
    // eslint-disable-next-line no-shadow
    const { component, requiresAuth, componentProps, delayMs, ...restProps } =
      $$props;
    props = restProps;
  }
  onMount(() => {
    if (requiresAuth && get(loggedIn).username === "") {
      window.location.href = `${import.meta.env.VITE_API_ENDPOINT}/admin/login`;
      return;
    }

    if (delayMs) {
      timeout = setTimeout(() => {
        showFallback = true;
      }, delayMs);
    }
    component().then((module: any) => {
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
