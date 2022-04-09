<script lang="ts">
    import Fa from 'svelte-fa'
    import { faArrowRotateForward } from '@fortawesome/free-solid-svg-icons'

    import { getCaptcha } from '../api'
    import type { iCaptcha } from '../api/interfaces'

    export let captchaCode: string = ''
    export let captcha: iCaptcha = {} as iCaptcha

    export async function setCaptcha() {
        captchaCode = ''
        captcha = await getCaptcha()
    }

    setCaptcha()
</script>

<div>
    <label for="capy-captcha">Capytcha</label>
    <img src={captcha.imageB64} alt="Captcha">
    <button type="button" on:click={setCaptcha}>
        <Fa icon={faArrowRotateForward} />
    </button>
    <input bind:value={captchaCode} required type="text" name="capy-captcha" placeholder="beep boop">
</div>
