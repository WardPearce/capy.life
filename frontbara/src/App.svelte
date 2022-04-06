<script lang="ts">
    let page = 0
</script>

<main>
    <section>
        <h1>Capybara of the day!</h1>
        <img src="./src/assets/img/capy.jpg" alt="capy">

        <h2>What is capy.life?</h2>
        <p>Capy.Life is the official daily Capybara site approved by many Zoos & Scientists. 1/10 Endocrinologist say that viewing a Capybara each day drastically improves your mental state.</p>

        <h2 id="submit">Submit a capybara!</h2>
        <form>
            <label for="capy-name">Name <span style="font-size: .7em;">(optional)</span></label>
            <input type="text" maxlength="30" name="capy-name" placeholder="e.g. greg">
            <label for="capy-email">Email <span style="font-size: .7em;">(optional)</span></label>
            <input type="email" name="capy-email" placeholder="receive a email if approved / denied">
            <label for="capy-file">Image</label>
            <input required type="file" name="capy-file" accept="image/png,image/gif,image/jpeg,image/jpg">
            <label for="capy-captcha">Capytcha</label>
            <input type="text" name="capy-captcha" placeholder="beep boop">
            <button type="submit">Submit</button>
        </form>

        <h2>Timeline</h2>
        <p style="padding-bottom: 1em;">View the history of capybaras!</p>
        <button on:click={() => page++}>Load more</button>
    </section>
    <footer>
        <p>Everything on this website is satire & is NOT factually accurate.</p>
        <a href="https://github.com/capylife/capyend" target="_blank" rel="noopener noreferrer">Source code</a>
    </footer>
</main>
