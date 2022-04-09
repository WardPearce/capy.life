<script lang="ts">
    import { Link, navigate } from 'svelte-routing'

    import {
        getToApprove, AdminCapy, getCapyCount,
        logout, generateInvite
    } from '../api'
    import type { iCapy, iCapyCount } from '../api/interfaces'
    import { adminStore } from '../stores'

    let capyCount: iCapyCount  = {} as iCapyCount
    getCapyCount().then(resp => capyCount = resp).catch(error => {
        if (error.status === 401) {
            navigate('/login')
        }
    })

    let toApprove: iCapy[] = []
    getToApprove().then(resp => {
        toApprove = resp
    })

    let canInvite = false
    adminStore.subscribe(value => canInvite = value.canInvite)

    let inviteCode = ''
    async function createInvite() {
        inviteCode = (await generateInvite()).inviteCode
    }

    function removeIdFromList(capyId: string) {
        toApprove = toApprove.filter(capy => capy._id !== capyId)
    }

    async function denyCapy(capyId: string) {
        removeIdFromList(capyId)
        await (new AdminCapy(capyId)).deny()
    }

    async function approveCapy(capyId: string) {
        removeIdFromList(capyId)

        capyCount.total++
        capyCount.remaining++

        await (new AdminCapy(capyId)).approve()
    }

    async function logMeOut() {
        await logout()
        adminStore.set({
            is: false,
            canInvite: false
        })
        navigate('/')
    }
</script>

<Link to="/">
    <button>Home</button>
</Link>

<button on:click={logMeOut}>Logout</button>

{#if canInvite}
    <h2>Invitation codes</h2>
    <form on:submit|preventDefault={createInvite}>
        {#if inviteCode !== ''}
            <input bind:value={inviteCode} type="text" disabled>
        {/if}
        <button type="submit">Generate invite</button>
    </form>
{/if}

<h2>Stats</h2>
<p>Capybaras left: {capyCount.remaining}/{capyCount.total} ({ capyCount.remaining } days covered)</p>

<h2>To approvel</h2>
{#if toApprove.length === 0 }
    <p>No capybaras to approve</p>
{:else}
    <ul class="approval">
        {#each toApprove as capy }
            <li><div class="card">
                <h3>{ capy.name }</h3>
                <img src={capy.image} alt={`Capy named ${capy.name}`}>
                <div>
                    <button on:click={async () => await approveCapy(capy._id)} style="margin-right: .2em;">Approve</button>
                    <button on:click={async () => await denyCapy(capy._id)} class="deny">Deny</button>
                </div>
            </div></li>
        {/each }
    </ul>
{/if}
