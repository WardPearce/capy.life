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


export interface iToApproveCapy {
    name: string
    image: string
    _id: string
}
