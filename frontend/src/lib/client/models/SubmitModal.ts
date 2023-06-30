/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RelationshipEnum } from './RelationshipEnum';

export type SubmitModal = {
    image: Blob;
    name?: string;
    relationship_status?: RelationshipEnum;
};

