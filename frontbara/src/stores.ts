import { writable } from 'svelte-local-storage-store'

export const adminStore = writable('admin', {
    is: false,
    canInvite: false
})
