/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AdminModel } from '../models/AdminModel';
import type { CapybaraModel } from '../models/CapybaraModel';
import type { StatsModel } from '../models/StatsModel';
import type { SubmitModal } from '../models/SubmitModal';

import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';

export class DefaultService {

    constructor(public readonly httpRequest: BaseHttpRequest) {}

    /**
     * @param daysAgo
     * @returns CapybaraModel Request fulfilled, document follows
     * @throws ApiError
     */
    public getTodayCapybara(
        daysAgo?: (null | number),
    ): CancelablePromise<CapybaraModel> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/',
            query: {
                'days_ago': daysAgo,
            },
            errors: {
                400: `Bad request syntax or unsupported method`,
            },
        });
    }

    /**
     * @param formData
     * @returns any Document created, URL follows
     * @throws ApiError
     */
    public submitCapy(
        formData: SubmitModal,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/submit',
            formData: formData,
            mediaType: 'multipart/form-data',
            errors: {
                400: `Bad request syntax or unsupported method`,
            },
        });
    }

    /**
     * @param code
     * @returns AdminModel Document created, URL follows
     * @throws ApiError
     */
    public adminAuthAuth(
        code: string,
    ): CancelablePromise<AdminModel> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/admin/auth',
            query: {
                'code': code,
            },
            errors: {
                400: `Bad request syntax or unsupported method`,
            },
        });
    }

    /**
     * @returns StatsModel Request fulfilled, document follows
     * @throws ApiError
     */
    public adminStatsStats(): CancelablePromise<StatsModel> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/admin/stats',
        });
    }

    /**
     * @returns any Request fulfilled, document follows
     * @throws ApiError
     */
    public adminLogoutLogout(): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/admin/logout',
        });
    }

}
