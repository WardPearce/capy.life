<script lang="ts">
    import { Link, navigate } from 'svelte-routing'
    import { io } from 'socket.io-client'
    import { SyncLoader } from 'svelte-loading-spinners'

    import Fa from 'svelte-fa'
    import {
        faCheckSquare, faSquareXmark, faTrash, faCheck, faXmark,
        faRotate, faHomeAlt, faRightFromBracket, faArrowDown
    } from '@fortawesome/free-solid-svg-icons'

    import {
        getToApprove, AdminCapy, getCapyCount,
        logout, generateInvite, getInvites, deleteInvite,
        getApprovalHistory, deleteCapy
    } from '../api'
    import type { iCapy, iCapyCount } from '../api/interfaces'
    import { adminStore } from '../stores'

    let pageLoading = true
    let approvedNames = {}

    let capyCount: iCapyCount  = {} as iCapyCount
    getCapyCount().then(resp =>{
        capyCount = resp
        pageLoading = false
    }).catch(_ => {
        navigate('/login')
    })

    let toApprove: iCapy[] = []
    getToApprove().then(resp => {
        toApprove = resp
    })

    let isRoot = false
    let invites = []
    adminStore.subscribe(async value => {
        isRoot = value.root
        if (isRoot) {
            invites = await getInvites()
        }
    })

    let historyPage = 1
    let approvalHistory = []
    getApprovalHistory().then(resp => approvalHistory = resp)

    async function loadMoreHistory() {
        historyPage++
        approvalHistory = [
            ...approvalHistory,
            ...await getApprovalHistory(historyPage)
        ]
    }

    async function removeCapy(capyId: string) {
        try {
            await deleteCapy(capyId)
            approvalHistory = approvalHistory.filter(capy => capy._id !== capyId)
        } catch (error) {}
    }

    let inviteCode = ''
    async function createInvite() {
        inviteCode = (await generateInvite()).inviteCode
        invites.push(inviteCode.split('/', 1))
        invites = invites
    }

    async function removeInvite(inviteId: string) {
        inviteCode = ''
        try {
            await deleteInvite(inviteId)
        } catch (error) {return}
        invites = invites.filter(id => id !== inviteId)
    }

    function removeIdFromList(capyId: string) {
        toApprove = toApprove.filter(capy => capy._id !== capyId)
    }

    async function denyCapy(capyId: string) {
        try {
            await (new AdminCapy(capyId)).deny()
            removeIdFromList(capyId)
        } catch (error) {
            navigate('/login')
            return
        }
        if (toApprove.length === 0) {
            toApprove = await getToApprove()
        }
    }

    async function approveCapy(capyId: string) {
        capyCount.total++
        capyCount.remaining++

        try {
            await (new AdminCapy(capyId)).approve(
                capyId in approvedNames ? !(approvedNames[capyId]) : false
            )
            // Kinda ugly, but fast.
            for (let index = 0; index < toApprove.length; index++) {
                const element = toApprove[index]
                if (element._id === capyId) {
                    approvalHistory = [
                        element,
                        ...approvalHistory
                    ]
                    break
                }
            }
            removeIdFromList(capyId)
        } catch (error) {
            navigate('/login')
            return
        }
        if (toApprove.length === 0) {
            toApprove = await getToApprove()
        }
    }

    async function logMeOut() {
        await logout()
        adminStore.set({
            is: false,
            root: false
        })
        navigate('/')
    }

    const socket = io(
        import.meta.env.VITE_URL_PROXIED as string
    )
    socket.connect()
    socket.on('disconnect', () => {
        socket.connect()
    })

    socket.on('approval_update', (data) => {
        removeIdFromList(data._id)
    })
</script>

{#if pageLoading}
    <div class="loading-center">
        <SyncLoader color="#644a4a" />
    </div>
{:else}
<nav>
    <Link to="/">
        <button>
            <Fa icon={faHomeAlt} /> Home
        </button>
    </Link>
    
    <button on:click={logMeOut}>
        <Fa icon={faRightFromBracket} /> Logout
    </button>
</nav>

{#if isRoot}
    <h2>Invitation codes</h2>
    {#if invites.length === 0 }
        <p style="margin-bottom: .5em;">No invites</p>
    {:else}
        <ul class="approval">
            {#each invites as code }
                <li><div class="card center">
                    <p>{ code }</p>
                    <button class="deny" on:click={async () => await removeInvite(code)}>
                        <Fa icon={faTrash} /> Remove
                    </button>
                </div></li>
            {/each}
        </ul>
    {/if}
    <form on:submit|preventDefault={createInvite}>
        {#if inviteCode !== ''}
            <input bind:value={inviteCode} type="text" disabled>
        {/if}
        <button type="submit">
            <Fa icon={faRotate} /> Generate invite
        </button>
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
                <label style="cursor: pointer;">
                    <input on:click={() => capy._id in approvedNames ? approvedNames[capy._id] = !approvedNames[capy._id] : approvedNames[capy._id] = false} style="display: none;" type="checkbox" checked>
                    <h3>
                        {#if !(capy._id in approvedNames) || approvedNames[capy._id]}
                            <Fa icon={faCheckSquare} style="color: #11c650;" />
                        {:else}
                            <Fa icon={faSquareXmark} style="color: #d11414;" />
                        {/if}
                        { capy.name }
                    </h3>
                </label>
                  
                <img src={capy.image} alt={`Capy named ${capy.name}`}>
                <div>
                    <button on:click={async () => await approveCapy(capy._id)} style="margin-right: .2em;">
                        <Fa icon={faCheck} /> Approve
                    </button>
                    <button on:click={async () => await denyCapy(capy._id)} class="deny">
                        <Fa icon={faXmark} /> Deny
                    </button>
                </div>
            </div></li>
        {/each }
    </ul>
{/if}

<h2>{!isRoot ? 'My' : ''} Approval History</h2>
{#if approvalHistory.length === 0 }
    <p>No history</p>
{:else}
    <ul class="approval">
        {#each approvalHistory as capy }
            <li><div class="card">
                <h3>
                    { capy.name }
                </h3>
                {#if isRoot}
                    <p><span style="font-weight: 300;">Admin:</span> {capy.approvedBy}</p>
                {/if}
                <p><span style="font-weight: 300;">Approved:</span> {capy.approvedAt}</p>
                <img src={capy.image} alt={`Capy named ${capy.name}`} loading="lazy">
                <div>
                    <button on:click={async () => await removeCapy(capy._id)} class="deny">
                        <Fa icon={faTrash} /> Remove
                    </button>
                </div>
            </div></li>
        {/each }
    </ul>
    {#if approvalHistory.length % 5 === 0}
        <button on:click={loadMoreHistory}>
            Load more
        </button>
    {/if}
{/if}
{/if}
