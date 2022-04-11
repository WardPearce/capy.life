<script lang="ts">
    import { Link } from 'svelte-routing'
    import { SyncLoader } from 'svelte-loading-spinners'

    import { submitCapy, getTodayCapy, getCapyHistory } from '../api'
    import type { iCaptcha, iCapySubmit, iCapy, iCapyHistory } from '../api/interfaces'
    import { adminStore } from '../stores'
    import Captcha from '../components/Captcha.svelte'

    let todayCapyError = ''
    let todayCapy: iCapy = {} as iCapy
    getTodayCapy().then(resp => {
        todayCapy = resp
    }).catch(async error => todayCapyError = (await error.json()).error)

    let captcha: iCaptcha
    let captchaCode: string
    let captchaComponent

    let isAdmin = false
    adminStore.subscribe(value => {
        isAdmin = value.is
    })

    let errorMsg = ''
    let successful = ''
    let capyDetails: iCapySubmit = {} as iCapySubmit
    let capySubmitting = false
    async function attemptCapySubmit() {
        capySubmitting = true
        errorMsg = ''
        successful = ''
        try {
            await submitCapy(captcha?.captchaId, captchaCode, capyDetails)
            capyDetails = {
                // eslint-disable-next-line @typescript-eslint/ban-ts-comment
                // @ts-ignore
                image: ''
            }
            successful = 'Capybara has been submitted for approval!'
        } catch (error) {
            if (isAdmin && error.code === 1001) {
                adminStore.set({
                    is: false,
                    root: false
                })
                errorMsg = 'Admin login has expired, please login again.'
            } else
                errorMsg = (await error.json()).error
        }
        await captchaComponent.setCaptcha()
        capySubmitting = false
    }

    let capyHistoryPage = 1
    let capyHistory: iCapyHistory[] = []
    getCapyHistory().then(history => capyHistory = history)

    async function loadMoreHistory() {
        capyHistoryPage++
        capyHistory = await getCapyHistory(capyHistoryPage)
    }
</script>

{#if isAdmin}
    <nav>
        <Link to="/admin"><button>Admin portal</button></Link>
    </nav>
{/if}

<main>
    <h1>Capybara of the day!</h1>
    {#if todayCapyError !== ''}
        <div class="error">
            <p>{ todayCapyError }.</p>
        </div>
    {:else if Object.keys(todayCapy).length === 0}
        <SyncLoader color="#644a4a" />
    {:else}
        <img src={todayCapy.image} alt="capy">
        <h3 style="text-align: center;">Name: { todayCapy.name }</h3>
    {/if}
</main>

<h2>What is capy.life?</h2>
<p>Capy.Life is the official daily Capybara site approved by many Zoos & Scientists. 1/10 Endocrinologist say that viewing a Capybara each day drastically improves your mental state.</p>

<h2 id="submit">Submit a capybara!</h2>
<form on:submit|preventDefault={attemptCapySubmit}>
    {#if errorMsg !== ''}
        <div class="error">
            <p>{ errorMsg }.</p>
        </div>
    {/if}

    {#if successful !== ''}
        <div class="successful">
            <p>{ successful }</p>
        </div>
    {/if}
    <label for="capy-name">Capybara name <span style="font-size: .7em;">(optional)</span></label>
    <input bind:value={capyDetails.name} type="text" maxlength="30" name="capy-name" placeholder="e.g. greg">

    {#if !isAdmin}
        <label for="capy-email">Email <span style="font-size: .7em;">(optional)</span></label>
        <input bind:value={capyDetails.email} type="email" name="capy-email" placeholder="e.g. example@pm.me">
    {/if}

    <label for="capy-file">Image</label>
    <input bind:files={capyDetails.image} required type="file" name="capy-file" accept="image/png,image/gif,image/jpeg,image/jpg">
    {#if !isAdmin}
        <Captcha bind:captchaCode bind:captcha bind:this={captchaComponent} />
    {/if}
    {#if !capySubmitting}
        <button type="submit">Submit</button>
    {:else}
        <SyncLoader color="#644a4a" />
    {/if}
</form>

{#if capyHistory.length > 0}
    <h2>Timeline</h2>
    <p style="padding-bottom: 1em;">View the history of capybaras!</p>
    <ul class="approval capy-history">
        {#each capyHistory as history}
            <li><div class="card" style="display: flex;justify-content: space-between;align-items: center;">
                <div class="capy-name-date">
                    <h3>{history.name}</h3>
                    <p>{history.used}</p>
                </div>
                <img
                    src={history.image}
                    alt={`Capybara named ${history.name}`}
                    loading="lazy"
                >
            </div></li>
        {/each}
    </ul>
    {#if capyHistory.length % 5 === 0}
        <button on:click={loadMoreHistory}>Load more</button>
    {/if}
{/if}
