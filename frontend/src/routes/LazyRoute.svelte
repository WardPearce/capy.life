<script lang="ts">
  import { Route } from "svelte-navigator";
  import Lazy from "../components/Lazy.svelte";

  export let component: any;
  export let delayMs: number | null = null;
  export let componentProps: any = null;
  export let requiresAuth = false;

  let props: Record<any, any>;
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
