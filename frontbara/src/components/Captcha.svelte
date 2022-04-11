<script lang="ts">
    import Fa from 'svelte-fa'
    import { faArrowRotateForward } from '@fortawesome/free-solid-svg-icons'
    import { SyncLoader } from 'svelte-loading-spinners'

    import { getCaptcha } from '../api'
    import type { iCaptcha } from '../api/interfaces'

    export let captchaCode: string = ''
    export let captcha: iCaptcha = {} as iCaptcha

    let captchaLoading = true
    export async function setCaptcha() {
        captchaLoading = true
        captchaCode = ''
        captcha = await getCaptcha()
        captchaLoading = false
    }

    setCaptcha()
</script>

<div>
    <label for="capy-captcha">Capytcha</label>
    {#if captchaLoading}
        <SyncLoader color="#644a4a" />
    {:else}
        <img src={captcha.imageB64} alt="Captcha">
        <button type="button" on:click={setCaptcha}>
            <Fa icon={faArrowRotateForward} />
        </button>
        <input bind:value={captchaCode} required type="text" name="capy-captcha" placeholder="beep boop">
    {/if}
</div>
