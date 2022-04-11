<script lang="ts">
    import { navigate } from 'svelte-routing'
    import { SyncLoader } from 'svelte-loading-spinners'

    import type { iAdminDetails, iCaptcha } from '../api/interfaces'
    import { login, logout } from '../api'
    import { adminStore } from '../stores'
    import Captcha from '../components/Captcha.svelte'

    let mode = 'login'
    let errorMsg = ''
    let otpStage = false

    let loginDetails: iAdminDetails = {
        username: '',
        password: '',
        otpCode: 'blank'
    }
    let loginLoading = false

    let captcha: iCaptcha
    let captchaCode: string
    let captchaComponent

    adminStore.set({
        is: false,
        root: false
    })
    logout().then()

    async function attemptLogin() {
        loginLoading = true
        if (mode === 'login' && 'inviteCode' in loginDetails) {
            delete loginDetails.inviteCode
        }
        errorMsg = ''

        try {
            const adminLogin = await login(loginDetails, captcha.captchaId, captchaCode)
            adminStore.set({
                is: true,
                root: adminLogin.isRoot
            })
            if (!adminLogin.otpCompleted) {
                navigate('/otp')
            } else {
                navigate('/admin')
            }
        } catch (error) {
            const errorJson = await error.json()
            if (errorJson.code === 1011) {
                navigate('/otp')
                return
            } else if (errorJson.code === 1010) {
                if (loginDetails.otpCode !== 'blank')
                    errorMsg = errorJson.error
                loginDetails.otpCode = ''
                otpStage = true
                await captchaComponent.setCaptcha()
                loginLoading = false
                return
            }
            await captchaComponent.setCaptcha()
            errorMsg = errorJson.error
        }
        loginLoading = false
    }

</script>

<h2>Login required</h2>
<form on:submit|preventDefault={attemptLogin}>
    {#if errorMsg !== ''}
        <div class="error">
            <p>{ errorMsg }.</p>
        </div>
    {/if}
    {#if !otpStage}
        <label for="username">Username</label>
        <input bind:value={loginDetails.username} type="text" name="username" required placeholder="...">

        <label for="password">Password</label>
        <input bind:value={loginDetails.password} type="password" name="password" required placeholder="...">

        {#if mode === 'register'}
            <label for="invite">Invite code</label>
            <input bind:value={loginDetails.inviteCode} type="password" name="invite" required placeholder="...">
        {/if}
    {:else}
        <label for="otp">Two-factor code</label>
        <input bind:value={loginDetails.otpCode} placeholder="..." type="text" required name="otp">
    {/if}
    <Captcha bind:captchaCode bind:captcha bind:this={captchaComponent} />
    {#if loginLoading}
        <SyncLoader color="#644a4a" />
    {:else}
        <button type="submit" style="text-transform: capitalize;">{ mode }</button>
        <button
            type="button"
            style="background-color: transparent;text-transform: capitalize;text-decoration: underline;"
            on:click={() => mode === 'login' ? mode = 'register' : mode = 'login'}>
            {#if mode === 'login'}
                Register
            {:else}
                Login
            {/if}
        </button>
    {/if}
</form>
