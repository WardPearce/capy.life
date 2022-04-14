<script lang="ts">
    import { navigate } from 'svelte-routing'
    import { SyncLoader } from 'svelte-loading-spinners'
    import zxcvbn from 'zxcvbn'

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

    let passwordStrength: typeof zxcvbn = {}

    adminStore.set({
        is: false,
        root: false
    })
    logout().then()

    function passwordCheck() {
        if (mode !== 'register')
            return
        passwordStrength = zxcvbn(loginDetails.password)
    }

    async function attemptLogin() {
        loginLoading = true
        if (mode === 'login' && 'inviteCode' in loginDetails) {
            delete loginDetails.inviteCode
        }
        errorMsg = ''

        if (mode === 'register') {
            passwordCheck()
            if (passwordStrength.score < 2) {
                errorMsg = 'Password too weak, please provide something stronger'
                loginLoading = false
                return
            }
        }

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
        <input on:input={passwordCheck} bind:value={loginDetails.password} type="password" name="password" required placeholder="...">

        {#if mode === 'register'}
            {#if Object.keys(passwordStrength).length !== 0}
                <p style="margin-bottom: .5em;margin-top:0;">
                    <span style="font-weight: 300;">Strength:</span>
                    {passwordStrength.crack_times_display.offline_slow_hashing_1e4_per_second}
                    to guess.
                </p>
            {/if}
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
