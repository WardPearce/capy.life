/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AdminModel } from '../models/AdminModel';
import type { CreateAdminModel } from '../models/CreateAdminModel';
import type { ListAdminsModel } from '../models/ListAdminsModel';
import type { StatsModel } from '../models/StatsModel';
import type { ToApproveModel } from '../models/ToApproveModel';

import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';

export class AdminService {

    constructor(public readonly httpRequest: BaseHttpRequest) {}

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
     * @returns ToApproveModel Request fulfilled, document follows
     * @throws ApiError
     */
    public adminToApproveToApprove(): CancelablePromise<ToApproveModel> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/admin/to-approve',
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

    /**
     * @param requestBody
     * @returns any Document created, URL follows
     * @throws ApiError
     */
    public adminAddAddAdmin(
        requestBody: CreateAdminModel,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/admin/add',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Bad request syntax or unsupported method`,
            },
        });
    }

    /**
     * @param adminId
     * @returns void
     * @throws ApiError
     */
    public adminRemoveRemoveAdmin(
        adminId: string,
    ): CancelablePromise<void> {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/admin/remove/{admin_id}',
            path: {
                'admin_id': adminId,
            },
            errors: {
                400: `Bad request syntax or unsupported method`,
            },
        });
    }

    /**
     * @returns ListAdminsModel Request fulfilled, document follows
     * @throws ApiError
     */
    public adminListListAdmins(): CancelablePromise<ListAdminsModel> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/admin/list',
        });
    }

    /**
     * @param capyId
     * @param changeName
     * @returns any Document created, URL follows
     * @throws ApiError
     */
    public adminApproveApproveCapy(
        capyId: string,
        changeName: number,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/admin/approve/{capy_id}/{change_name}',
            path: {
                'capy_id': capyId,
                'change_name': changeName,
            },
            errors: {
                400: `Bad request syntax or unsupported method`,
            },
        });
    }

    /**
     * @param capyId
     * @returns void
     * @throws ApiError
     */
    public adminDenyDenyCapy(
        capyId: string,
    ): CancelablePromise<void> {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/admin/deny/{capy_id}',
            path: {
                'capy_id': capyId,
            },
            errors: {
                400: `Bad request syntax or unsupported method`,
            },
        });
    }

}
