<script lang="ts">
  import { Router, Route, link, navigate } from "svelte-navigator";

  import Home from "./routes/Home.svelte";
  import LazyRoute from "./routes/LazyRoute.svelte";
  import RouteTransition from "./components/RouteTransition.svelte";
  import PageLoading from "./components/PageLoading.svelte";
  import TransitionContainer from "./components/TransitionContainer.svelte";

  const SubmitLoader = () => import("./routes/Submit.svelte");
  const AdminLoader = () => import("./routes/Admin.svelte");
</script>

<nav>
  <a href="/" use:link><h1>capy.life</h1></a>
  <button class="button" on:click={() => navigate("/submit")}
    >Submit a Capybara</button
  >
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
      path="/admin"
      requiresAuth={true}
      component={AdminLoader}
      delayMs={500}
    >
      <PageLoading />
    </LazyRoute>
  </TransitionContainer>
</Router>
