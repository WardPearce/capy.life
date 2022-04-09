<script lang="ts">
    import { onMount } from 'svelte'
    import { navigate } from 'svelte-routing'
    import QRCode from 'qrcode'

    import { getOtpQR, setOtpCode } from '../api';

    let errorMsg = ''
    let otpCode = ''

    async function setupOtp() {
        try {
            await setOtpCode(otpCode)
            navigate('/admin')
        } catch (error) {
            otpCode = ''
            errorMsg = (await error.json()).error
        }
    }

    onMount(() => {
        getOtpQR().then(
            resp => {
                QRCode.toCanvas(
                    document.getElementById('qr-code'),
                    resp.provisioningUri
                )
            }
        ).catch(_ => navigate('/'))
    })
</script>

<h2>Two-factor setup required</h2>
<form on:submit|preventDefault={setupOtp}>
    {#if errorMsg !== ''}
        <div class="error">
            <p>{ errorMsg }.</p>
        </div>
    {/if}

    <p>Please scan & enter the code below</p>
    <canvas style="margin: .3em 0;" id="qr-code"></canvas>
    <label for="otp">Two-factor code</label>
    <input bind:value={otpCode} placeholder="..." type="text" required name="otp">

    <button type="submit" style="text-transform: capitalize;">Complete setup</button>
</form>
