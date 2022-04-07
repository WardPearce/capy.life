<script lang="ts">
    import { getToApprove, AdminCapy } from '../api'
    import type { iToApproveCapy } from '../api/interfaces'

    let toApprove: iToApproveCapy[] = []
    getToApprove().then(resp => {
        toApprove = resp
    })

    function removeIdFromList(capyId: string) {
        toApprove = toApprove.filter(capy => capy._id !== capyId)
    }

    async function denyCapy(capyId: string) {
        removeIdFromList(capyId)
        await (new AdminCapy(capyId)).deny()
    }

    async function approveCapy(capyId: string) {
        removeIdFromList(capyId)
        await (new AdminCapy(capyId)).approve()
    }
</script>

<a href="/" style="padding-bottom: 1em;display:block;">Home</a>

{#if toApprove.length === 0 }
    <h3>No capybaras to approve</h3>
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
