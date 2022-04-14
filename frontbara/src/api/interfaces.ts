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

export interface iCapy {
    name: string
    image: string
    _id: string
}

export interface iCapyApprovalHistory {
    approvedBy: string
    approvedAt: string
}

export interface iCapyHistory extends iCapy {
    used: string
}

export interface iCapyCount {
    remaining: number
    total: number
}

export interface iAdminLogin {
    isRoot: boolean
    otpCompleted: boolean
}

export interface iAdminOtp {
    provisioningUri: string
}

export interface iAdminInvite {
    inviteCode: string
}

export interface iAdminDetails {
    username: string
    password: string
    otpCode?: string
    inviteCode?: string
}
