import type { iCaptcha, iCapySubmit } from './interfaces'

const backendUrl: string = import.meta.env.VITE_BACKEND_URL as string

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
