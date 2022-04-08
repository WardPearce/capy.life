import type { iCaptcha, iCapySubmit, iCapy, iCapyCount } from './interfaces'

const backendUrl: string = import.meta.env.VITE_URL_PROXIED as string

export async function getCaptcha(): Promise<iCaptcha> {
    const resp = await fetch(`${backendUrl}/api/captcha`)
    if (resp.status !== 200)
        throw resp
    return await resp.json()
}

export async function submitCapy(captchaId: string, captchaCode: string,
                                 details: iCapySubmit) {
    const formData = new FormData()
    formData.append('file', details.image[0])
    if (typeof details.email !== 'undefined')
        formData.append('email', details.email)
    if (typeof details.name !== 'undefined')
        formData.append('name' , details.name)

    const resp = await fetch(`${backendUrl}/api/capy?captchaId=${captchaId}&captchaCode=${captchaCode}`, {
        method: 'POST',
        body: formData
    })
    if (resp.status !== 200)
        throw resp
}

export async function getToApprove(): Promise<iCapy[]> {
    const resp = await fetch(`${backendUrl}/api/admin/approval`)
    if (resp.status !== 200)
        throw resp
    return await resp.json()
}

export async function getTodayCapy(): Promise<iCapy> {
    const resp = await fetch(`${backendUrl}/api`)
    if (resp.status !== 200)
        throw resp
    return await resp.json()
}

export async function getCapyCount(): Promise<iCapyCount> {
    const resp = await fetch(`${backendUrl}/api/admin/remaining`)
    if (resp.status !== 200)
        throw resp
    return await resp.json()
}

export class AdminCapy {
    capyId: string
    constructor(capyId: string) {
        this.capyId = capyId
    }

    async deny() {
        const resp = await fetch(`${backendUrl}/api/admin/approval/${this.capyId}`, {
            method: 'DELETE'
        })
        if (resp.status !== 200)
            throw resp
    }

    async approve() {
        const resp = await fetch(`${backendUrl}/api/admin/approval/${this.capyId}`, {
            method: 'POST'
        })
        if (resp.status !== 200)
            throw resp
    }
}
