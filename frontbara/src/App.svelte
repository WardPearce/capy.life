<script lang="ts">
    import { Router, Route } from 'svelte-routing'

    import Home from './routes/Home.svelte'
    import Admin from './routes/Admin.svelte'
    import Login from './routes/Login.svelte'
    import Otp from './routes/Otp.svelte'
</script>

<main>
    <section>
        <Router>
              <Route path="/" component={Home} />
              <Route path="/admin" component={Admin} />
              <Route path="/login" component={Login} />
              <Route path="/otp" component={Otp} />
          </Router>
    </section>
    <footer>
        <p>Everything on this website is satire & is NOT factually accurate.</p>
        <a href="https://github.com/capylife/capyend" target="_blank" rel="noopener noreferrer">Source code</a>
    </footer>
</main>
