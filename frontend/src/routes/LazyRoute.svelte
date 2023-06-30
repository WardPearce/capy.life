<script lang="ts">
  import { Route } from "svelte-navigator";
  import Lazy from "../components/Lazy.svelte";
  export let component;
  export let delayMs = null;
  export let componentProps = null;
  export let requiresAuth = false;
  let props;
  $: {
    // eslint-disable-next-line no-shadow
    const { component, ...restProps } = $$props;
    props = restProps;
  }
</script>

<Route {...props}>
  <Lazy {component} {delayMs} {componentProps} {requiresAuth}>
    <slot />
  </Lazy>
</Route>
