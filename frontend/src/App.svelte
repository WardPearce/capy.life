<script lang="ts">
  import { Route, Router, link, navigate } from "svelte-navigator";

  import PageLoading from "./components/PageLoading.svelte";
  import RouteTransition from "./components/RouteTransition.svelte";
  import TransitionContainer from "./components/TransitionContainer.svelte";
  import Home from "./routes/Home.svelte";
  import LazyRoute from "./routes/LazyRoute.svelte";
  import { loggedIn } from "./store";

  let isAdmin = false;
  loggedIn.subscribe((admin) => (isAdmin = admin.username !== ""));
</script>

<nav>
  <a href="/" use:link><h1>capy.life</h1></a>
  <div style="display: flex;align-items:center;">
    {#if isAdmin}
      <a href="/admin" use:link style="margin-right: 1em;">Admin Portal</a>
    {/if}
    <button class="button" on:click={() => navigate("/submit")}
      >Submit a Capybara</button
    >
  </div>
</nav>

<Router primary={false}>
  <TransitionContainer>
    <Route path="/">
      <RouteTransition><Home /></RouteTransition>
    </Route>
    <LazyRoute
      path="/submit"
      requiresAuth={false}
      component={() => import("./routes/Submit.svelte")}
      delayMs={100}
    >
      <PageLoading />
    </LazyRoute>
    <LazyRoute
      path="/admin/auth"
      requiresAuth={false}
      component={() => import("./routes/AdminAuth.svelte")}
      delayMs={100}
    >
      <PageLoading />
    </LazyRoute>
    <LazyRoute
      path="/admin"
      requiresAuth={true}
      component={() => import("./routes/Admin.svelte")}
      delayMs={100}
    >
      <PageLoading />
    </LazyRoute>
  </TransitionContainer>
</Router>
