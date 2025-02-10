import { wrapResponse } from './wrapResponse.js';
import { urlWithParams } from '../utilities/urls.js';

/**
 * Get shelters for a point.
 *
 * @param {Object} params - The parameters for the request.
 * @param {number} params.longitude - The longitude of the point.
 * @param {number} params.latitude - The latitude of the point.
 * @param {number} [params.offset] - The offset of the shelters.
 * @param {number} [params.limit] - The limit of the shelters.
 * @param {number} [params.range] - The range of the shelters.
 */
const getSheltersForPoint = async ({
    longitude,
    latitude,
    offset,
    limit,
    range,
}) => {
    const url = urlWithParams('/arcgis/shelters', {
        longitude,
        latitude,
        offset,
        limit,
        range,
    });

    return await wrapResponse(fetch(url));
};

export { getSheltersForPoint };
