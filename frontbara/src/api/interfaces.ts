export interface iCaptcha {
    imageB64: string
    captchaId: string
}

export interface iCapySubmit {
    name?: string
    email?: string
    captchaCode?: string
    image: FileList
}
