/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export { CapyClient } from './CapyClient';

export { ApiError } from './core/ApiError';
export { BaseHttpRequest } from './core/BaseHttpRequest';
export { CancelablePromise, CancelError } from './core/CancelablePromise';
export { OpenAPI } from './core/OpenAPI';
export type { OpenAPIConfig } from './core/OpenAPI';

export type { AdminModel } from './models/AdminModel';
export type { CapybaraModel } from './models/CapybaraModel';
export type { CreateAdminModel } from './models/CreateAdminModel';
export type { ListAdminsModel } from './models/ListAdminsModel';
export { RelationshipEnum } from './models/RelationshipEnum';
export type { StatsModel } from './models/StatsModel';
export type { SubmitModal } from './models/SubmitModal';
export type { ToApproveModel } from './models/ToApproveModel';

export { AdminService } from './services/AdminService';
export { DefaultService } from './services/DefaultService';
