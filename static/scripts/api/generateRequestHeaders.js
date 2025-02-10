import { getCsrfToken } from '../utilities/csrf.js';

/**
 * Generate request headers.
 *
 * @param {Object} params - The parameters for the request.
 * @param {string} params.accept - The accept header.
 * @param {string | null} params.contentType - The content type header.
 *  If not provided, it will be set to 'application/json'. If it is set to null,
 *  it will be removed from the headers.
 * @param {string} params.csrfToken - The CSRF token to use.
 * @param {Object} params.dict - Additional headers to add to the request.
 * @returns {Object} The headers.
 */
const generateRequestHeaders = ({
    accept = 'application/json',
    contentType,
    csrfToken = getCsrfToken(),
    ...dict
} = {}) => {
    if (contentType === undefined) {
        contentType = 'application/json';
    } else if (contentType === null) {
        contentType = undefined;
    }

    const headers = {
        Accept: accept,
        'X-CSRFToken': csrfToken,
        ...dict,
    };

    if (contentType !== undefined) {
        headers['Content-Type'] = contentType;
    }

    return headers;
};

export { generateRequestHeaders };
