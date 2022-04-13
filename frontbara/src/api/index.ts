import type {
    iCaptcha, iCapySubmit, iCapy, iCapyCount,
    iAdminLogin, iAdminDetails, iAdminOtp,
    iAdminInvite, iCapyHistory
} from './interfaces'

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
    const resp = await fetch(`${backendUrl}/api/`)
    if (resp.status !== 200)
        throw resp
    return await resp.json()
}

export async function getCapyHistory(page: number = 1): Promise<iCapyHistory[]> {
    const resp = await fetch(`${backendUrl}/api/capy/timeline?page=${page}`)
    if (resp.status !== 200)
        throw resp
    return await resp.json()
}

export async function getApprovalHistory(page: number = 1): Promise<iCapyHistory[]> {
    const resp = await fetch(`${backendUrl}/api/admin/approval/history?page=${page}`)
    if (resp.status !== 200)
        throw resp
    return await resp.json()
}

export async function deleteCapy(capyId: string) {
    const resp = await fetch(`${backendUrl}/api/admin/approval/${capyId}/remove`, {
        method: 'DELETE'
    })
    if (resp.status !== 200)
        throw resp
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

    async approve(changeName: boolean = false) {
        const resp = await fetch(`${backendUrl}/api/admin/approval/${this.capyId}?changeName=${changeName.toString()}`, {
            method: 'POST'
        })
        if (resp.status !== 200)
            throw resp
    }
}


export async function login(details: iAdminDetails, captchaId: string, captchaCode: string): Promise<iAdminLogin> {
    let payload = {
        username: details.username,
        password: details.password
    }

    if (details.otpCode)
        payload['otpCode'] = details.otpCode

    if (details.inviteCode)
        payload['inviteCode'] = details.inviteCode

    const resp = await fetch(`${backendUrl}/api/admin/login?captchaId=${captchaId}&captchaCode=${captchaCode}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    if (resp.status !== 200)
        throw resp
    return await resp.json()
}

export async function logout() {
    await fetch(`${backendUrl}/api/admin/login`, {
        method: 'DELETE'
    })
}

export async function getOtpQR(): Promise<iAdminOtp> {
    const resp = await fetch(`${backendUrl}/api/admin/login/otp`, {
        method: 'GET'
    })
    if (resp.status !== 200)
        throw resp
    return await resp.json()
}

export async function setOtpCode(otpCode: string) {
    const resp = await fetch(`${backendUrl}/api/admin/login/otp`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({otpCode: otpCode})
    })
    if (resp.status !== 200)
        throw resp
}

export async function generateInvite(): Promise<iAdminInvite> {
    const resp = await fetch(`${backendUrl}/api/admin/invite`, {
        method: 'POST'
    })
    if (resp.status !== 200)
        throw resp
    return await resp.json()
}

export async function getInvites(): Promise<string[]> {
    const resp = await fetch(`${backendUrl}/api/admin/invite`, {
        method: 'GET'
    })
    if (resp.status !== 200)
        throw resp
    return await resp.json()
}

export async function deleteInvite(inviteId: string) {
    const resp = await fetch(`${backendUrl}/api/admin/invite?inviteId=${inviteId}`, {
        method: 'DELETE'
    })
    if (resp.status !== 200)
        throw resp
}
