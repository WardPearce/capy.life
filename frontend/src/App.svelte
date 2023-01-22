<script lang="ts">
  import { Router, Route, link, navigate } from "svelte-navigator";

  import Home from "./routes/Home.svelte";
  import LazyRoute from "./routes/LazyRoute.svelte";
  import RouteTransition from "./components/RouteTransition.svelte";
  import PageLoading from "./components/PageLoading.svelte";
  import TransitionContainer from "./components/TransitionContainer.svelte";
  import { loggedIn } from "./store";

  const SubmitLoader = () => import("./routes/Submit.svelte");
  const AdminLoader = () => import("./routes/Admin.svelte");
  const AdminAuthLoader = () => import("./routes/AdminAuth.svelte");

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
      component={SubmitLoader}
      delayMs={500}
    >
      <PageLoading />
    </LazyRoute>
    <LazyRoute
      path="/admin/auth"
      requiresAuth={false}
      component={AdminAuthLoader}
      delayMs={500}
    >
      <PageLoading />
    </LazyRoute>
    <LazyRoute
      path="/admin"
      requiresAuth={true}
      component={AdminLoader}
      delayMs={500}
    >
      <PageLoading />
    </LazyRoute>
  </TransitionContainer>
</Router>
