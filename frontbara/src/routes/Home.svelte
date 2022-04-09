<script lang="ts">
    import { Link } from 'svelte-routing'

    import { submitCapy, getTodayCapy } from '../api'
    import type { iCaptcha, iCapySubmit, iCapy } from '../api/interfaces'
    import { adminStore } from '../stores'
    import Captcha from '../components/Captcha.svelte'

    let page = 0

    let todayCapy: iCapy = {} as iCapy
    getTodayCapy().then(resp => todayCapy = resp)

    let captcha: iCaptcha = {} as iCaptcha
    let captchaCode = ''
    let captchaCompoponet

    let isAdmin = false
    adminStore.subscribe(value => {
        isAdmin = value.is
    })

    let errorMsg = ''
    let successful = ''
    let capyDetails: iCapySubmit = {} as iCapySubmit
    async function attemptCapySubmit() {
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
                    canInvite: false
                })
                errorMsg = 'Admin login has expired, please login again.'
            } else
                errorMsg = (await error.json()).error
        }
        await captchaCompoponet.setCaptcha()
    }
</script>

{#if isAdmin}
    <nav>
        <Link to="/admin"><button>Admin portal</button></Link>
    </nav>
{/if}

<h1>Capybara of the day!</h1>
<img src={todayCapy.image} alt="capy">
<h3 style="text-align: center;">Name: { todayCapy.name }</h3>

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
        <Captcha bind:captchaCode bind:captcha bind:this={captchaCompoponet} />
    {/if}
    <button type="submit">Submit</button>
</form>

<h2>Timeline</h2>
<p style="padding-bottom: 1em;">View the history of capybaras!</p>
<button on:click={() => page++}>Load more</button>
