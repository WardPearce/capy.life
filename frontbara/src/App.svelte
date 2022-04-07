<script lang="ts">
    import { Router, Route } from 'svelte-routing'

    import Home from './routes/Home.svelte'
    import Admin from './routes/Admin.svelte'
</script>

<main>
    <section>
        <Router>
              <Route path="/" component={Home} />
              <Route path="/admin" component={Admin} />
          </Router>
    </section>
    <footer>
        <p>Everything on this website is satire & is NOT factually accurate.</p>
        <a href="https://github.com/capylife/capyend" target="_blank" rel="noopener noreferrer">Source code</a>
    </footer>
</main>
