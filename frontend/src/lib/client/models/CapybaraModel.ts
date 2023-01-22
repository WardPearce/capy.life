/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RelationshipEnum } from './RelationshipEnum';

export type CapybaraModel = {
    name: string;
    image: string;
    _id: string;
    muncher_lvl: number;
    weapon: string;
    class: string;
    used?: string;
    relationship_status: RelationshipEnum;
    days_ago: number;
};

